import uuid, os

imagePaths = ['session_images/recieved_images', 'session_images/formatted_images', 'session_images/cropped_images']

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
