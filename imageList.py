from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import os


class NamedImage:
    name = ''
    image = None

    def __init__(self, name, image):
        self.name = name
        self.image = image


class ImageList:

    __image_dir_path = ''
    __images = []

    def __init__(self, image_dir_path):
        self.__image_dir_path = image_dir_path

        # for each image in the directory
        for filename in os.listdir(image_dir_path):
            # if file-ending is jpg, png, gif or webp store it in the list
            file_ending = filename.split('.')[-1]
            if file_ending in ['jpg', 'png', 'gif', 'webp']:
                self.__images.append(
                    NamedImage(
                        filename,
                        Image.open('{}/{}'.format(image_dir_path, filename))
                    )
                )

    def save(self, save_dir_path=None):
        if save_dir_path is None:
            '{}/exports'.format(self.__image_dir_path)

        for named_image in self.__images:
            named_image.image.save(save_dir_path + '/' + named_image.name)

    def __apply_lambda(self, lambda_function):
        for i, named_image in enumerate(self.__images):
            named_image.image = lambda_function(named_image.image)
            self.__images[i] = named_image

    def preview(self, *, amount=1):
        for i, named_image in enumerate(self.__images):
            named_image.image.show()
            if i + 1 == amount:
                break
        return self

    def show(self):
        self.__apply_lambda(lambda image: image.show())
        return self

    def resize(self, *, width=None, height=None, remain_aspect_ratio=True):
        for i, named_image in enumerate(self.__images):
            image = named_image.image
            if width is None and height is None:
                (width, height) = image.size
            else:
                if(width is None):
                    if remain_aspect_ratio:
                        width = int(image.width * height / image.height)
                    else:
                        width = image.width
                if(height is None):
                    if remain_aspect_ratio:
                        height = int(image.height * width / image.width)
                    else:
                        height = image.height

            named_image.image = image.resize((width, height))
            self.__images[i] = named_image
        return self

    def rotate(self, degree):
        self.__apply_lambda(lambda image: image.rotate(degree))
        return self

    def to_grayscale(self):
        self.__apply_lambda(lambda image: image.convert('L'))
        return self

    def to_grayscale_with_alpha(self):
        self.__apply_lambda(lambda image: image.convert('LA'))
        return self

    def apply_threshold(self, threshold):
        self.__apply_lambda(lambda image: image.point(
            lambda p: p > threshold and 255))
        return self

    def apply_gaussian_blur(self, radius=None):
        if radius is None:
            radius = 5

        self.__apply_lambda(lambda image: image.filter(
            ImageFilter.GaussianBlur(radius=radius)))
        return self

    def apply_smoothing(self):
        self.__apply_lambda(
            lambda image: image.filter(ImageFilter.SMOOTH_MORE))
        return self

    def apply_detail(self):
        self.__apply_lambda(lambda image: image.filter(ImageFilter.DETAIL))
        return self

    def apply_find_edges(self):
        self.__apply_lambda(lambda image: image.filter(ImageFilter.FIND_EDGES))
        return self

    def sharpen(self):
        self.__apply_lambda(lambda image: image.filter(ImageFilter.SHARPEN))
        return self

    def apply_filter(self, filter):
        self.__apply_lambda(lambda image: image.filter(filter))
        return self

    # crop has the format (x, y, width, height)
    def crop(self, box):
        self.__apply_lambda(lambda image: image.crop(box))
        return self

    '''
        Submit float values greater 0

        0-1 reduces the contrast, brightness, sharpness
        1 is the original value
        above 1 increases the contrast, brightness, sharpness
    '''

    def enhance(self, *, contrast=None, brightness=None, sharpness=None):
        if contrast is not None:
            self.__apply_lambda(
                lambda image: ImageEnhance.Contrast(image).enhance(contrast))
        if brightness is not None:
            self.__apply_lambda(lambda image: ImageEnhance.Brightness(
                image).enhance(brightness))
        if sharpness is not None:
            self.__apply_lambda(
                lambda image: ImageEnhance.Sharpness(image).enhance(sharpness))
        return self

    def watermark(self, text, opacity=0.5, font_size=20, font_path=None):

        font_path = "arial.ttf" if font_path is None else font_path
        font = ImageFont.truetype(font_path, font_size)
        text_color = (
            255, 255, 255, int(255*opacity))

        for i, named_image in enumerate(self.__images):
            image = named_image.image
            imageMode = image.mode
            image = image.convert('RGBA')

            txtLayer = Image.new('RGBA', image.size, (255, 255, 255, 0))
            drawObject = ImageDraw.Draw(txtLayer)

            x, y = self.__determine_watermark_position(
                image, drawObject, text, font)

            drawObject.text((x, y), text, fill=text_color, font=font)

            image = Image.alpha_composite(image, txtLayer)
            image = image.convert(imageMode)

            named_image.image = image

            self.__images[i] = named_image
        return self

    def __determine_watermark_position(self, image, drawObject, text, font):
        width, height = image.size
        text_width, text_height = drawObject.textsize(text, font)
        x = width / 2 - text_width / 2
        y = height / 2 - text_height / 2

        return x, y
