import streamlit as st
from utilities.garment import components as garment_components
from utilities.pose import components as pose_components
from utilities.avatar import components as avatar_components
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

def main():
    create_col, garment_display_col = st.columns([1, 1])
    with create_col:
        garment_components.create_garment()
    with garment_display_col:
        garment_components.list_garments()
    pose_display_col, avatar_display_col = st.columns([1,1]) 
    with pose_display_col:
        pose_components.list_poses()
    with avatar_display_col:
        avatar_components.list_avatars()
if __name__ == "__main__":
    main()