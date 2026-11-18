"""Structural checks for the public Colab notebook's helper call contracts."""
import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "factindic_interactive_evaluation_colab.ipynb"


def _cells():
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]


def _python_cells():
    return [
        "".join(cell.get("source", []))
        for cell in _cells()
        if cell.get("cell_type") == "code"
    ]


def test_notebook_json_and_python_cells_are_well_formed():
    cells = _python_cells()
    assert cells
    for source in cells:
        # Skip Colab's standalone pip magic cell; all other cells must parse.
        if source.lstrip().startswith("%"):
            continue
        ast.parse(source)


def test_interactive_helpers_and_retry_parameter_are_defined():
    helpers = next(source for source in _python_cells() if "def check_claims(" in source)
    tree = ast.parse(helpers)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert {"make_summary", "check_claims", "factuality_summary"} <= functions.keys()
    summary_args = {arg.arg for arg in functions["make_summary"].args.args}
    assert "numeric_retry" in summary_args


def test_callback_uses_the_defined_numeric_retry_keyword():
    callback = next(source for source in _python_cells() if "def on_run_clicked(" in source)
    calls = [
        node
        for node in ast.walk(ast.parse(callback))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "make_summary"
    ]
    assert any(
        any(keyword.arg == "numeric_retry" for keyword in call.keywords)
        for call in calls
    )
