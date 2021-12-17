from PIL.ImageEnhance import Brightness
from imageList import ImageList

images = ImageList('./example_images')

(images
    .resize(height=450)
    .sharpen()
    .enhance(contrast=1.3, brightness=1.05)
    .watermark('aeckerstorfer', font_size=30, opacity=0.35)
    .preview(amount=1)
    .save(save_dir_path='./exports')
 )
