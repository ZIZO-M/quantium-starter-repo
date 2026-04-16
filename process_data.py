import pandas as pd
import glob

# Load and combine all CSV files
files = glob.glob("data/daily_sales_data_*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Filter to pink morsel only
df = df[df["product"] == "pink morsel"]

# Calculate sales: strip '$' from price, cast to float, multiply by quantity
df["sales"] = df["price"].str.replace("$", "", regex=False).astype(float) * df["quantity"]

# Keep only required columns
df = df[["sales", "date", "region"]]

# Write output
df.to_csv("output.csv", index=False)

print(f"Done. {len(df)} rows written to output.csv")
