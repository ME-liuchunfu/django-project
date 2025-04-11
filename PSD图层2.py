
"""
pip install Pillow psd-tools

"""

from psd_tools import PSDImage
from psd_tools.api.layers import Group, Layer, PixelLayer
from PIL import Image, ImageDraw, ImageFont


def create_layer_with_text(psd, name, size, color, text=None, left=0, top=0):
    # 创建图层的 PIL 图像
    layer_image = Image.new('RGBA', size, color=color)
    draw = ImageDraw.Draw(layer_image)

    # 尝试加载系统字体，如果没有可用字体，则使用默认字体
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  # bbox的宽度
    text_height = bbox[3] - bbox[1]  # bbox的高度

    # 计算文本位置
    text_position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(text_position, text, fill="black", font=font)

    layer = PixelLayer.frompil(layer_image, psd_file=psd, name=name, left=left, top=top)
    return layer



def create_psd():
    # 创建一个300x200像素的白色背景的PSD画布
    psd = PSDImage.new(mode='RGBA', size=(300, 200))

    # 创建第一个图层: 淡蓝色背景
    layer1 = Image.new('RGBA', (100, 50), (173, 216, 230, 255))  # 淡蓝色
    psd.append(PixelLayer.frompil(layer1, psd_file=psd, name='Layer 1', left=0, top=0))

    # 创建第二个图层: 浅绿色背景
    layer2 = Image.new('RGBA', (100, 50), (144, 238, 144, 255))  # 浅绿色
    pixe2 = PixelLayer.frompil(layer2, psd_file=psd, name='Layer 2', left=50, top=50)
    pixe2.name = '1111'
    psd.append(pixe2)

    # 创建第三个图层: 浅灰色背景
    layer3 = Image.new('RGBA', (100, 20), (211, 211, 211, 255))  # 浅灰色
    psd.append(PixelLayer.frompil(layer3, psd_file=psd, name='Layer 3', left=150, top=0))  # 位置 (150, 0)

    # 第三个图层：浅灰色背景
    layer3 = create_layer_with_text(psd, 'Layer 4', (100, 50), (211, 211, 211, 255), text='Hello', left=150, top=50)
    psd.append(layer3)

    # 保存为PSD文件
    psd.save('output.psd')

if __name__ == '__main__':
    create_psd()
