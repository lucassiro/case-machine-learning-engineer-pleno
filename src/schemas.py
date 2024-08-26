from pydantic import BaseModel


class VariableSchema(BaseModel):
    origin_wind_speed: float
    dest_wind_speed: float


class PredictionSchema(BaseModel):
    status: str
    flight_delay: float


class StatusSchema(BaseModel):
    status: str
