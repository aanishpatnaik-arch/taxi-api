import pandas as pd
from app.config import PARQUET_FILE

print("Loading parquet file...")
df = pd.read_parquet(PARQUET_FILE)
