import requests
from urllib.parse import urlparse
import base64
import os
from PIL import Image
import streamlit as st
import aiohttp
import io
async def upload_file_signed_url(file, url:str, 
                                 headers:dict ={'Content-Type': 'application/octet-stream'}):
    try:
        response = requests.put(url,headers=headers, data=file)
        return None, response
    except Exception as e:
        return e, None
def parse_url(url):
    url = urlparse(url)
    url_split = url.path.split('/')
    return url_split
def parse_gcp_url(gcp_url: str, type: str ):
    types = ("avatar","garment")
    if type not in types:
        raise Exception(f"Invalid type. Type must be one of {types}")
    parse_urls = parse_url(gcp_url)
    # get avatar_id
    avatar_id = None
    for item in parse_urls:
        if item.startswith("avatar_"):
            avatar_id = int(item[len("avatar_"):])
    # Get pose_id
    pose_id = None
    for item in parse_urls:
        if item.startswith("pose_"):
            pose_id = int(item[len("pose_"):])
    # Get garment_id
    garment_id = None
    for item in parse_urls:
        if item.startswith("garment_"):
            garment_id = int(item[len("garment_"):])
    # Check valid result
    if avatar_id is None or pose_id is None:
        raise Exception("Can't find avatar_id or pose_id")
    if type == "garment" and garment_id is None:
        raise Exception("Can't find garment_id")
     
    return avatar_id, pose_id, garment_id
def paste_image(background, image, position= (0,0)):
    image = image.convert("RGBA")
    background.paste(image, position, mask=image)
    return background
@st.cache_data(ttl=3600)
def read_image_as_base64(image_path:str):
    extension = os.path.splitext(image_path)[1]
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/{extension};base64,{encoded_string}"
@st.cache_data(ttl=3600)
def read_image_from_url(url:str):
    try:
        image = Image.open(requests.get(url, stream = True).raw)
        return image
    except Exception as e:
        print(e)
        return None
@st.cache_resource(ttl=3600)
async def read_image_from_url_async(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    return image
                else:
                    print(f"Failed to fetch image: {response.status}")
                    return None
    except Exception as e:
        print(e)
        return None