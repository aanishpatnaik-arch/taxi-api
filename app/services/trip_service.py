from app.data.loader import df
from datetime import timedelta
from typing import Optional
from pandas import isna
import pandas as pd


def safe_response(func):
    """Decorator to wrap functions with try/except and prevent internal server errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}
    return wrapper


@safe_response
def get_trip_summary(query):
    
    start = pd.to_datetime(query.start)
    end = pd.to_datetime(query.end)
    mask = (
        (df["tpep_pickup_datetime"] >= start) &
        (df["tpep_dropoff_datetime"] <= end)
    )

    if query.pu_location_id is not None:
        mask &= df["PULocationID"] == query.pu_location_id

    if query.do_location_id is not None:
        mask &= df["DOLocationID"] == query.do_location_id

    filtered = df.loc[mask]

    return {
        "num_trips": len(filtered),
        "total_amount": float(filtered["total_amount"].sum())
    }


@safe_response
def get_weekly_trips(query):
    mask = (
        (df["tpep_pickup_datetime"] >= query.start) &
        (df["tpep_pickup_datetime"] <= query.end)
    )

    if query.pu_location_id is not None:
        mask &= df["PULocationID"] == query.pu_location_id

    if query.do_location_id is not None:
        mask &= df["DOLocationID"] == query.do_location_id

    filtered = df.loc[mask]

    result = []
    current_start = query.start

    while current_start <= query.end:
        current_end = min(
            current_start + timedelta(days=6, hours=23, minutes=59, seconds=59),
            query.end
        )

        week_mask = (
            (filtered["tpep_pickup_datetime"] >= current_start) &
            (filtered["tpep_pickup_datetime"] <= current_end)
        )
        week_trips = filtered.loc[week_mask]

        result.append({
            "week_start": current_start.strftime("%Y-%m-%d"),
            "week_end": current_end.strftime("%Y-%m-%d"),
            "num_trips": int(len(week_trips)),
            "total_amount": float(week_trips["total_amount"].sum())
        })

        current_start = current_start + timedelta(days=7)

    return result


@safe_response
def get_summary_service():
    columns = df.columns.tolist()
    row_count = len(df)
    vendors = df["VendorID"].dropna().unique().tolist()
    null_counts = df.isna().sum().to_dict()

    result = {
        "columns": columns,
        "row_count": row_count,
        "unique_vendors": vendors,
        "null_counts": null_counts
    }

    def replace_nan(obj):
        if isinstance(obj, list):
            return [replace_nan(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: replace_nan(v) for k, v in obj.items()}
        elif isna(obj):
            return None
        else:
            return obj

    return replace_nan(result)


@safe_response
def get_sample_data(n: int):
    sample_data = df.sample(n=n).where(pd.notna(df), None).to_dict(orient="records")
    return sample_data


@safe_response
def get_filtered_passengers(passenger_count: int):
    filtered_passengers = (
        df[df["passenger_count"] == passenger_count]
        .where(pd.notna(df), None)
        .to_dict(orient="records")
    )
    return filtered_passengers


@safe_response
def get_trip_duration_preview(limit: int = 10):
    temp_df = df.copy()
    temp_df["trip_duration_minutes"] = (
        (temp_df["tpep_dropoff_datetime"] - temp_df["tpep_pickup_datetime"])
        .dt.total_seconds()
        / 60
    )
    preview = (
        temp_df[["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_duration_minutes"]]
        .head(limit)
        .where(pd.notna(temp_df), None)
        .to_dict(orient="records")
    )
    return preview


@safe_response
def get_daily_trips():
    daily_counts = (
        df.groupby(df["tpep_pickup_datetime"].dt.date)
        .size()
        .reset_index(name="trip_count")
    )
    return daily_counts.to_dict(orient="records")


@safe_response
def get_top_pickup_locations(top: int):
    top_locations = (
        df["PULocationID"]
        .value_counts()
        .head(top)
        .reset_index()
    )
    return top_locations.to_dict(orient="records")


@safe_response
def get_revenue_by_vendor():
    revenue = (
        df.groupby("VendorID")["total_amount"]
        .sum()
        .reset_index()
    )
    return revenue.to_dict(orient="records")


@safe_response
def get_avg_fare_per_mile():
    safe_df = df[df["trip_distance"] > 0]
    avg = (safe_df["fare_amount"] / safe_df["trip_distance"]).mean()
    return {"avg_fare_per_mile": round(avg, 2)}


@safe_response
def get_peak_hours():
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    counts = df.groupby('pickup_hour').size().to_dict()
    return counts


@safe_response
def get_payment_split():
    counts = df['payment_type'].value_counts(normalize=True) * 100
    return counts.round(2).to_dict()


@safe_response
def get_airport_trips(limit: int = 100):
    airport = (
        df[df["Airport_fee"] > 0]
        .head(limit)
        .where(pd.notna(df), None)
        .to_dict(orient="records")
    )
    return airport


@safe_response
def get_passenger_distribution():
    counts = df['passenger_count'].value_counts().sort_index()
    return counts.to_dict()


@safe_response
def get_high_tips(min_tip: float = 20, limit: int = 100):
    high_tips = (
        df[df["tip_amount"] > min_tip]
        .head(limit)
        .where(pd.notna(df), None)
        .to_dict(orient="records")
    )
    return high_tips


@safe_response
def get_longest_trips(top: int = 5):
    longest = (
        df.sort_values(by="trip_distance", ascending=False)
        .head(top)
        .where(pd.notna(df), None)
        .to_dict(orient="records")
    )
    return longest


@safe_response
def get_congestion_impact():
    df['pickup_date'] = df['tpep_pickup_datetime'].dt.date
    impact = df.groupby('pickup_date')['congestion_surcharge'].sum().to_dict()
    return impact


@safe_response
def get_avg_duration_vendor():
    df['trip_duration_minutes'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    avg_duration = df.groupby('VendorID')['trip_duration_minutes'].mean().round(2).to_dict()
    return avg_duration


@safe_response
def get_monthly_revenue():
    monthly = (
        df.groupby(df["tpep_pickup_datetime"].dt.to_period("M"))["total_amount"]
        .sum()
        .reset_index()
    )
    monthly["tpep_pickup_datetime"] = monthly["tpep_pickup_datetime"].astype(str)
    return monthly.to_dict(orient="records")
