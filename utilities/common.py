import requests
import asyncio

async def upload_file_signed_url(file, url:str, 
                                 headers:dict ={'Content-Type': 'application/octet-stream'}):
    try:
        response = requests.put(url,headers=headers, data=file)
        return None, response
    except Exception as e:
        return e, None