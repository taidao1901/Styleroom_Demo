import streamlit as st
from utilities.fitting import components
from PIL import Image
from utilities import common
from streamlit_clickable_images import clickable_images
from utilities.fitting.clickable_image import ImageSelector
import time
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

shoes1 = "https://i.ibb.co/R9qRvtT/Shoes.png"
shoes1_thumbnail = "https://i.ibb.co/R9qRvtT/Shoes.png"
def main():
    left, mid, right  = st.columns([1,2,2])
    avatar_image, avatar_shadow = None, None
    top_image, top_shadow = None, None
    bottom_image, bottom_shadow = None, None
    shoes_image, shawdow_image = None, None
    if "viewpoint" not in st.session_state:
        st.session_state["viewpoint"]=0
    components.list_avatar()
    # print("avatar", st.session_state["fitting_avatars"])
    with left:
        avatar, pose = st.columns([1,1])
        with avatar:
            components.show_avatar()
        with pose:
            components.show_pose()
    with right:
        components.show_hair()
        components.show_top()
        components.show_accessory()
        components.show_bottom()
        components.show_shoes()
        components.show_whole_body()
    with mid:
        # start = time.time()
        # components.show_viewpoint()
        if "viewpoint" not in st.session_state or "fitting_avatar_selected" not in st.session_state or "fitting_pose_selected" not in st.session_state:
            new_image = Image.new("RGBA", (1280 , 1976))
            components.show_image(new_image)
        avatar_image, avatar_shadow = components.get_avatar_image()
        hair_image, hair_shadow = components.get_hair_image()
        top_image, top_shadow = components.get_top_image()
        accessory_image, accessory_shadow = components.get_accessory_image()
        
        bottom_image, bottom_shadow = components.get_bottom_image()
        shoes_image, shoes_shadow = components.get_shoes_image()
        whole_body_image, whole_body_shadow = components.get_whole_body_image()
        if avatar_image is not None and avatar_shadow is not None:
            components.show_image(avatar_image, avatar_shadow, shoes_image, shoes_shadow, bottom_image, bottom_shadow, top_image, top_shadow, accessory_image, accessory_shadow, hair_image, hair_shadow, whole_body_image, whole_body_shadow)
            # st.write("Time taken to render: ", time.time() - start)
if __name__ == "__main__":
    
    main()