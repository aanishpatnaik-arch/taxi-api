from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TripQuery(BaseModel):
    start: datetime
    end: datetime
    pu_location_id: Optional[int] = None
    do_location_id: Optional[int] = None
