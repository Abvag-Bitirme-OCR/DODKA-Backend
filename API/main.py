import base64
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Union
from PIL import Image
import io
import base64
import redis
import uvicorn

import sys
sys.path.append('.')
from YOLO_OCR import YOLO_OCR



# If you create redis please download Docker and run this command;
# docker container run --name=docker-container -d -p 6379:6379 redis

# Download this packages
# pip install fastapi "uvicorn[standard]"
# pip install pillow
# pip install python-multipart

app = FastAPI()


# Query from user (FromQuery)
@app.post("/file")
async def create_file(file_base_64: Union[str, None] = None):

    try:
        
        if file_base_64 != None:        

            #  have to escape this value 'data:image/jpeg;base64,' 
            # file_base_64 = file_base_64.split("base64,")[1]
            # # to image
            # img = Image.open(io.BytesIO(base64.decodebytes(bytes(file_base_64, "utf-8"))))
            # # save for example
            # img.save('my-image.png')
            path = "../API/my-image.jpg"
            yolo = YOLO_OCR.YoloStage()
            yolo.build(path)


            imageProcessing = YOLO_OCR.ImageProcessingStage()
            imageProcessing.build(path)

            ocr = YOLO_OCR.OCRStage()
            ocr.build(yolo.predictions, imageProcessing.erosion)



            result = {
                "data": ocr.text,
                "message":"Process is successful!",
                "success": True
            }

            return JSONResponse(content=result, status_code=200)
        else:
            result = {
                "message":"assasa Error",
                "success": False
            }
            return JSONResponse(content=result, status_code=400)
    except:
        result = {
            "message":"Unexcepted Error",
            "success": False
        }
        return JSONResponse(content=result, status_code=500)


@app.post("/createQuery")
def read_item(query: Union[str, None] = None):

    if query != None:

        result = {
            "data": query,
            "message":"Process is successful!",
            "success": True
        }

        return JSONResponse(content=result, status_code=200)

    else:

        result = {
            "message":"Query Failed!",
            "success": False
        }

        return JSONResponse(content=result, status_code=400)
    

@app.get("/")
async def connection_checkpoint():
    result = {            
            "message":"Redis connection isa successfuly!",
            "success": True
        }
    return JSONResponse(content=result ,status_code=200)

@app.get("/deneme")
async def deneme():
       try:
            path =  "g310.jpg"
            yolo = YOLO_OCR.YoloStage()
            yolo.build(path)


            imageProcessing = YOLO_OCR.ImageProcessingStage()
            imageProcessing.build(path)

            ocr = YOLO_OCR.OCRStage()
            ocr.build(yolo.predictions, imageProcessing.erosion)



            result = {
                "data": ocr.text,
                "message":"Process is successful!",
                "success": True
            }

            return JSONResponse(content=result, status_code=200)
       
       except Exception as e:
            
    
           
            result = {
                "data": "adsada",
                "message":"Process is successful!",
                "success": True
            }

            return JSONResponse(content=result, status_code=200)
           


if __name__ == '__main__':
  
    uvicorn.run(app,host="127.0.0.1",port=8000)