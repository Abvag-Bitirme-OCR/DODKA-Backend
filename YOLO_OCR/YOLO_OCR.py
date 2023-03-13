import cv2
import pytesseract
import os
from PIL import Image
from roboflow import Roboflow
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'





import base64
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Union
from PIL import Image
import io
import base64
import redis
import uvicorn

app = FastAPI()


class YoloStage:

    def __init__(self) -> None:
        pass

    def build(self, path):
        # yolo
        rf = Roboflow(api_key="QFwnNJwDHIDMn7u7G809")
        project = rf.workspace().project("paragraph-models")
        model = project.version(3).model
        # 'YOLO_OCR/g310.jpg'
        self.predictions = model.predict(path, confidence=40, overlap=30).json()
        # 'YOLO_OCR/g310.jpg'
        model.predict(path, confidence=40, overlap=30).save("prediction.jpg")

class ImageProcessingStage:
    def __init__(self) -> None:
        pass

    def build(self, path):
        # image processing
        # 'YOLO_OCR/g310.jpg'
        image_path = os.path.join(path)
        image = cv2.imread(image_path )
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.Canny(blur, 50, 150, apertureSize=3)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilation = cv2.dilate(edges, kernel, iterations=1)
        self.erosion = cv2.erode(dilation, kernel, iterations=1)

        
class OCRStage:
    def __init__(self) -> None:
        pass

    def build(self, predictions, erosion):
        # OCR
        for predict in predictions["predictions"]:
            y_start = int(predict["y"]-(predict["height"]/2))
            x_start = int(predict["x"]-(predict["width"]/2))
            cropped_img = erosion[y_start:int(y_start+predict["height"]), x_start:int(x_start+predict["width"])]

            # # OCR işlemini gerçekleştirmek için pytesseract'i kullanın
            self.text = pytesseract.image_to_string(cropped_img, lang='tur')

            # OCR tarafından dönüştürülen metni yazdırın
            print(self.text, "\n\n")


# # start
# yolo = YoloStage()
# yolo.build("g310.jpg")

# imageProcessing = ImageProcessingStage()
# imageProcessing.build("g310.jpg")

# ocr = OCRStage()
# ocr.build(yolo.predictions, imageProcessing.erosion)



@app.get("/deneme")
async def deneme():
       try:
            # start
            yolo = YoloStage()
            yolo.build("g310.jpg")

            imageProcessing = ImageProcessingStage()
            imageProcessing.build("g310.jpg")

            ocr = OCRStage()
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