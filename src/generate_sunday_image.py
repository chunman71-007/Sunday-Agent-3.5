import os
import requests
from datetime import datetime

# 你可以之後改用自己喜歡的模型
MODEL_ID = "stabilityai/stable-diffusion-2-1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

def generate_sunday_image(
    prompt: str,
    output_dir: str = "assets/sunday_base",
    filename_prefix: str = "sunday_cartoon"
):
    os.makedirs(output_dir, exist_ok=True)

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN 環境變數未設定")

    headers = {"Authorization": f"Bearer {hf_token}"}

    # 先用簡單 prompt，之後你可以再調整字眼
    full_prompt = (
        "cute cartoon cat named Sunday, orange and white fur, big eyes, "
        "kawaii style, clean vector flat illustration, transparent background, "
        + prompt
    )

    payload = {
        "inputs": full_prompt,
        "options": {"wait_for_model": True}
    }

    print(f"🔹 呼叫 Hugging Face 模型: {MODEL_ID}")
    for attempt in range(3):
    resp = requests.post(API_URL, headers=headers, json=payload)
    if resp.status_code == 200:
        break
    elif "model is currently loading" in resp.text:
        print("模型載入中，重試...")
        time.sleep(30)
    else:
        break
    resp = requests.post(API_URL, headers=headers, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Hugging Face API 失敗: {resp.status_code} {resp.text[:300]}"
        )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "wb") as f:
        f.write(resp.content)

    print(f"✅ Sunday 卡通圖已儲存：{filepath}")
    return filepath

if __name__ == "__main__":
    # 允許從 command line 傳入簡單描述
    import sys
    extra_prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "holiday sticker"
    generate_sunday_image(extra_prompt)
