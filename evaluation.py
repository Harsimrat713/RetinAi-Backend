from utilities import genKey

async def evaluation(images):
    # generate a key for this session
    #session_key = genKey()

    results = []
    # go through each image
    for image in images:
        print(f"Received image: {image.filename}, Content-Type: {image.content_type}")
        # You can save the file or process it here
        contents = await image.read()
        with open(f"uploaded_{image.filename}", "wb") as f:
            f.write(contents)
    
    return results