# imageServer.py
from fastapi import FastAPI, UploadFile, File
import os
import time

app = FastAPI()

@app.post("/upload_image")
async def upload_image(image: UploadFile = File(...)):
    print("Received image")
    # 处理和存储图片信息
    image_bytes = await image.read()
    image_path = './image_server'
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    image_name = f'image_{int(time.time())}.jpg'
    save_path = os.path.join(image_path, image_name)
    with open(save_path, 'wb') as f:
        f.write(image_bytes)

    return {"result": "Image received"}

# 运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.31.80", port=8002)
