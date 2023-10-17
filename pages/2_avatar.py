import streamlit as st
from utilities.avatar import components as avatar_components
from utilities.pose import components as pose_components
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

def main():
    create_col, avatar_display_col, pose_display_col = st.columns([1, 1,1])
    with create_col:
        avatar_components.create_avatar()
    with avatar_display_col:
        avatar_components.list_avatars()
    with pose_display_col:
        pose_components.list_poses()
if __name__ == "__main__":
    main()