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


def test_single_date_mismatch_is_corrected_only_when_unambiguous():
    helpers = next(source for source in _python_cells() if "def correct_unique_source_date(" in source)
    tree = ast.parse(helpers)
    selected = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id in {"_MONTH_ALIASES", "_DATE_PATTERN"}
            for target in node.targets
        ):
            selected.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in {"_date_parts", "correct_unique_source_date", "unsupported_full_dates"}:
            selected.append(node)
    namespace = {"re": __import__("re")}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "<date-guard>", "exec"), namespace)

    source = "Vikram lander 23 August 2023 ko Moon par soft-land hua."
    summary = "Vikram landed on the Moon on 24 August 1923."
    corrected, details = namespace["correct_unique_source_date"](source, summary)
    assert corrected == "Vikram landed on the Moon on 23 August 2023."
    assert details == {"generated_date": "24 August 1923", "source_date": "23 August 2023"}

    ambiguous_source = source + " The article also mentions 14 July 2023."
    unchanged, details = namespace["correct_unique_source_date"](ambiguous_source, summary)
    assert unchanged == summary
    assert details is None
    assert namespace["unsupported_full_dates"](
        ambiguous_source, "The first event occurred on September 23, 2023."
    ) == ["September 23, 2023"]


def test_claim_checker_cannot_assert_numbers_absent_from_summary():
    helpers = next(source for source in _python_cells() if "def check_claims(" in source)
    tree = ast.parse(helpers)
    needed = {
        "normalize_quote", "parse_json_object", "parse_claim_payload", "check_claims",
        "numeric_tokens", "factuality_summary",
    }
    selected = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in needed
    ]
    namespace = {
        "json": json,
        "re": __import__("re"),
        "ast": ast,
        "unicodedata": __import__("unicodedata"),
        "CLAIM_CHECK_TOKEN_LIMIT": 768,
    }
    exec(compile(ast.Module(body=selected, type_ignores=[]), "<claim-consistency>", "exec"), namespace)
    raw = json.dumps({"claims": [
        {"claim": "Chandrayaan-2 landed on 23 August 2023", "status": "supported", "evidence": "Vikram landed"},
        {"claim": "Chandrayaan-1 landed on 31 July 1923", "status": "supported", "evidence": "Vikram landed"},
    ]})
    namespace["chat_generate"] = lambda *args: (raw, 20, 1.0)
    source = "Chandrayaan-3's Vikram lander landed on 23 August 2023."
    summary = "Chandrayaan-3's Vikram lander landed on 23 August 2023."
    claims, *_ = namespace["check_claims"](source, summary, None, None)
    assert [claim["assessment"] for claim in claims] == ["checker_mismatch", "checker_mismatch"]
    assert [claim["claim_numbers_not_in_summary"] for claim in claims] == [["2"], ["1", "1923", "31"]]
    assert "unreliable" in namespace["factuality_summary"](claims)
    assert all(not claim["source_evidence"] for claim in claims)


def test_summary_is_labeled_unverified_when_evidence_is_unclear_or_unavailable():
    helpers = next(source for source in _python_cells() if "def summary_requires_review(" in source)
    tree = ast.parse(helpers)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "summary_requires_review")
    namespace = {}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "<review-label>", "exec"), namespace)
    needs_review = namespace["summary_requires_review"]
    assert needs_review([{"assessment": "checker_mismatch", "quote_found_in_model_input": False}])
    assert needs_review([{"assessment": "supported", "quote_found_in_model_input": True}], date_correction={"source_date": "23 August 2023"})
    assert needs_review([], claim_check_error="bad JSON")
    assert not needs_review([{"assessment": "supported", "quote_found_in_model_input": True}])


def test_source_name_spelling_correction_uses_unique_source_identifiers():
    helpers = next(source for source in _python_cells() if "def correct_source_name_spellings(" in source)
    tree = ast.parse(helpers)
    selected = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in {"_identifier_number", "_entity_parts", "correct_source_name_spellings"}:
            selected.append(node)
    namespace = {"re": __import__("re"), "difflib": __import__("difflib")}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "<name-correction>", "exec"), namespace)
    source = "Chandrayaan-3 ka Vikram lander tha. Iske baad Pragyan rover lunar surface par utara."
    summary = "Chandryaan-III's Vikram lands; Pragyaan rover arrives."
    corrected, changes = namespace["correct_source_name_spellings"](source, summary)
    assert "Chandrayaan-3" in corrected
    assert "Pragyan rover" in corrected
    assert {item["source_name"] for item in changes} == {"Chandrayaan-3", "Pragyan"}


