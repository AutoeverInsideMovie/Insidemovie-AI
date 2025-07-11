import torch
from transformers import AutoModelForSequenceClassification
from kobert_tokenizer import KoBERTTokenizer
from const import LABELS_7
from config import settings

_tokenizer = KoBERTTokenizer.from_pretrained(settings.model_dir)
_model     = AutoModelForSequenceClassification.from_pretrained(settings.model_dir)
_model.eval()

def predict_emotions(text: str) -> dict[str, float]:
    inputs = _tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = _model(**inputs)
        probs = torch.softmax(outputs.logits[0], dim=-1)
    return { LABELS_7[i]: float(probs[i]) for i in range(len(LABELS_7)) }