from fastapi import APIRouter, HTTPException
from datetime import datetime
from schemas import TextItem, Prediction
from services.prediction import (
    predict_emotion_full,
    predict_emotion_split_avg,
    predict_emotion_overall_avg,
)
from db import collection

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/full", response_model=Prediction)
async def predict_full(item: TextItem):
    try:
        probs = predict_emotion_full(item.text)
        record = {
            "text": item.text,
            "probabilities": probs,
            "timestamp": datetime.utcnow()
        }
        await collection.insert_one(record)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/split_avg", response_model=Prediction)
async def predict_split_avg(item: TextItem):
    try:
        probs = predict_emotion_split_avg(item.text)
        record = {
            "text": item.text,
            "probabilities": probs,
            "timestamp": datetime.utcnow()
        }
        await collection.insert_one(record)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/overall_avg", response_model=Prediction)
async def predict_overall_avg(item: TextItem):
    try:
        probs = predict_emotion_overall_avg(item.text)
        record = {
            "text": item.text,
            "probabilities": probs,
            "timestamp": datetime.utcnow()
        }
        await collection.insert_one(record)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))