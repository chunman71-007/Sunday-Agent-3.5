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
            current_line += " " + word if current_line else
