def extract_right_part_of_image(image, percentage=0.7):
    height, width = image.shape[:2]
    start_column = round(width * (1 - percentage))
    return image[:, start_column:]


def extract_left_part_of_image(image, percentage=0.3):
    height, width = image.shape[:2]
    end_column = int(width * percentage)
    return image[:, :end_column]


def extract_bottom_part_of_image(image, percentage=0.8):
    height, width = image.shape[:2]
    start_row = round(height * (1 - percentage))
    return image[start_row:, :]