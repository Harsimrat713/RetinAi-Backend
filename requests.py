from typing import List
from fastapi import FastAPI, File, UploadFile, Form

from evaluation import evaluation

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
    # evaluate images
    results = await evaluation(images)

    return {
        "kiosk_id": kiosk_id, 
        "kiosk_location":kiosk_location, 
        "time_stamp":time_stamp, 
        "uploaded_files": [image.filename for image in images]
        }
