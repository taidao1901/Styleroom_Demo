import streamlit as st
from typing import List
import os
from PIL import Image
import asyncio
from utilities import common
from utilities.avatar.components import list_avatar_func
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from utilities.fitting.clickable_image import ImageSelector
from dotenv import load_dotenv
import asyncio

load_dotenv()

def show_image(*args):
    if args  != None:
        width, height = args[0].size
    image = Image.new("RGBA", (width, height))
    for arg in args:
        if arg != None :
            image = common.paste_image(image, arg)
    st.image(image, use_column_width=True)
    
async def search_avatar_func(**kwargs):
    is_activate = kwargs["is_activate"] if "is_activate" in kwargs else None
    name = kwargs["name"] if "name" in kwargs else None
    avatar_id = kwargs["avatar_id"] if "avatar_id" in kwargs else None
    pose = kwargs["pose"] if "pose" in kwargs else None
    
    arg = ""
    arg += "isActivate: "+str(is_activate).lower()+"," if is_activate != None else ""
    arg += "name: "+str(name)+"," if name != None else ""
    arg += "avatarId: "+str(avatar_id)+"," if avatar_id != None else ""
    arg += "pose: "+str(pose)+"," if pose != None else ""
    
    transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
    try:
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query =("""
                query{
                    searchAvatars(input:{ #kwargs#}){
                        status
                        id
                        name
                        poses{
                        id
                        name
                        }
                        thumbnail
                        shadows {
                            d0
                            d45
                            d90
                            d135
                            d180
                            d225
                            d270
                            d315
                        }
                        objects {
                            d0
                            d45
                            d90
                            d135
                            d180
                            d225
                            d270
                            d315
                        }
                    }
                }
            """)
            query = query.replace("#kwargs#",arg)
            query = gql(query)
            
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
async def search_avatars(avatar_ids: List[int]):
    avatars = [search_avatar_func(avatar_id=avatar_id) for avatar_id in avatar_ids]
    return await asyncio.gather(*avatars)
async def search_garment_func(**kwargs):
    is_activate = kwargs["is_activate"] if "is_activate" in kwargs else None
    garment_id = kwargs["garment_id"] if "garment_id" in kwargs else None
    avatar_id = kwargs["avatar_id"] if "avatar_id" in kwargs else None
    pose_id = kwargs["pose_id"] if "pose_id" in kwargs else None
    
    arg = ""
    arg += "isActive: "+str(is_activate).lower()+"," if is_activate != None else ""
    arg += "garmentId: "+str(garment_id)+"," if garment_id != None else ""
    arg += "avatarId: "+str(avatar_id)+"," if avatar_id != None else ""
    arg += "poseId: "+str(pose_id)+"," if pose_id != None else ""
    try:
        transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = ("""
                # Write your query or mutation here
                query{
                searchGarments(input: { #arg#}){
                        status
                        id
                        type
                        thumbnail
                        sboxPostId
                        objects{
                            d0
                            d45
                            d90
                            d135
                            d180
                            d225
                            d270
                            d315
                        }
                        shadows{
                            d0
                            d45
                            d90
                            d135
                            d180
                            d225
                            d270
                            d315
                        }
                        createdAt
                        updatedAt
                    }
                }
            """)
            query = query.replace("#arg#",arg)
            
            query = gql(query)       
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
def search_garment(avatar_id: int, pose_id: int, is_activate: bool):
    try: 
        if "search_garment" not in st.session_state:
            st.session_state["search_garment"] ={}
        if f"{avatar_id}_{pose_id}" not in st.session_state["search_garment"]:
            response = asyncio.run(search_garment(avatar_id, pose_id, is_activate=is_activate))
            garments = response["searchGarments"]
            st.session_state["search_garment"][f"{avatar_id}_{pose_id}"] ={}
            st.session_state["search_garment"][f"{avatar_id}_{pose_id}"]["top"] = [garment for garment in garments if garment["type"] == "top"]
            st.session_state["search_garment"][f"{avatar_id}_{pose_id}"]["bottom"] = [garment for garment in garments if garment["type"] == "bottom"]
            st.session_state["search_garment"][f"{avatar_id}_{pose_id}"]["shoes"] = [garment for garment in garments if garment["type"] == "shoes"]
            st.session_state["search_garment"][f"{avatar_id}_{pose_id}"]["hair"] = [garment for garment in garments if garment["type"] == "hair"]
            st.session_state["search_garment"][f"{avatar_id}_{pose_id}"]["accessories"] = [garment for garment in garments if garment["type"] == "accessories"]
        
    except Exception as e:
        st.write(e)
        return
    

