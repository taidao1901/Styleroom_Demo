import requests
import asyncio
from urllib.parse import urlparse
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
   
    
