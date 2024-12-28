from ultralytics import YOLO
from PIL import Image

#from utilities import imagePaths

# Load the YOLO model
model = YOLO('models/retinai_yolo.pt')

def crop_image(model, image_path, imageName, saveLocation):
    # Load the image
    image = Image.open(image_path).convert("RGB")

    # Perform inference
    results = model(image)

    # Extract bounding box data
    boxes = results[0].boxes  # Get the box
    if len(boxes) == 0:
        # no boxes found so no cropping
        print("No objects detected.")
        return None
    else:
        # crop box found
        box = boxes.xyxy[0].cpu().numpy()  # Convert to numpy array
        x1, y1, x2, y2 = map(int, box)  # Bounding box coordinates

        # Crop the image
        cropped_image = image.crop((x1, y1, x2, y2))

        # Save the cropped image
        cropped_image.save(f'{saveLocation}/cropped_{imageName}')

        return cropped_image

def cropImages(imageLocation, saveLocation, imageNames, sessionInfo):
    # take the location of where the images are, where the cropped images will be saved, and the names of the images
    for image, imageInfo in zip(imageNames, sessionInfo):
        cropped = crop_image(model, f'{imageLocation}/uploaded_{image}', image, saveLocation)
        if cropped:
            cropped.show()  # Display image
            imageInfo['cropped'] = True
        else:
            print("No cropping performed.")
    return sessionInfo

'''
# for testing
def main():
    cropImages(imagePaths[1], imagePaths[2], ['937_right.jpg'])

if __name__ == '__main__':
    main()
'''
