# textServer.py
from fastapi import FastAPI, Form
import os

app = FastAPI()

@app.post("/upload_text")
async def upload_text(message: str = Form(...)):
    print("Received message:", message)
    
    text_server_path = './text_server'
    if not os.path.exists(text_server_path):
        os.makedirs(text_server_path)

    text_server_path = os.path.join(text_server_path, 'text.txt')
    # 处理和存储文本信息
    with open(text_server_path, 'wb') as f:
        f.write(message.encode('unicode_escape'))

    return {"result": "Text received"}

# 运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.31.80", port=8001)
