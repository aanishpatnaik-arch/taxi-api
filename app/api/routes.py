from fastapi import APIRouter,Query
from app.models.schemas import TripQuery
from typing import Optional
from app.services.trip_service import *

router = APIRouter()

@router.post("/trips_summary")
def trips_summary(query: TripQuery):
    return get_trip_summary(query)

@router.post("/weekly_trips")
def weekly_trips(query: TripQuery):
    return get_weekly_trips(query)

@router.get("/summary")
def get_summary():
    return get_summary_service()

@router.get("/sample")
def get_sample(n:int=Query(...,description="filter by n")):
    return get_sample_data(n)

@router.get("/filtered_passengers")
def filtered_passengers(passenger_count: int = Query(..., description="Filter trips by passenger count")):
    return get_filtered_passengers(passenger_count)

@router.get("/trip_duration_preview")
def trip_duration():
    return get_trip_duration_preview()

@router.get("/daily_trips")
def daily_trips():
    return get_daily_trips()

@router.get("/top_pickup_locations")
def top_pickup_locations(top: int = Query(..., description="Number of top pickup locations to return")):
    return get_top_pickup_locations(top)

@router.get("/revenue_by_vendor")
def revenue_by_vendor():
    return get_revenue_by_vendor()

@router.get("/avg_fare_per_mile")
def avg_fare_per_mile():
    return get_avg_fare_per_mile()

@router.get("/peak_hours")
def peak_hours():
    return get_peak_hours()

@router.get("/payment_split")
def payment_split():
    return get_payment_split()

@router.get("/airport_trips")
def airport_trips():
    return get_airport_trips()

@router.get("/passenger_distribution")
def passenger_distribution():
    return get_passenger_distribution()

@router.get("/high_tips")
def high_tips(min_tip: float = Query(..., description="Minimum tip amount")):
    return get_high_tips(min_tip)

@router.get("/longest_trips")
def longest_trips(top: int = Query(..., description="Top N longest trips")):
    return get_longest_trips(top)

@router.get("/congestion_impact")
def congestion_impact():
    return get_congestion_impact()

@router.get("/avg_duration_vendor")
def avg_duration_vendor():
    return get_avg_duration_vendor()

@router.get("/monthly_revenue")
def monthly_revenue():
    return get_monthly_revenue()