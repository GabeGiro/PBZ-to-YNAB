import os
import pandas as pd
from src.transactions import extract_transactions_from_image

def extract_transactions_from_images_in_directory(input_dir: str) -> pd.DataFrame:
    all_data = []

    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(".png"):
            file_path = os.path.join(input_dir, file_name)
            df = extract_transactions_from_image(file_path)
            all_data.append(df)

    return pd.concat(all_data, ignore_index=True)


def save_transactions_to_csv(dataframe: pd.DataFrame, output_file: str) -> None:
    dataframe.to_csv(output_file, index=False)
    print(f"Transactions saved to {output_file}")


if __name__ == "__main__":
    input_dir = "data/sensitive/run"
    output_file = "data/sensitive/run/transactions.csv"

    final_df = extract_transactions_from_images_in_directory(input_dir)
    save_transactions_to_csv(final_df, output_file)
    print(final_df)