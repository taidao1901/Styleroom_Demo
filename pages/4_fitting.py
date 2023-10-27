import streamlit as st
from utilities.fitting import components
from PIL import Image
from utilities import common
from streamlit_clickable_images import clickable_images
from utilities.fitting.clickable_image import ImageSelector
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

shoes1 = "https://i.ibb.co/R9qRvtT/Shoes.png"
shoes1_thumbnail = "https://i.ibb.co/R9qRvtT/Shoes.png"
def main():
    left, mid, right  = st.columns([1,2,2])
    avatar_image, avatar_shadow = None, None
    top_image, top_shadow = None, None
    bottom_image, bottom_shadow = None, None
    shoes_image, shawdow_image = None, None
    components.list_avatar()
    
    with left:
        avatar, pose = st.columns([1,1])
        with avatar:
            components.show_avatar()
        with pose:
            components.show_pose()
    with right:
        components.show_top()
        components.show_bottom()
    #     shoes_image, shawdow_image = ImageSelector(
    #         title="Shoes",
    #         images = [],
    #         image_names=["shoes"],
    #         thumbnails=[],
    #         div_style = {"display": "flex", "flex-direction":"row","overflow-x": "scroll", "width": "500px"},
    #         img_style = {"margin": "10px", "height": "100px", "border":"5px solid" },
    #         border_color="red",
    #         key="shoes",
    #         ).get_image()
    with mid:
        if "viewpoint" not in st.session_state:
            st.session_state["viewpoint"] = 0
        components.show_viewpoint()
        if "viewpoint" not in st.session_state or "fitting_avatar_selected" not in st.session_state or "fitting_pose_selected" not in st.session_state:
            new_image = Image.new("RGBA", (1280 , 1976), color="red")
            components.show_image(new_image)
        avatar_image, avatar_shadow = components.get_avatar_image()
        top_image, top_shadow = components.get_top_image()
        bottom_image, bottom_shadow = components.get_bottom_image()
        if avatar_image is not None and avatar_shadow is not None:
            components.show_image(avatar_image, avatar_shadow, shoes_image, shawdow_image, bottom_image, bottom_shadow, top_image, top_shadow)
    # st.json(components.list_avatar())

if __name__ == "__main__":
    main()