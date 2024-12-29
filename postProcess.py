def postProcess(sessionInfo):
    # just selects the first two valid images for now
    # will later adjust as needed
    chosenImageNames = []
    r = False 
    l = False
    for image in sessionInfo:
        if image['prediction'] != ('' or 'Unknown') and not image['selectedForDisp'] and len(chosenImageNames) < 2:
            # if the image does not have a prediction or is not Unknown
            # if the image is not already selected
            # and if both images have not been selected yet
            if image['eyeSide'] == 'right' and not r:
                # if the image is of the right side and the right side image has not been selected yet
                r = True
                chosenImageNames.append(image['name'])
                image['selectedForDisp'] = True
            if image['eyeSide'] == 'left' and not l:
                # if the image is of the left side and the left side image has not been selected yet
                l = True
                chosenImageNames.append(image['name'])
                image['selectedForDisp'] = True
    return chosenImageNames, sessionInfo


# for testing
def main():
    chosenImageNames, sessionInfo = postProcess( 
        [{
            "name": "Corolla GR.jpg",
            "eyeSide": "",
            "cropped": False,
            "prediction": "",
            "selectedForDisp": False
            },
            {
            "name": "937_left.jpg",
            "eyeSide": "left",
            "cropped": True,
            "prediction": "Glaucoma",
            "selectedForDisp": False
            },
            {
            "name": "937_right.jpg",
            "eyeSide": "right",
            "cropped": True,
            "prediction": "Glaucoma",
            "selectedForDisp": False
            }
        ])
    print(chosenImageNames)
    print(sessionInfo)

if __name__ == '__main__':
    main()
