import os
import pandas as pd
from src.transactions import extract_transactions_from_image

input_dir = "data/sensitive"
output_file = "data/sensitive/transactions.csv"

all_data = []

for file_name in os.listdir(input_dir):
    if file_name.endswith(".png"):  # Process only PNG files
        file_path = os.path.join(input_dir, file_name)
        df = extract_transactions_from_image(file_path)
        all_data.append(df)

# Combine all data into a single DataFrame
final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv(output_file, index=False)
print(final_df)