import csv
import os


def load_image(image_number):
    image_dir = "data/sprites/pokemon"
    image_path = os.path.join(image_dir, '{}.png'.format(image_number))
    if os.path.exists(image_path):
        return image_path
    return os.path.join(image_dir, 'substitute.png')


def table_data_gen(table_name):
    data_file_name = os.path.join('data', 'csv', '{}.csv'.format(table_name))
    with open(data_file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # FIXME: Hardcode English
            if row.get('local_language_id'):
                if row['local_language_id'] == '9':
                    yield row
            elif row.get('language_id'):
                if row['language_id'] == '9':
                    yield row
            else:
                yield row
