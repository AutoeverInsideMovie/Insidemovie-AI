import torch
from transformers import AutoModelForSequenceClassification
from kobert_tokenizer import KoBERTTokenizer
from const import LABELS_5
from config import settings

_tokenizer = KoBERTTokenizer.from_pretrained(settings.model_dir)
_model     = AutoModelForSequenceClassification.from_pretrained(settings.model_dir)
_model.eval()


def get_avg_emotion(results: list[dict[str, float]]) -> dict[str, float]:
    if not results:
        return {label: 0.0 for label in LABELS_5}

    # 각 레이블별 합산
    sums = {label: 0.0 for label in LABELS_5}
    for prob in results:
        for label, score in prob.items():
            sums[label] += score

    # 평균 계산
    n = len(results)
    return {label: sums[label] / n for label in LABELS_5}

def _predict_batch(texts: list[str]) -> list[dict[str, float]]:
    inputs = _tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        logits = _model(**inputs).logits  # [batch_size, num_labels]
        probs = torch.softmax(logits, dim=-1)

    return [
        { LABELS_5[i]: float(prob[i]) for i in range(len(LABELS_5)) }
        for prob in probs
    ]


def predict_emotion_split_avg(text: str) -> dict[str, float]:
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if not sentences:
        sentences = [text.strip()]

    probs_list = _predict_batch(sentences)
    return get_avg_emotion(probs_list)


def predict_emotion_overall_avg(text: str) -> dict[str, float]:
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if not sentences:
        sentences = [text.strip()]
    all_texts = [text.strip()] + sentences

    probs_list = _predict_batch(all_texts)
    return get_avg_emotion(probs_list)


def predict_emotion_full(text: str) -> dict[str, float]:
    [prob] = _predict_batch([text.strip()])
    return prob