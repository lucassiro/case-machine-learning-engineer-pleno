import pickle
from datetime import datetime
from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, File, HTTPException

from src.history import History
from src.model import load_model
from src.schemas import PredictionSchema, StatusSchema, VariableSchema

app = FastAPI()


@app.post("/model/predict/", response_model=PredictionSchema, status_code=HTTPStatus.OK)
async def predict(variables: VariableSchema):
    model = load_model()
    if model is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="model not found, send a model first using /model/load/"
        )

    prediction = model.predict([[variables.origin_wind_speed, variables.dest_wind_speed]])

    history = History()
    history.insert_one({
        "timestamp": datetime.now(),
        "origin_wind_speed": variables.origin_wind_speed,
        "dest_wind_speed": variables.dest_wind_speed,
        "flight_delay": prediction[0],
    })

    response = PredictionSchema(status="ok", flight_delay=prediction[0])
    return response


@app.post("/model/load/", status_code=HTTPStatus.OK, response_model=StatusSchema)
async def load(model: bytes = File()):
    model = pickle.loads(model)
    with open("src/models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    status = StatusSchema(status="ok")
    return status


@app.get("/model/history/", status_code=HTTPStatus.OK)
async def history():
    history = History().get_history()

    return {"status": "ok", "history": history}


@app.get("/health/", status_code=HTTPStatus.OK, response_model=StatusSchema)
async def health():
    status = StatusSchema(status="ok")
    return status


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
