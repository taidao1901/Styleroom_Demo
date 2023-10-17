import asyncio
import streamlit as st
from dotenv import load_dotenv
from gql import gql, Client
# from gql.transport.exceptions import TransportQueryError
from gql.transport.aiohttp import AIOHTTPTransport
import os
import pandas as pd
from utilities.common import upload_file_signed_url
load_dotenv()

async def list_avatar_func():
    transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
    try:
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = gql("""
                query{
                avatars{
                    id,
                    name,
                    userId,
                    extendes,
                    createdAt,
                    updatedAt
                }
                }
            """)
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
async def create_avatar_func(name,pose_id):
    try:
        transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = ("""
                mutation {
                createAvatar(
                    input: { name: "#name#", poseId: #poseid# }
                ) {
                    status
                    id
                    signedUrl
                    glbPath
                }
                }
            """)
            query = query.replace("#name#",name)
            query = query.replace("#poseid#",pose_id)
            query = gql(query)       
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
def create_avatar():
    with st.form("create_avatar"):
        st.title("Create a new avatar")
        name = st.text_input("Name")
        pose_id = st.text_input("Pose ID")
        file = st.file_uploader("Upload GLB file", type="glb")
        submit = st.form_submit_button(label="submit")
        try:
            if submit:
                if name is None or name =="":
                    st.error("Name cannot be empty")
                    return None
                if pose_id is None or pose_id =="":
                    st.error("Pose ID cannot be empty")
                    return None
                if file is None:
                    st.error("GLB file cannot be empty")
                    return None
                response = asyncio.run(create_avatar_func(name,pose_id))
                try:
                    response = response["createAvatar"]
                    if response["status"] == 201:
                        signed_url = response["signedUrl"]
                        st.write("glbPath: ",response["glbPath"])
                        error, response = asyncio.run(upload_file_signed_url(file,signed_url))
                        if error is not None:
                            raise Exception(error)
                        else:
                            if response.status_code ==200:
                                st.success("Create avatar successfully")
                            else:
                                raise Exception(error)
                            
                except Exception as error:
                    print("lol")
                    try:
                        error = str(response.errors[0])
                    except:
                        pass
                    raise Exception("Error upload file: ",error)
        except Exception as e:
            st.write(e)
            pass        
def list_avatars():
    st.title("List of Avatars")
    try:
        avatar = asyncio.run(list_avatar_func())["avatars"]
        avatar = pd.DataFrame(avatar)
        if avatar.empty:
            st.write("No avatars found")
            return None
        avatar['createdAt'] = pd.to_datetime(avatar['createdAt'],format='%Y-%m-%dT%H:%M:%S.%fZ')
        avatar['updatedAt'] = pd.to_datetime(avatar['updatedAt'], format='%Y-%m-%dT%H:%M:%S.%fZ')
        st.dataframe(avatar,hide_index=True)
    except Exception as e:
        st.write("Error fetching avatar: ",e)

    