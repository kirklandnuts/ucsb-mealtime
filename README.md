# UCSB Meal Time
Determining wait times at UCSB dining halls via computer vision

## Data 
UCSB has recently released a series of APIs, [one of which](https://developer.ucsb.edu/apis/dining/dining-cams-v1) provides feeds from [cameras at Carrillo, DLG, and Ortega dining halls](http://www.housing.ucsb.edu/dining/dining-cams).

Here are examples of stills from each of the cameras retrieved by `get_sample_images.py` which uses the `get_cams` module.

Carrillo:  
![](img/carrillo_sample.jpg)

DLG:  
![](img/de-la-guerra_sample.jpg)

Ortega:  
![](img/ortega_sample.jpg)



## Requirements
### Data retrieval module
- during dining hall open hours, automatically collect still images for training
- get video feed

### Computer vision model
- image classification with {'no line', 'short line', 'long line'}
- object detection to count number of people in line

### Retraining
- automatically retrain model on a monthly basis with additional images collected since last training

