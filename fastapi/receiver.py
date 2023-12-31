from fastapi import FastAPI, File, UploadFile, Response, Form
from fastapi.responses import JSONResponse
import os
import time
import httpx

app = FastAPI()


@app.post("/")
async def upload_image(image: UploadFile = File(...), message: str = Form()):
    global save_path
    # 将上传的图片保存到本地
    file_bytes = image.file.read()
    image_path = r'./upload/images'
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    # image_name = image.filename
    # 按照当前时间戳命名图片
    image_name = 'image_' + str(int(time.time())) + '.jpg'
    save_path = os.path.join(image_path, image_name)

    image_server_url = 'http://192.168.31.80:8002/upload_image'
    image_response = httpx.post(image_server_url, files={'image': file_bytes})

    with open(save_path, 'wb') as f:
        f.write(file_bytes)
        
    with open(save_path, 'rb') as f:
        f.seek(0xF0)
        encrypted_metric = f.read(1).hex()
        print("0xF0字段为:",encrypted_metric)

    
    print('加密前信息', message)
    # 对消息进行加密
    encrypted_message = encrypt_message(message, int(encrypted_metric, 16))
    print('加密后信息', encrypted_message)

    text_server_url = 'http://192.168.31.80:8001/upload_text'
    text_response = httpx.post(text_server_url, data={'message': encrypted_message})

    text_path = r'upload/message'
    if not os.path.exists(text_path):
        os.makedirs(text_path)

    text_path = os.path.join(text_path, 'text.txt')
    with open(text_path, 'wb') as file:
        file.write(encrypted_message.encode('unicode_escape'))

    # 返回一个 JSON 响应
    return JSONResponse(content={
        'result': 'OK',
        'text_server_response': text_response.json(),
        'image_server_response': image_response.json()
        })

@app.get("/get")
def read_root():
    global save_path

    with open(save_path, 'rb') as f:
        f.seek(0xF0)
        encrypted_metric = f.read(1).hex()
        print("0xF0字段为:",encrypted_metric)
    
    with open('upload/message/text.txt', 'rb') as f:   
        text = f.read().decode('unicode_escape')
    text = "解码前：" + text + "\n" + "解码后：" + \
            decrypt_message(text, int(encrypted_metric,16))
    return Response(content=text, media_type="text/plain")

# 加密函数
def encrypt_message(message, encrypt_metric):
    encrypted_message = ''
    print("加密指标为：", hex(encrypt_metric))
    for char in message:
        encrypted_message += chr(ord(char) ^ encrypt_metric)
    return encrypted_message

# 解密函数
def decrypt_message(encrypted_message, encrypt_metric):
    decrypted_message = ''
    for char in encrypted_message:
        decrypted_message += chr(ord(char) ^ encrypt_metric)
    return decrypted_message

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.31.80", port=8000)
