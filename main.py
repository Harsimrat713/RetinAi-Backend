import time
from typing import List
from fastapi import FastAPI, File, UploadFile

from evaluation import evaluation
from utilities import deleteSessionImages, createImageInfo, sessionTimings
from generateSessionFolder import generateSessionFolder
from localImageSave import localImageSave
from format_images import formatImages
from imageCropping import cropImages
from postProcess import postProcess

app = FastAPI()

@app.get("/")
def Root_Response():
    # base response to check connection
    return {"Response": "Hello RetinAi Team"}

@app.post("/eye_evaluation/{kiosk_id}")
async def eye_evaluation(
    kiosk_id: str, # kiosk id
    kiosk_location:str, # kiosk location (may be deprecated)
    time_stamp:int, # time of kiosk request 
    images: List[UploadFile] = File(...) # array of images
    ):
    print("got request")
    # need to change the time.time() method as it does not take into account time zones
    sessionTimings['ImagesSent'] = time_stamp
    sessionTimings['ImagesRecieved'] = time.time()
    # Create Folder struct for this session
    sessionId, imagePaths = generateSessionFolder('images_store')
    # save images localy
    imageList = await localImageSave(images, imagePaths[1])
    sessionTimings['ImagesSavedLocally'] = time.time()
    # create session info
    sessionInfo = createImageInfo(imageList)
    # format images
    formatImages(imagePaths[1], imagePaths[2])
    sessionTimings['ImagesFormatted'] = time.time()
    # crop images
    sessionInfo = cropImages(imagePaths[2], imagePaths[3], imageList, sessionInfo)
    sessionTimings['ImagesCropped'] = time.time()
    # evaluate images
    sessionInfo = evaluation(imagePaths[3], sessionInfo)
    sessionTimings['ImagesEvaluated'] = time.time()
    # average results
    chosenImageNames, sessionInfo = postProcess(sessionInfo)
    # save to db
    # delete session images (not needed and can save images as is)
    #deleteSessionImages(imagePaths)

    return {
        "kiosk_id": kiosk_id,
        "uploaded_files": imageList,
        "image_Info": sessionInfo,
        "session_Timings":sessionTimings,
        "chosen_Images": chosenImageNames
        }
