from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
from typing import Union
import json
from PIL import Image
import io

#Baslarken
# pip install fastapi "uvicorn[standard]"
# pip install pillow
# pip install python-multipart


app = FastAPI()


class Result():

    data: any
    success: bool
    message: str

    def __init__(self, data:any, success:bool, message:str) -> None:
        self.data = data
        self.success = success
        self.message = message

def objectToJson(result:Result):

    data = json.dumps(result.__dict__)
    data = json.loads(data)

    return data


# Dosya Yukleme (RequestBody)
@app.post("/file")
async def create_file(file: bytes = File()):
    # -> file basta byte geliyor
    image = Image.open(io.BytesIO(file))
    image.save("ex.png") # -> dizine kayıt
    # image.show() -> gosterir
    result = objectToJson(Result(len(file), True, "Dosya Aktarma Islemi Basarili"))
     
    return JSONResponse(content=result, status_code=200)

# Kullanıcıdan Sorgu alma 1. yöntem (PathVariable)
@app.post("/createQuery/{query}")
def read_item(query: str):
    
    result = objectToJson(Result(query, True, "Islem Basarili"))
    
    return JSONResponse(content=result, status_code=200)

# Kullanıcıdan Sorgu alma 2. yöntem (RequestParams)
@app.post("/createQuery2")
def read_item(q: Union[str, None] = None):

    result = objectToJson(Result(q, True, "Islem Basarili"))

    return JSONResponse(content=result, status_code=200)

