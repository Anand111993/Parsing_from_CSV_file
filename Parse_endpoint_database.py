import pandas as pd
import os
import sys

def process_csv(file_path):
    """Process a single CSV file: remove duplicates based on MACAddress."""
    try:
        df = pd.read_csv(file_path)

        # Remove duplicates based on "MACAddress", keeping the first occurrence
        df_deduplicated = df.drop_duplicates(subset=["MACAddress"], keep="first")

        return df_deduplicated

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def process_folder(folder_path):
    """Process all CSV files in a folder and merge the cleaned data into one final CSV."""
    all_data = []  # List to store processed DataFrames

    # Iterate over all CSV files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_name}")

            df_cleaned = process_csv(file_path)
            if df_cleaned is not None:
                all_data.append(df_cleaned)

    # Combine all cleaned data
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        output_file = os.path.join(folder_path, "Endpoint Database Combined.csv")

        # Save final combined CSV
        final_df.to_csv(output_file, index=False)
        print(f"\n✅ Process completed! Combined file saved as: {output_file}")
    else:
        print("❌ No valid CSV files found or processed.")

if __name__ == "__main__":
    # Check if the folder path is provided
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print(f"❌ Folder '{folder_path}' does not exist.")
        sys.exit(1)

    print(f"\n📂 Processing all CSV files in folder: {folder_path}\n")
    process_folder(folder_path)
