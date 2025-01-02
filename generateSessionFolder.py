import os

from utilities import genKey, isUniqueID

def generateSessionFolder(imageStoreLocation):
    # base location of diffrent session's images
    sessionID = genKey()
    path = []
    dir_list = os.listdir(imageStoreLocation)
    # varify that the ID is unique
    varifiedID = isUniqueID(sessionID, dir_list)
    path.append(f"{imageStoreLocation}/{varifiedID}_Session_Images")
    # Make base directory for this session
    os.makedirs(path[0])
    # Make path to recieved images
    path.append(f"{path[0]}/recieved_images")
    os.makedirs(path[1])
    # Make path to formatted images
    path.append(f"{path[0]}/formatted_images")
    os.makedirs(path[2])
    # Make path to cropped images
    path.append(f"{path[0]}/cropped_images")
    os.makedirs(path[3])
    
    return varifiedID, path

# For testing
'''
def main():
    sessionId, path = generateSessionFolder('testingFolder')

if __name__ == '__main__':
    main()
'''
