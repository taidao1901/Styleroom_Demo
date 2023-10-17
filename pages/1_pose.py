import streamlit as st
from utilities.pose import components
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
def main():
    create_col, display_col = st.columns([1, 1])
    with create_col:
        form = components.create_pose()
    with display_col:
        components.list_poses()
if __name__ == "__main__":
    main()