def list_avatar():
    avatars = asyncio.run(list_avatar_func())["avatars"]
    id_list = [avatar["id"] for avatar in avatars]
    avatars = asyncio.run(search_avatars(id_list))
    result  = []
    for avatar in avatars:
        search_avatar = avatar["searchAvatars"][0]
        if search_avatar["status"] == 200:
            data = {
                "id": search_avatar["id"],
                "name": search_avatar["name"],
                "poses": search_avatar["poses"],
                "thumbnail": search_avatar["thumbnail"],
            }
            result.append(data)
    st.session_state["fitting_avatars"] = result
def show_avatar():
    thumbnails = [avatar["thumbnail"] for avatar in st.session_state["fitting_avatars"]]
    image_names = [avatar["name"] for avatar in st.session_state["fitting_avatars"]]
    if "fitting_avatar_selector" not in st.session_state:
        st.session_state["fitting_avatar_selector"] =  ImageSelector(
        title="Avatar",
        image_names=image_names,
        thumbnails=thumbnails,
        div_style = {"display": "flex","flex-direction": "column","overflow-y": "scroll", "height": "450px", "width": "120px"},
        img_style = {"margin": "10px", "height": "100px", "border":"5px solid" },
        border_color="red",
        key="avatar",             
        )
        
    index = st.session_state["fitting_avatar_selector"].click_detect()
    if index == -1:
        st.stop()
    # Reset pose selector
    # Reset avatar selected
    if "fitting_avatar_selected" not in st.session_state or st.session_state["fitting_avatar_selected"] != index:
        st.session_state["fitting_avatar_selected"] = index
        if "fitting_pose_selector" in st.session_state:
            del st.session_state["fitting_pose_selector"]
        if "fitting_pose_selected" in st.session_state:
            del st.session_state["fitting_pose_selected"]
    st.write(st.session_state["fitting_avatar_selected"])
def show_pose():
    poses = st.session_state["fitting_avatars"][st.session_state["fitting_avatar_selected"]]["poses"]
    st.session_state["fitting_poses"] = poses
    thumbnails = [st.session_state["fitting_avatars"][st.session_state["fitting_avatar_selected"]]["thumbnail"]]
    image_names =[pose["name"] for pose in poses]
    
    if "fitting_pose_selector" not in st.session_state or st.session_state["fitting_pose_selector"] is None:
        st.session_state["fitting_pose_selector"] = ImageSelector(
        title="Pose",
        image_names = [image_names],
        thumbnails=[thumbnails],
        div_style = {"display": "flex","flex-direction": "column","overflow-y": "scroll", "height": "450px", "width": "120px"},
        img_style = {"margin": "10px", "height": "100px", "border":"5px solid" },
        border_color="red",
        key="pose",
        )
        
    index = st.session_state["fitting_pose_selector"].click_detect()
    if index == -1:
        st.stop()
    if "fitting_pose_selected" not in st.session_state or st.session_state["fitting_pose_selected"] != index:
        st.session_state["fitting_pose_selected"] = index
    # reset garment selector
def show_viewpoint():
    viewpoint = st.radio("Viewpoint", [0,45,90,135,180,225,270,315], index=0, horizontal=True)
    if "viewpoint" not in st.session_state or st.session_state["viewpoint"] != viewpoint:
        st.session_state["viewpoint"] = viewpoint
def get_avatar_image():
    avatar_id = st.session_state["fitting_avatars"][st.session_state["fitting_avatar_selected"]]["id"]
    pose_id = st.session_state["fitting_poses"][st.session_state["fitting_pose_selected"]]["id"]
    avatar = asyncio.run(search_avatar_func(avatar_id=avatar_id, pose_id = pose_id))["searchAvatars"][0]
    viewpoint = st.session_state["viewpoint"]
    avatar_image = common.read_image_from_url(avatar["objects"]["d"+str(viewpoint)])
    avatar_shadow = common.read_image_from_url(avatar["shadows"]["d"+str(viewpoint)])
    return avatar_image, avatar_shadow
    
def show_top(avatar_id: int, pose_id: int):
    if "search_garment" not in st.session_state and f"{avatar_id}_{pose_id}" not in st.session_state["search_garment"]:
        search_garment(avatar_id, pose_id, is_activate=True)
            
    tops = st.session_state["search_garment"][f"{avatar_id}_{pose_id}"]["top"]  
    thumbnails = [top["thumbnail"] for top in tops]

    image_names = []
    if "fitting_top_selector" not in st.session_state:
        st.session_state["fitting_top_selector"] = ImageSelector(
        title="Top",
        image_names= image_names,
        thumbnails=thumbnails,
        div_style = {"display": "flex", "flex-direction":"row","overflow-x": "scroll", "width": "500px"},
        img_style = {"margin": "10px", "height": "100px", "border":"5px solid" },
        border_color="red",
        key="bar",
        )
    index = st.session_state["fitting_top_selector"].click_detect()
    if index == -1:
        if "fitting_top_selected" in st.session_state:
            del st.session_state["fitting_top_selected"]
    elif "fitting_top_selected" not in st.session_state or st.session_state["fitting_top_selected"] != index:
        st.session_state["fitting_top_selected"] = index
