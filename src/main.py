import os
import pandas as pd
from src.transactions import extract_transactions_from_image

input_dir = "data/sensitive/run"
output_file = "data/sensitive/run/transactions.csv"

all_data = []

for file_name in os.listdir(input_dir):
    if file_name.lower().endswith(".png"):  
        file_path = os.path.join(input_dir, file_name)
        df = extract_transactions_from_image(file_path)
        all_data.append(df)

final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv(output_file, index=False)
print(final_df)