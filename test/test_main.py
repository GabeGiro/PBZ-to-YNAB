import os
import pandas as pd
from src.main import extract_transactions_from_images_in_directory, save_transactions_to_csv


def test_process_images_in_directory(tmpdir):
    """
    Test the process_images_in_directory function with sample images.
    """
    input_dir = tmpdir.mkdir("images")
    sample_image_path = input_dir.join("sample.png")
    sample_image_path.write("dummy image content")

    def mock_extract_transactions_from_image(image_path):
        return pd.DataFrame({"Date": ["2025-07-26"], "Description": ["Test"], "Amount (EUR)": [10.0]})

    original_function = extract_transactions_from_image
    extract_transactions_from_image = mock_extract_transactions_from_image

    try:
        result = extract_transactions_from_images_in_directory(str(input_dir))

        assert not result.empty
        assert len(result) == 1
        assert list(result.columns) == ["Date", "Description", "Amount (EUR)"]
    finally:
        extract_transactions_from_image = original_function


def test_save_transactions_to_csv(tmpdir):
    """
    Test the save_transactions_to_csv function.
    """
    dataframe = pd.DataFrame({"Date": ["2025-07-26"], "Description": ["Test"], "Amount (EUR)": [10.0]})

    output_file = tmpdir.join("transactions.csv")

    save_transactions_to_csv(dataframe, str(output_file))

    assert os.path.exists(output_file)

    saved_data = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(dataframe, saved_data)


def test_process_images_with_different_extensions(tmpdir):
    """
    Test that both .PNG and .png files are processed.
    """
    input_dir = tmpdir.mkdir("images")

    png_image_path = input_dir.join("sample.png")
    png_image_path.write("dummy image content")

    uppercase_png_image_path = input_dir.join("sample.PNG")
    uppercase_png_image_path.write("dummy image content")

    def mock_extract_transactions_from_image(image_path):
        return pd.DataFrame({"Date": ["2025-07-26"], "Description": ["Test"], "Amount (EUR)": [10.0]})

    original_function = extract_transactions_from_image
    extract_transactions_from_image = mock_extract_transactions_from_image

    try:
        result = extract_transactions_from_images_in_directory(str(input_dir))

        assert not result.empty
        assert len(result) == 2
        assert list(result.columns) == ["Date", "Description", "Amount (EUR)"]
    finally:
        extract_transactions_from_image = original_function