def test_numeric_tokens_normalize_fullwidth_digits():
    helpers = next(source for source in _python_cells() if "def numeric_tokens(" in source)
    tree = ast.parse(helpers)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "numeric_tokens")
    namespace = {"re": __import__("re"), "unicodedata": __import__("unicodedata")}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "<number-normalization>", "exec"), namespace)
    assert namespace["numeric_tokens"]("mission ３ on 23 August 2023") == ["3", "23", "2023"]


def test_all_called_notebook_helpers_are_defined():
    import builtins

    combined = "\n".join(
        source for source in _python_cells() if not source.lstrip().startswith("%")
    )
    tree = ast.parse(combined)
    defined = set(dir(builtins))
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined.add(target.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                defined.add(alias.asname or alias.name.split(".")[0])

    undefined = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            local_names = {arg.arg for arg in node.args.args}
            for inner in ast.walk(node):
                if isinstance(inner, ast.Assign):
                    for target in inner.targets:
                        if isinstance(target, ast.Name):
                            local_names.add(target.id)
                        elif isinstance(target, ast.Tuple):
                            for elt in target.elts:
                                if isinstance(elt, ast.Name):
                                    local_names.add(elt.id)
            for inner in ast.walk(node):
                if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name):
                    if inner.func.id not in defined and inner.func.id not in local_names:
                        undefined.add(inner.func.id)
    assert not undefined, f"Undefined helper calls in notebook: {sorted(undefined)}"


def test_chat_generate_does_not_block_repeated_ngrams():
    helpers = next(source for source in _python_cells() if "def chat_generate(" in source)
    assert "no_repeat_ngram_size" not in helpers
    assert "repetition_penalty" not in helpers


def test_summary_requires_review_when_nli_flags_contradiction():
    helpers = next(source for source in _python_cells() if "def summary_requires_review(" in source)
    tree = ast.parse(helpers)
    function = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "summary_requires_review"
    )
    namespace = {}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "<nli-review>", "exec"), namespace)
    needs_review = namespace["summary_requires_review"]
    assert needs_review([{
        "assessment": "supported",
        "quote_found_in_model_input": True,
        "independent_nli_label": "contradiction",
    }])


def test_fact_anchors_and_hinglish_nli_normalization():
    helpers = next(source for source in _python_cells() if "def extract_fact_anchors(" in source)
    tree = ast.parse(helpers)
    needed = {
        "_MONTH_ALIASES", "_DATE_PATTERN", "_HINGLISH_NLI_GLOSSES",
        "numeric_tokens", "extract_fact_anchors", "normalize_hinglish_for_nli",
    }
    selected = [
        node for node in tree.body
        if (isinstance(node, ast.FunctionDef) and node.name in needed)
        or (isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id in needed for t in node.targets
        ))
    ]
    namespace = {"re": __import__("re"), "unicodedata": __import__("unicodedata")}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "<anchors-nli>", "exec"), namespace)

    warning_src = (
        "Heavy rain ke baad administration ne alert jaari kiya hai ki log Yamuna nadi ke kinare "
        "bilkul na jaayein aur bridge par traffic band hai."
    )
    anchors = namespace["extract_fact_anchors"](warning_src)
    assert "bilkul na" in anchors["cues"]
    assert "band hai" in anchors["cues"]

    norm = namespace["normalize_hinglish_for_nli"](warning_src)
    assert "do not go" in norm.lower()
    assert "is closed" in norm.lower()


def test_dual_archetype_detection_and_validation():
    helpers = next(source for source in _python_cells() if "def detect_input_archetype(" in source)
    tree = ast.parse(helpers)
    function = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "detect_input_archetype"
    )
    namespace = {"re": __import__("re")}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "<archetype>", "exec"), namespace)
    detect = namespace["detect_input_archetype"]

    dev_sample = "भारत में pollution का level लगातार increase हो रहा है।"
    rom_sample = "Bharat me pollution ka level lagatar increase ho raha hai."
    assert detect(dev_sample, "Auto-detect") == "devanagari_codemixed"
    assert detect(rom_sample, "Auto-detect") == "roman_hinglish"
    assert detect(dev_sample, "Devanagari / Code-Mixed (Hindi + English)") == "devanagari_codemixed"
    assert detect(rom_sample, "Roman-script Hinglish") == "roman_hinglish"

    try:
        detect(dev_sample, "Roman-script Hinglish")
        raise AssertionError("Expected ValueError for Devanagari in Roman mode")
    except ValueError:
        pass
