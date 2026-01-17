import os
import sys
from datetime import datetime

def create_sticker(style="new_year", text="Happy Meow Year", output_dir="assets/generated"):
os.makedirs(output_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
# 檔名用 style 作 prefix，安全處理特殊字元
safe_style = "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in style.lower())
filename = f"{safe_style}_sticker_{timestamp}.txt"
filepath = os.path.join(output_dir, filename)

content = f"""
🐱 Sunday Agent 貼紙生成器
樣式: {style}
文字: {text}
時間: {timestamp}
"""

with open(filepath, "w", encoding="utf-8") as f:
f.write(content.strip())

# Debug 輸出（log 會見到）
print(f"貼紙已儲存至: {filepath}")
print(f"實際收到 style: '{style}'")
print(f"實際收到 text : '{text}'")
print("Generated file content preview:")
print(content.strip())

if __name__ == "__main__":
print("=== DEBUG: sys.argv 內容 ===")
print(sys.argv) # 超重要！讓你見到到底傳咗乜

# 安全取參數
style = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "new_year"
text = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else "Happy Meow Year"

create_sticker(style=style, text=text)
