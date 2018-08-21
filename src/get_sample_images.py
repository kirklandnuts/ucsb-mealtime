import dining_hall_cams as cams
import os

dining_halls = ["carrillo", "de-la-guerra", "ortega"]
script_path = os.path.dirname(__file__)

if __name__ == '__main__':
    for dining_hall in dining_halls:
        save_filename = '{}_sample.jpg'.format(dining_hall)
        save_path = os.path.join(script_path, '..', 'img', save_filename)
        cams.save_still(dining_hall, save_path)