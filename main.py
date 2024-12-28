import time
from typing import List
from fastapi import FastAPI, File, UploadFile, Form

from evaluation import evaluation
from utilities import localImageSave, deleteSessionImages, genKey, createImageInfo, imagePaths, sessionTimings
from format_images import formatImages
from imageCropping import cropImages

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
    # generate a key for this session
    session_key = genKey()
    # save images localy
    imageList = await localImageSave(images)
    sessionTimings['ImagesSavedLocally'] = time.time()
    # create session info
    sessionInfo = createImageInfo(imageList)
    # format images
    formatImages(imagePaths[0], imagePaths[1])
    sessionTimings['ImagesFormatted'] = time.time()
    # crop images
    sessionInfo = cropImages(imagePaths[1], imagePaths[2], imageList, sessionInfo)
    sessionTimings['ImagesCropped'] = time.time()
    # evaluate images
    # sessionInfo = await evaluation(imageList)
    # average results
    # save to db
    print(sessionInfo)
    print(sessionTimings)
    # delete session images
    # deleteSessionImages(imagePaths)

    return {
        "kiosk_id": kiosk_id, 
        "kiosk_location":kiosk_location, 
        "time_stamp":time_stamp, 
        "uploaded_files": imageList
        }
