import os
import requests
import time
import base64
from datetime import datetime

def generate_sunday_image(
    prompt: str,
    output_dir: str = "assets/sunday_base",
    filename_prefix: str = "sunday_cartoon"
):
    os.makedirs(output_dir, exist_ok=True)

    FAL_KEY = os.getenv("FAL_KEY")  # 之後換 FAL 免費 key
    if not FAL_KEY:
        raise RuntimeError("FAL_KEY 未設定")

    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "prompt": f"cute cartoon cat named Sunday, orange fur, big blue eyes, kawaii style, transparent background, {prompt}",
            "image_size": "square_hd"
        }
    }

    print("🔹 呼叫 Fal.ai Stable Diffusion")
    resp = requests.post("https://fal.run/fal-ai/fast-sdxl", headers=headers, json=payload)
    
    if resp.status_code != 200:
        raise RuntimeError(f"Fal.ai API 失敗: {resp.status_code} {resp.text}")

    image_data = base64.b64decode(resp.json()["images"][0])
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "wb") as f:
        f.write(image_data)
    
    print(f"✅ Sunday 卡通圖已儲存：{filepath}")
    return filepath
