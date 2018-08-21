import requests
from PIL import Image

def get_still(dining_hall):
    '''
    gets still image from UCSB dining cam API

    INPUT
        dining_hall string, name of dining hall {"carrillo", "de-la-guerra", or "ortega"}

    OUTPUT
        image       PIL JpegImageFile
    '''
    url = 'https://api.ucsb.edu/dining/cams/v1/still/{}'.format(dining_hall)
    r = requests.get(url, stream=True)
    image = Image.open(r.raw)
    return image

def save_still(dining_hall, save_path):
    '''
    saves still image from UCSB dining cam API to specified location

    INPUT
        dining_hall string, name of dining hall {"carrillo", "de-la-guerra", or "ortega"}

    OUTPUT
        success     boolean, True if still image was successfully saved, False o.w.
    '''
    success = True
    try:
        image = get_still(dining_hall)
        image.save(save_path)
    except:
        success = False
    return success