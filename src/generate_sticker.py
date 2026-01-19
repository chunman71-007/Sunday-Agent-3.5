import os
import sys
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageColor

def split_text(text, max_chars_per_line=10):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) <= max_chars_per_line:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def create_sticker(style="new_year", text="Happy Meow Year", font_name="default", background="transparent", text_color="#000000", output_dir="assets/generated"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_style = "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in style.lower())
    filename = f"{safe_style}_sticker_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    width, height = 1024, 1024

    # 背景設定
    if background == "transparent":
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    elif background == "white":
        img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    elif background == "black":
        img = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    elif background == "forest":
        img = Image.new("RGBA", (width, height), (34, 139, 34, 255))
        draw = ImageDraw.Draw(img)
        for y in range(height):
            shade = int(34 + (y / height) * 100)
            draw.line([(0, y), (width, y)], fill=(shade, 139, shade, 255))
    elif background == "starry":
        img = Image.new("RGBA", (width, height), (10, 10, 40, 255))
        draw = ImageDraw.Draw(img)
        for _ in range(200):
            x, y = random.randint(0, width), random.randint(0, height)
            draw.ellipse((x, y, x+2, y+2), fill=(255, 255, 255, 255))
    elif background == "watercolor":
        img = Image.new("RGBA", (width, height), (173, 216, 230, 255))
        draw = ImageDraw.Draw(img)
        for y in range(height):
            shade = int(173 + (y / height) * 50)
            draw.line([(0, y), (width, y)], fill=(shade, 200, 230, 255))
    elif background == "smoke":
        img = Image.new("RGBA", (width, height), (200, 200, 200, 255))
        draw = ImageDraw.Draw(img)
        for y in range(height):
            shade = int(200 - (y / height) * 100)
            draw.line([(0, y), (width, y)], fill=(shade, shade, shade, 255))
    else:
        print(f"⚠️ 未知背景選項 '{background}'，改用透明背景")
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    # 嘗試載入字型
    font_path = f"fonts/{font_name}.ttf"
    print(f"=== 嘗試載入字型檔: {font_path} ===")
    if os.path.exists(font_path):
        try:
            font_large = ImageFont.truetype(font_path, 96)
            font_small = ImageFont.truetype(font_path, 48)
            print(f"✅ 成功載入字型: {font_name}")
        except Exception as e:
            print(f"⚠️ 載入字型失敗，錯誤: {e}")
            print("➡️ 改用預設字型")
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    else:
        print(f"⚠️ 找不到字型檔: {font_path}")
        print("➡️ 改用預設字型")
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 文字顏色
    try:
        color = ImageColor.getrgb(text_color)
    except Exception as e:
        print(f"⚠️ 無效文字顏色 '{text_color}'，錯誤: {e}")
        color = (0, 0, 0)

    # 標題
    title = "Sunday Agent"
    title_w, title_h = draw.textbbox((0,0), title, font=font_small)[2:]
    draw.text(((width - title_w) / 2, 80), title, fill=(120,120,120,255), font=font_small)

    # 主文字（自動分行）
    lines = split_text(text, max_chars_per_line=10)
    y = height // 2 - (len(lines) * 60)
    for line in lines:
        w, h = draw.textbbox((0,0), line, font=font_large)[2:]
        draw.text(((width - w) / 2, y), line, fill=color, font=font_large)
        y += h + 20

    # Footer
    footer = f"style: {style} • {timestamp}"
    fw, fh = draw.textbbox((0,0), footer, font=font_small)[2:]
    draw.text(((width - fw) / 2, height - fh - 80), footer, fill=(90,90,90,255), font=font_small)

    img.save(filepath, "PNG")

    print(f"貼紙已儲存至: {filepath}")
    print(f"實際收到 style: '{style}'")
    print(f"實際收到 text : '{text}'")
    print(f"使用字型: {font_name}")
    print(f"背景模式: {background}")
    print(f"文字顏色: {text_color}")

if __name__ == "__main__":
    print("=== DEBUG: sys.argv 內容 ===")
    print(sys.argv)
    style = sys.argv[1].strip() if len(sys.argv) > 1 and sys.argv[1].strip() else "new_year"
    text = sys.argv[2].strip() if len(sys.argv) > 2 and sys.argv[2].strip() else "Happy Meow Year"
    font_name = sys.argv[3].strip() if len(sys.argv) > 3 and sys.argv[3].strip() else "default"
    background = sys.argv[4].strip() if len(sys.argv) > 4 and sys.argv[4].strip() else "transparent"
    text_color = sys.argv[5].strip() if len(sys.argv) > 5 and sys.argv[5].strip() else "#000000"
    create_sticker(style=style, text=text, font_name=font_name, background=background, text_color=text_color)
