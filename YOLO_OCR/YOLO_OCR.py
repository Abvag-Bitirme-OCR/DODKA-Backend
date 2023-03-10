import cv2
import pytesseract
import os
from PIL import Image
from roboflow import Roboflow
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# yolo
rf = Roboflow(api_key="QFwnNJwDHIDMn7u7G809")
project = rf.workspace().project("paragraph-models")
model = project.version(3).model
predictions = model.predict('YOLO_OCR/g310.jpg', confidence=40, overlap=30).json()
model.predict("YOLO_OCR/g310.jpg", confidence=40, overlap=30).save("prediction.jpg")
# image processing
image_path = os.path.join('YOLO_OCR/g310.jpg')
image = cv2.imread(image_path )
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(blur, 50, 150, apertureSize=3)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilation = cv2.dilate(edges, kernel, iterations=1)
erosion = cv2.erode(dilation, kernel, iterations=1)

# OCR
for predict in predictions["predictions"]:
    y_start = int(predict["y"]-(predict["height"]/2))
    x_start = int(predict["x"]-(predict["width"]/2))
    cropped_img = erosion[y_start:int(y_start+predict["height"]), x_start:int(x_start+predict["width"])]

    # # OCR işlemini gerçekleştirmek için pytesseract'i kullanın
    text = pytesseract.image_to_string(cropped_img, lang='tur')

    # OCR tarafından dönüştürülen metni yazdırın
    print(text, "\n\n")