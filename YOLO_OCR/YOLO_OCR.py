import cv2
import pytesseract
import os
from PIL import Image
from roboflow import Roboflow
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

class YoloStage:

    def __init__(self) -> None:
        pass

    def build(self, imagePath:str):
        # yolo
        rf = Roboflow(api_key="QFwnNJwDHIDMn7u7G809")
        project = rf.workspace().project("paragraph-models")
        model = project.version(3).model
        # 'YOLO_OCR/g310.jpg'
        self.predictions = model.predict(imagePath, confidence=40, overlap=30).json()
        # 'YOLO_OCR/g310.jpg'
        model.predict(imagePath, confidence=40, overlap=30).save("prediction.jpg")

class ImageProcessingStage:
    def __init__(self) -> None:
        pass

    def build(self, imagePath):
        # image processing
        # 'YOLO_OCR/g310.jpg'
        image_path = os.path.join(imagePath)
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


# start
yolo = YoloStage()
yolo.build()

imageProcessing = ImageProcessingStage()
imageProcessing.build()

ocr = OCRStage()
ocr.build(yolo.predictions, imageProcessing.erosion)



