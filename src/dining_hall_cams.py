import os
import requests
from PIL import Image
import pandas as pd
from datetime import datetime, date, timedelta


root_dir = os.path.join(os.path.dirname(__file__), '..')
cases_days_map = {
    'weekday': [1, 2, 3, 4, 5],
    'weekend': [6, 7],
    'latenite': [1, 2, 3, 4]
}


def get_still(dining_hall):
    '''
    gets still image from UCSB dining cam API

    INPUT
        dining_hall string, name of dining hall ["carrillo", "de-la-guerra", or "ortega"]

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
        dining_hall string, name of dining hall ["carrillo", "de-la-guerra", or "ortega"]
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


def dining_hall_open(dining_hall, now=None):
    '''
    checks whether or not a dining hall is open

    INPUT
        dining_hall     string, name of dining hall ["carrillo", "de-la-guerra", or "ortega"]
        now (optional)  datetime, time to check for dining hall availability, current time by default

    OUTPUT
        is_open         boolean, True if dining hall is open, False o.w.
    '''
    if now == None:
        now = datetime.today()
    day = now.isoweekday()
    relevant_hours = dining_hall_hours.loc[(dining_hall_hours['dining_hall'] == dining_hall) & (dining_hall_hours['day'] == day)]
    open_hours_list = list(relevant_hours.apply(lambda x: (x['start'], x['end']), axis=1))
    is_open = False
    for (start, end) in open_hours_list:
        start_time = datetime.strptime(start, '%I:%M:%S %p').time()
        end_time = datetime.strptime(end, '%I:%M:%S %p').time()
        if _time_in_range(start_time, end_time, now.time()):
            is_open = True
            break
    return is_open


def get_dining_hall_hours():
    '''
    reads dining hall operating hours data and lengthens it for optimal querying

    INPUT
        NONE

    OUTPUT
        dining_hall_hours_long  DataFrame, long format dataframe containing dining hall operating hours
    '''
    dining_hall_hours_path = os.path.join(root_dir, 'data', 'ucsb_dining_hall_hours.csv')
    dining_hall_hours = pd.read_csv(dining_hall_hours_path)
    dining_hall_hours_long = pd.DataFrame()
    for i in range(len(dining_hall_hours)):
        rec = dining_hall_hours.loc[i]
        long_rec = _dining_hall_hours_lengthen_rec(rec)
        dining_hall_hours_long = pd.concat([dining_hall_hours_long, long_rec])
    dining_hall_hours_long = dining_hall_hours_long

    return dining_hall_hours_long


def _dining_hall_hours_lengthen_rec(x):
    '''
    duplicates a record in the dining hall hours dataset for long format transformation

    INPUT
        x       Series, a record in the dining hall hours dataset

    OUTPUT
        x_long  DataFrame, contains the input record duplicated once for each day in the corresponding case
    '''
    days = cases_days_map[x['case']]
    nb_rec = len(days)
    dining_hall_li = [x['dining_hall']] * nb_rec
    start_li = [x['start']] * nb_rec
    end_li = [x['end']] * nb_rec
    desc_li = [x['desc']] * nb_rec
    x_dict = dict(
        dining_hall=dining_hall_li,
        day=days,
        start=start_li,
        end=end_li,
        desc=desc_li
    )
    x_long = pd.DataFrame(x_dict)

    return x_long


def _time_in_range(start, end, x):
    '''
    checks if a time is in a timerange
    NOTE: taken from https://stackoverflow.com/questions/10747974/how-to-check-if-the-current-time-is-in-range-in-python

    INPUT
        start   datetime.time, start of timerange
        end     datetime.time, end of timerange
        x       datetime.time, time to check

    OUTPUT
                boolean, True if time x is between start and end, False o.w.
    '''
    today = date.today()
    start = datetime.combine(today, start)
    end = datetime.combine(today, end)
    x = datetime.combine(today, x)
    if end <= start:
        end += timedelta(1)
    if x <= start:
        x += timedelta(1)

    return start <= x <= end


dining_hall_hours = get_dining_hall_hours()