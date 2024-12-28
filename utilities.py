import uuid, os

# Paths to each of the images
imagePaths = ['session_images/recieved_images', 'session_images/formatted_images', 'session_images/cropped_images']
# information on the time for functions to complete
sessionTimings = {
    "ImagesSent":0,
    "ImagesRecieved":0,
    "ImagesSavedLocally":0,
    "ImagesFormatted":0,
    "ImagesCropped":0,
    "ImagesEvaluated":0,
    }

def createImageInfo(imageNames):
    # create the dictionary array that holds the image data for one session
    sessionInfo = []
    for image in imageNames:
        sessionInfo.append({
            'name':image,
            'cropped':False,
            'prediction':'',
            'selectedForDisp':False})
    return sessionInfo

def genKey():
    # generate key for data base
    key = str(uuid.uuid4())
    return key

async def localImageSave(images):
    # open all images and return a list of all the image names
    imageList = []
    for image in images:
        # print for testing
        print(f"Received image: {image.filename}, Content-Type: {image.content_type}")
        imageList.append(image.filename)
        # save images to session images
        contents = await image.read()
        with open(f"session_images/recieved_images/uploaded_{image.filename}", "wb") as f:
            f.write(contents)
    return imageList

def deleteSessionImages(paths):
    # delete all images that were used for this session
    for path in paths:
        dir_list = os.listdir(path)
        for dir in dir_list:
            os.remove(f"{path}/{dir}")
    print("deleted")
    return

# for testing
def main():
    deleteSessionImages(imagePaths)

if __name__ == '__main__':
    main()
