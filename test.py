import pandas as pd

# Load the CSV file
file_path = "30-Day- Auth- SW1.csv"  # Replace with actual file path
df = pd.read_csv(file_path)

# Convert "Logged At" column to datetime
df["Logged At"] = pd.to_datetime(df["Logged At"])

# Sort DataFrame by "Logged At" in descending order
df_sorted = df.sort_values(by="Logged At", ascending=False)

# Drop duplicates based on "Endpoint ID", keeping the latest occurrence
df_deduplicated = df_sorted.drop_duplicates(subset=["Endpoint ID"], keep="first")

# Save to a new CSV file
output_path = "cleaned_auth_database.csv"
df_deduplicated.to_csv(output_path, index=False)

print(f"Processed file saved as: {output_path}")
