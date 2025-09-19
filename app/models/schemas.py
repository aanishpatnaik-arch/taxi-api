from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TripQuery(BaseModel):
    start: datetime = Field(..., description="Start datetime in ISO format")
    end: datetime = Field(..., description="End datetime in ISO format")
    pu_location_id: Optional[int] = Field(None, description="Pickup location ID filter")
    do_location_id: Optional[int] = Field(None, description="Dropoff location ID filter")
