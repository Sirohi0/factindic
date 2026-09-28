from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM
from huggingface_hub import HfApi, hf_hub_download
import pandas as pd

MODEL = "csebuetnlp/mT5_multilingual_XLSum"
DATASET = "csebuetnlp/xlsum"
REV = "refs/convert/parquet"

cfg = AutoConfig.from_pretrained(MODEL)
print("config:", cfg.model_type, cfg.d_model, cfg.num_layers)

tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
print("params:", sum(p.numel() for p in model.parameters()))

path = hf_hub_download(DATASET, "hindi/test/0000.parquet", repo_type="dataset", revision=REV)
df = pd.read_parquet(path)
print("dataset shape:", df.shape)
print("columns:", df.columns.tolist())

api = HfApi()
print("model sha:", api.model_info(MODEL).sha)
print("dataset revision sha:", api.dataset_info(DATASET, revision=REV).sha)