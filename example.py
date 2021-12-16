from PIL.ImageEnhance import Brightness
from imageList import ImageList

images = ImageList('./example_images')

(images
    .resize(height=450)
    .preview(amount=1)
    .sharpen()
    .enhance(contrast=1.3, brightness=1.05)
    .preview(amount=1)
    .save(save_dir_path='./exports')
 )
