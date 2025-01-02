async def localImageSave(images, savePath):
    # open all images and return a list of all the image names
    imageList = []
    for image in images:
        # print for testing
        print(f"Received image: {image.filename}, Content-Type: {image.content_type}")
        imageList.append(image.filename)
        # save images to session images
        contents = await image.read()
        with open(f"{savePath}/uploaded_{image.filename}", "wb") as f:
            f.write(contents)
    return imageList

'''
# For testing
def main():
    ...

if __name__ == '__main__':
    main()
'''