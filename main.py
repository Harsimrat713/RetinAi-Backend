import time
from typing import List
from fastapi import FastAPI, File, UploadFile

from evaluation import evaluation
from utilities import localImageSave, deleteSessionImages, genKey, createImageInfo, imagePaths, sessionTimings
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
    sessionInfo = evaluation(imagePaths[2], sessionInfo)
    sessionTimings['ImagesEvaluated'] = time.time()
    # average results
    chosenImageNames, sessionInfo = postProcess(sessionInfo)
    # save to db
    # delete session images
    deleteSessionImages(imagePaths)

    return {
        "kiosk_id": kiosk_id,
        "uploaded_files": imageList,
        "image_Info": sessionInfo,
        "session_Timings":sessionTimings,
        "chosen_Images": chosenImageNames
        }
