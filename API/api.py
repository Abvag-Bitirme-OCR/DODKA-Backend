from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
from typing import Union
import json
from PIL import Image
import io
import redis
import uvicorn
import uuid

# If you create redis please download Docker and run this command;
# docker container run --name=docker-container -d -p 6379:6379 redis

# Download this packages
# pip install fastapi "uvicorn[standard]"
# pip install pillow
# pip install python-multipart


app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

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


# File upload with RequestBody
@app.post("/file/upload")
async def create_file(file: bytes = File()):
    image_id=uuid.uuid4()
    redis_client.set(str(image_id),file,ex=900)
    result = objectToJson(Result(len(file), True, "File transfer successfuly."))
     
    return JSONResponse(content=result, status_code=200)

# Query method 1(Path Variable)
@app.post("/query(create1/{query}")
def read_item(query: str):
    
    result = objectToJson(Result(query, True, "Process succeeded."))
    
    return JSONResponse(content=result, status_code=200)

# Query method 2 (Request Param)
@app.post("/query/create2")
def read_item(q: Union[str, None] = None):

    result = objectToJson(Result(q, True, "Process succeeded."))

    return JSONResponse(content=result, status_code=200)

@app.get("/checkpoint")
def connection_checkpoint():
    if redis_client.ping():
        return JSONResponse(content="Redis connection is successfuly!",status_code=200)
    else:
        return JSONResponse(content="Redis connection is not successfuly!",status_code=500)

if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port=8000)