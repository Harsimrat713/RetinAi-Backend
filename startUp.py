import os

# Run upon initialization to create image store folder

def generateImageStore():
    storePath = 'images_store'
    if not os.path.exists(storePath):
        os.makedirs(storePath)

def main():
    generateImageStore()

if __name__ == '__main__':
    main()