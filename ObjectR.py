import base64
import urllib
import io
import os
import PIL # pip install Pillow
from IPython.display import display, Image

GOOGLE_API_KEY = 'AIzaSyAcLCy8_JBlvnVtI65HztU6ZLbMFKPUriw'

# pip install google-api-python-client
from googleapiclient.discovery import build
service = build('vision', 'v1', developerKey=GOOGLE_API_KEY)

cat = 'cat.jpg'

def label_image(path=None, URL=None, max_results=5):
    '''Read an image file (either locally or from the web) and pass the image data
    to Google's Cloud Vision API for labeling. Use the URL keyword to pass in the
    URL to an image on the web. Otherwise, pass in the path to a local image file.
    Use the max_results keyword to control the number of labels returned by
    the Cloud Vision API.
    '''
    if URL is not None:
        image_content = base64.b64encode(urllib.request.urlopen(URL).read())
    else:
        image_content = base64.b64encode(open(path, 'rb').read())
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [{
                'type': 'LABEL_DETECTION',
                'maxResults': max_results
            }]
        }]
    })
    labels = service_request.execute()['responses'][0]['labelAnnotations']
    if URL is not None:
        display(Image(url=URL))
    else:
        display(Image(path))
    for label in labels:
        print ('[{0:3.0f}%]: {1}'.format(label['score']*100, label['description']))

    return

# Finally, call the image labeling function on the image of a cat
label_image(cat)