from PIL import Image

img = Image.open('image.png').convert('RGBA')
width, height = img.size

for y in range(height):
    for x in range(width):
        if img.getpixel((x, y))[3] == 255:
            print(f'DRAW OUT, {x}, {height - y - 1}')
        