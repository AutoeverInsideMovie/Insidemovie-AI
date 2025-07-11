from fastapi import APIRouter, HTTPException
from datetime import datetime
from schemas import TextItem, Prediction
from services.prediction import predict_emotions
from db import collection

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/", response_model=Prediction)
async def create_prediction(item: TextItem):
    try:
        probs = predict_emotions(item.text)
        record = {
            "text": item.text,
            "probabilities": probs,
            "timestamp": datetime.utcnow()
        }
        await collection.insert_one(record)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=list[Prediction])
async def list_predictions(limit: int = 20):
    cursor = collection.find().sort("timestamp", -1).limit(limit)
    results = []
    async for doc in cursor:
        results.append(Prediction(**doc))
    return results