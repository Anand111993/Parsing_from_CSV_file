import pandas as pd
import os
import sys

def map_unmatched_endpoints(auth_file, endpoint_file, output_file):
    """Merge Endpoint Database with unmatched Endpoint IDs from Authentication Database."""

    print("\n🔍 Merging Endpoint Database with unmatched Endpoint IDs...\n")  # Print initial message

    # Load the Authentication Database CSV
    try:
        auth_df = pd.read_csv(auth_file)
    except Exception as e:
        print(f"❌ Error reading {auth_file}: {e}")
        return

    # Load the Endpoint Database CSV
    try:
        endpoint_df = pd.read_csv(endpoint_file)
    except Exception as e:
        print(f"❌ Error reading {endpoint_file}: {e}")
        return

    # Required columns mapping
    mapped_columns = {
        "Endpoint ID": "MACAddress",
        "Identity": "User-Name",
        "Endpoint Profile": "EndPointPolicy",
        "Device Type": "Device Type",
        "Location": "Location",
        "Identity Group": "IdentityGroup"
    }

    # Find unmatched Endpoint IDs
    unmatched_auth_df = auth_df[~auth_df["Endpoint ID"].isin(endpoint_df["MACAddress"])]

    if unmatched_auth_df.empty:
        print("✅ All Endpoint IDs from the Authentication Database are already present in the Endpoint Database.")
        print(f"✅ Full Endpoint Database saved as: {output_file}")
        endpoint_df.to_csv(output_file, index=False)
        return

    # Print the unmatched Endpoint IDs
    print("🔎 The following Endpoint IDs are NOT found in the Endpoint Database Combined:")
    for endpoint_id in unmatched_auth_df["Endpoint ID"].unique():
        print(f"   ➜ {endpoint_id}")

    print("\n✅ Processing unmatched Endpoint IDs and merging...\n")

    # Select and rename the required columns for new entries
    mapped_auth_df = unmatched_auth_df[list(mapped_columns.keys())].rename(columns=mapped_columns)

    # Ensure the mapped dataframe has the same column structure as Endpoint Database
    final_columns = endpoint_df.columns.tolist()  # Get the column order

    # Add missing columns with default static values
    static_values = {
        "DeviceRegistrationStatus": "NotRegistered",
        "BYODRegistration": "Unknown",
        "StaticAssignment": "FALSE",
        "StaticGroupAssignment": "FALSE"
    }

    for col in final_columns:
        if col not in mapped_auth_df.columns:
            mapped_auth_df[col] = static_values.get(col, "")  # Fill missing columns

    # Reorder columns to match Endpoint Database structure
    mapped_auth_df = mapped_auth_df[final_columns]

    # Merge both datasets
    combined_df = pd.concat([endpoint_df, mapped_auth_df], ignore_index=True)

    # Save the merged endpoint database
    combined_df.to_csv(output_file, index=False)

    print("\n✅ Merging complete!")
    print(f"✅ Full Mapped Endpoint Database saved as: {output_file}")

if __name__ == "__main__":
    # Check if the required arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python3 map_endpoints.py <auth_database_csv> <endpoint_database_csv>")
        sys.exit(1)

    auth_file = sys.argv[1]
    endpoint_file = sys.argv[2]
    output_file = "mapped_endpoint_database.csv"

    # Check if files exist
    if not os.path.exists(auth_file):
        print(f"❌ File '{auth_file}' not found.")
        sys.exit(1)
    if not os.path.exists(endpoint_file):
        print(f"❌ File '{endpoint_file}' not found.")
        sys.exit(1)

    map_unmatched_endpoints(auth_file, endpoint_file, output_file)
