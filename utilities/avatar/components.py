import asyncio
import streamlit as st
from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os
import pandas as pd
from utilities.common import upload_file_signed_url, parse_gcp_url
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
                    extends,
                    createdAt,
                    updatedAt
                }
                }
            """)
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
async def create_avatar_func(name: str,pose_id: int):
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
            query = query.replace("#name#",str(name))
            query = query.replace("#poseid#",str(pose_id))
            query = gql(query)       
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
async def update_avatar_status_func(avatar_id: int, pose_id: int, state:str):
    try:
        transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = ("""
                mutation {
                    updateAvatarState(
                        input: { avatarId: #avatar_id#, poseId: #pose_id#, state: #state# }
                    ) {
                        status
                    }
                }
            """)
            query = query.replace("#avatar_id#",str(avatar_id))
            query = query.replace("#pose_id#",str(pose_id))
            query = query.replace("#state#",str(state))
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
                        glb_path = response["glbPath"]
                        st.write("glbPath: ",glb_path)
                        #upload glb file 
                        error, response = asyncio.run(upload_file_signed_url(file,signed_url))
                        if error is not None:
                            raise Exception(error)
                        else:
                            if response.status_code ==200:
                                #update avatar state
                                avatar_id, pose_id, _ = parse_gcp_url(glb_path, type = "avatar")
                                update_response = asyncio.run(update_avatar_status_func(avatar_id, pose_id, "glbUploaded"))
                                print(update_response)
                                try:
                                    if update_response["updateAvatarState"]["status"]==200:
                                        st.success("Create avatar successfully")
                                    else:
                                        raise Exception(f"Error update avatar state: {update_response}")
                                except:
                                    raise Exception(f"Error update avatar state: {update_response}")
                            else:
                                raise Exception(f"Can't upload glb file: {response.text}")
                            
                except Exception as error:
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
        try:
            avatar['createdAt'] = pd.to_datetime(avatar['createdAt'],format='%Y-%m-%dT%H:%M:%S.%fZ')
            avatar['updatedAt'] = pd.to_datetime(avatar['updatedAt'], format='%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            pass
        st.dataframe(avatar,hide_index=True)
    except Exception as e:
        st.write("Error fetching avatar: ",e)

    