import base64
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Union
from PIL import Image
import io
import base64





#Started
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
            file_base_64 = file_base_64.split("base64,")[1]
            # to image
            img = Image.open(io.BytesIO(base64.decodebytes(bytes(file_base_64, "utf-8"))))
            # save for example
            img.save('my-image.png')

            result = {
                "data": len(file_base_64),
                "message":"Islem Basarili Bir Sekilde Gerceklesti",
                "success": True
            }

            return JSONResponse(content=result, status_code=200)
        else:
            result = {
                "data": "",
                "message":"Base64 Alinamadi",
                "success": False
            }
            return JSONResponse(content=result, status_code=400)
    except:
        result = {
            "data": "",
            "message":"Bir Hata Ile Karsilasildi",
            "success": False
        }
        return JSONResponse(content=result, status_code=500)

# Kullanıcıdan Sorgu alma 1. yöntem (PathVariable)
@app.post("/createQuery/{query}")
def read_item(query: str):

    if query != None:

        result = {
            "data": query,
            "message":"Islem Basarili Bir Sekilde Gerceklesti",
            "success": True
        }

        return JSONResponse(content=result, status_code=200)

    else:

        result = {
            "data": "",
            "message":"Query Alinamadi",
            "success": False
        }

        return JSONResponse(content=result, status_code=400)



# Kullanıcıdan Sorgu alma 2. yöntem (RequestParams)
@app.post("/createQuery2")
def read_item(query: Union[str, None] = None):

    if query != None:

        result = {
            "data": query,
            "message":"Islem Basarili Bir Sekilde Gerceklesti",
            "success": True
        }

        return JSONResponse(content=result, status_code=200)

    else:

        result = {
            "data": "",
            "message":"Query Alinamadi",
            "success": False
        }

        return JSONResponse(content=result, status_code=400)