def get_top_image():
    images = [
        "https://storage.googleapis.com/asset-service/garment/garment_2/avatar_1/pose_3/rendered/#viewpoint#/processed/object.png",
        "https://storage.googleapis.com/asset-service/garment/garment_3/avatar_1/pose_3/rendered/#viewpoint#/processed/object.png",
        "https://storage.googleapis.com/asset-service/garment/garment_4/avatar_1/pose_3/rendered/#viewpoint#/processed/object.png"
    ]
    shadows = [
        "https://storage.googleapis.com/asset-service/garment/garment_2/avatar_1/pose_3/rendered/#viewpoint#/raw/shadow.png",
        "https://storage.googleapis.com/asset-service/garment/garment_3/avatar_1/pose_3/rendered/#viewpoint#/raw/shadow.png",
        "https://storage.googleapis.com/asset-service/garment/garment_4/avatar_1/pose_3/rendered/#viewpoint#/raw/shadow.png"
    ]
    viewpoint = st.session_state["viewpoint"]
    if "fitting_top_selected" not in st.session_state:
        return None, None
    index = st.session_state["fitting_top_selected"]
    image= common.read_image_from_url(images[index].replace("#viewpoint#", str(viewpoint)))
    shadow= common.read_image_from_url(shadows[index].replace("#viewpoint#", str(viewpoint)))
    return image, shadow
def show_bottom():
    thumbnails = [
        "https://storage.googleapis.com/asset-service/garment/garment_5/avatar_1/pose_3/rendered/0/processed/thumbnail.png",
        "https://storage.googleapis.com/asset-service/garment/garment_6/avatar_1/pose_3/rendered/0/processed/thumbnail.png",
        "https://storage.googleapis.com/asset-service/garment/garment_7/avatar_1/pose_3/rendered/0/processed/thumbnail.png"
    ]
    image_names = ["Quan1", "Quan2", "Quan3"]
    if "fitting_bottom_selector" not in st.session_state:
        st.session_state["fitting_bottom_selector"] = ImageSelector(
        title="Bottom",
        image_names=image_names,
        thumbnails=thumbnails,
        div_style = {"display": "flex", "flex-direction":"row","overflow-x": "scroll", "width": "500px"},
        img_style = {"margin": "10px", "height": "100px", "border":"5px solid" },
        border_color="red",
        key="bottom",
        )
    index = st.session_state["fitting_bottom_selector"].click_detect()
    if index == -1:
        if "fitting_bottom_selected" in st.session_state:
            del st.session_state["fitting_bottom_selected"]
    elif "fitting_bottom_selected" not in st.session_state or st.session_state["fitting_bottom_selected"] != index:
        st.session_state["fitting_bottom_selected"] = index
def get_bottom_image():
    images = [
        "https://storage.googleapis.com/asset-service/garment/garment_5/avatar_1/pose_3/rendered/#viewpoint#/processed/object.png",
        "https://storage.googleapis.com/asset-service/garment/garment_6/avatar_1/pose_3/rendered/#viewpoint#/processed/object.png",
        "https://storage.googleapis.com/asset-service/garment/garment_7/avatar_1/pose_3/rendered/#viewpoint#/processed/object.png"
    ]
    shadows = [
        "https://storage.googleapis.com/asset-service/garment/garment_5/avatar_1/pose_3/rendered/#viewpoint#/raw/shadow.png",
        "https://storage.googleapis.com/asset-service/garment/garment_6/avatar_1/pose_3/rendered/#viewpoint#/raw/shadow.png",
        "https://storage.googleapis.com/asset-service/garment/garment_7/avatar_1/pose_3/rendered/#viewpoint#/raw/shadow.png"
    ]
    viewpoint = st.session_state["viewpoint"]
    if "fitting_bottom_selected" not in st.session_state:
        return None, None
    index = st.session_state["fitting_bottom_selected"]
    image= common.read_image_from_url(images[index].replace("#viewpoint#", str(viewpoint)))
    shadow= common.read_image_from_url(shadows[index].replace("#viewpoint#", str(viewpoint)))
    return image, shadow
    
    
    
