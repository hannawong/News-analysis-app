
from PIL import Image

img = Image.open("C:\\Users\\zh-wa\\Desktop\\1.jpg")
img = img.convert('RGBA') # 修改颜色通道为RGBA
x, y = img.size # 获得长和宽

# 设置每个像素点颜色的透明度
for i in range(x):
    for k in range(y):
        color = img.getpixel((i, k))
        color = color[:-1] + (100, )
        img.putpixel((i, k), color)

img.save("tologo.png") # 要保存为.PNG格式的图片才可以