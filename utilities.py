import uuid, os, re

# information on the time for functions to complete
sessionTimings = {
    "ImagesSent":0,
    "ImagesRecieved":0,
    "ImagesSavedLocally":0,
    "ImagesFormatted":0,
    "ImagesCropped":0,
    "ImagesEvaluated":0,
    }

def isUniqueID(id, dir_list):
    # Recursive function that ensures that the a data folder with the same ID does not exist
    unique = True
    for session in dir_list:
        if re.search(re.escape(id), session):
            unique = False
    if unique:
        return id
    else:
        newKey = genKey()
        return isUniqueID(newKey, dir_list)

def createImageInfo(imageNames):
    # create the dictionary array that holds the image data for one session
    sessionInfo = []
    for image in imageNames:
        # add information from name into dict
        match = re.search(r"(left|right)", image)
        side = ''
        if match:
            side = match.group(1)
        # add dict into array
        sessionInfo.append({
            'name':image,
            'eyeSide': side,
            'cropped':False,
            'prediction':'',
            'selectedForDisp':False})
    return sessionInfo

def genKey():
    # generate key for data base
    key = str(uuid.uuid4())
    return key

def deleteSessionImages(paths):
    # delete all images that were used for this session
    # Can be deprecated as session images are saved in unique foulders related to the id of the session
    for path in paths:
        dir_list = os.listdir(path)
        for dir in dir_list:
            os.remove(f"{path}/{dir}")
    print("deleted")
    return
'''
# for testing
# Paths to each of the images
imagePaths = ['session_images/recieved_images', 'session_images/formatted_images', 'session_images/cropped_images']
def main():
    deleteSessionImages(imagePaths)

if __name__ == '__main__':
    main()
'''
