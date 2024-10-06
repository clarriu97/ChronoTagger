# chrono_tagger/main.py

import os
import re
from datetime import datetime, timedelta
from PIL import Image
import piexif
import argparse


def extract_date_and_order_img_yyyymmdd(filename):
    """
    Extract date and order number from filenames matching the pattern IMG-yyyymmdd-WAXXXX.
    """
    pattern = r'^IMG-(\d{4})(\d{2})(\d{2})-WA(\d{4,})'
    match = re.match(pattern, filename)
    if match:
        year, month, day, order_number = match.groups()
        order_number = int(order_number)
        base_datetime = datetime(int(year), int(month), int(day))
        adjusted_datetime = base_datetime + timedelta(seconds=order_number)
        date_str = adjusted_datetime.strftime("%Y:%m:%d %H:%M:%S")
        return date_str
    return None


def process_images(undated_folder, dated_folder):
    """
    Process images in the undated_folder, add EXIF date metadata, and save them to dated_folder.
    """
    if not os.path.exists(dated_folder):
        os.makedirs(dated_folder)

    date_extractors = [
        extract_date_and_order_img_yyyymmdd,
    ]

    for filename in sorted(os.listdir(undated_folder)):
        file_path = os.path.join(undated_folder, filename)

        if os.path.isfile(file_path):
            date_str = None

            for extractor in date_extractors:
                date_str = extractor(filename)
                if date_str:
                    break

            if date_str:
                try:
                    img = Image.open(file_path)
                    exif_dict = piexif.load(img.info.get('exif', b''))

                    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_str
                    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_str

                    exif_bytes = piexif.dump(exif_dict)

                    new_file_path = os.path.join(dated_folder, filename)

                    img.save(new_file_path, exif=exif_bytes)
                    img.close()

                    print(f"Processed: {filename} with date {date_str}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
            else:
                print(f"Could not extract date from: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Add dates to images based on filename patterns.'
    )
    parser.add_argument(
        '--undated_folder',
        type=str,
        default='undated',
        help='Folder containing images without dates.'
    )
    parser.add_argument(
        '--dated_folder',
        type=str,
        default='dated',
        help='Folder to save images with dates.'
    )

    args = parser.parse_args()

    process_images(args.undated_folder, args.dated_folder)


if __name__ == '__main__':
    main()
