import streamlit as st
from streamlit_clickable_images import clickable_images
from utilities import common
from PIL import Image
IMAGE_ERROR = Image.open("./static/image_error.png")

class ImageSelector():
    def __init__(self, title, div_style, img_style, key, border_color, thumbnails=[], images=[], shawdows=[], image_names=[]):
        self.title = title
        self.thumbnails = thumbnails
        self.images = images
        self.shadows = shawdows
        self.image_names = image_names
        self.div_style = div_style
        self.img_style = img_style
        self.key = key
        self.border_color = border_color
        # self.clicked_image = None
        self.images = [common.read_image_from_url(image) for image in self.images]
        self.shadows = [common.read_image_from_url(shadow) for shadow in self.shadows]
        self.images = [image if image != None else IMAGE_ERROR for image in self.images]
        self.shadows = [shadow if shadow != None else IMAGE_ERROR for shadow in self.shadows]
    def click_detect(self):
        with st.container():
            st.write(self.title)
            index= clickable_images(
                self.thumbnails,
                titles=self.image_names,
                div_style = self.div_style,
                img_style = self.img_style,
                key=self.key,
                border_color=self.border_color,
                )
            if type(index) == int:
                return index
            else:
                return -1
    def get_image(self):
        index = self.click_detect()
        if index != -1 and type(index) == int:
            image = self.images[index] if index < len(self.images) else None
            shadow = self.shadows[index] if index < len(self.shadows) else None
            return image, shadow
        else:
            return None, None