import os
import time
from datetime import datetime
import dining_hall_cams as cams
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='collect images from dining hall cams during open hours')
    parser.add_argument('-o', '--output_dir')
    args = parser.parse_args()
    output_dir = args.output_dir

    for dining_hall in cams.dining_halls:
        dining_hall_dir = os.path.join(output_dir, dining_hall)
        if not os.path.exists(dining_hall_dir):
            os.makedirs(dining_hall_dir)

    while True:
        now = datetime.today()
        print('==== {}'.format(datetime.strftime(now, '%m/%d/%y %I:%M:%S %p')))
        for dining_hall in cams.dining_halls:
            if cams.dining_hall_open(dining_hall):
                datetime_current = datetime.strftime(now, '%m%d%yT%H%M%S')
                image_save_name = '{}{}.jpg'.format(dining_hall[0], datetime_current)
                image_save_path = os.path.join(output_dir, dining_hall, image_save_name)
                cams.save_still(dining_hall, image_save_path)
                print('saved image {}'.format(image_save_path))
            else:
                print('{} is not open'.format(dining_hall))
        time.sleep(5)