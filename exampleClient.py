# an example of how piboard will call api
import requests

# Prepare the files for the request
files = [
    ('images', ('image1.jpg', open('image1.jpg', 'rb'), 'image/jpeg')),
    ('images', ('image2.jpg', open('image2.jpg', 'rb'), 'image/jpeg')),
    # Add as many images as needed
]

kiosk_id = 'A1' 
kiosk_location = 'UW' 
time_stamp = 123456


# Send the POST request
request_url = 'http://127.0.0.1:8000'
response = requests.post('{request_url}/eye_evaluation/{kiosk_id}?kiosk_location={kiosk_location}&time_stamp={time_stamp}', files=files)

print(response.status_code)
print(response.json())