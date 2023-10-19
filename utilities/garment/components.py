import asyncio
import streamlit as st
from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os
import pandas as pd
from utilities.common import upload_file_signed_url, parse_gcp_url
load_dotenv()

async def list_garment_func():
    transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
    try:
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = gql("""
                query{
                garments{
                    id,
                    sboxPostId,
                    type,
                    createdAt,
                    updatedAt
                }
                }
            """)
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
async def create_garment_func(pose_id:int, avatar_id:int, type:str, sbox_post_id:int):
    try:
        transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = ("""
                mutation {
                createGarment(
                    input: { poseId: #pose_id#, avatarId: #avatar_id#, type: #type#, sboxPostId: #sbox_post_id# }
                ) {
                    status
                    id
                    signedUrl
                    glbPath
                }
                }
            """)
            query = query.replace("#pose_id#",str(pose_id))
            query = query.replace("#avatar_id#",str(avatar_id))
            query = query.replace("#type#",type)
            query = query.replace("#sbox_post_id#",str(sbox_post_id))
            query = gql(query)       
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
async def update_garment_state_func(garment_id: int, avatar_id: int, pose_id: int, state:str):
    try:
        transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = ("""
                mutation {
                    updateGarmentState(
                        input: { garmentId: #garment_id#, avatarId: #avatar_id#, poseId: #pose_id#, state: #state# }
                    ) {
                        status
                    }
                }
            """)
            query = query.replace("#garment_id#",str(garment_id))
            query = query.replace("#avatar_id#",str(avatar_id))
            query = query.replace("#pose_id#",str(pose_id))
            query = query.replace("#state#",str(state))
            query = gql(query)       
            result = await session.execute(query)
            return result            
    except Exception as e:
        return e
def create_garment():
    with st.form("create_garment"):
        st.title("Create a new garment")
        pose_id = st.text_input("Pose ID")
        avatar_id = st.text_input("Avatar ID")
        type = st.text_input("Type")
        sbox_post_id = st.text_input("Sbox Post ID")
        file = st.file_uploader("Upload GLB file", type="glb")
        submit = st.form_submit_button(label="submit")
        try:
            if submit:
                if pose_id is None or pose_id=="":
                    st.error("Pose ID cannot be empty")
                    return None
                if avatar_id is None or avatar_id=="":
                    st.error("Avatar ID cannot be empty")
                    return None
                if type is None or type=="":
                    st.error("Type cannot be empty")
                    return None
                if sbox_post_id is None or sbox_post_id=="":
                    st.error("Sbox Post ID cannot be empty")
                    return None
                if file is None:
                    st.error("GLB file cannot be empty")
                    return None
                response = asyncio.run(create_garment_func(pose_id, avatar_id, type, sbox_post_id))
                try:
                    response = response["createGarment"]
                    if response["status"] == 201:
                        signed_url = response["signedUrl"]
                        glb_path = response["glbPath"]
                        st.write("glbPath: ",response["glbPath"])
                        error, response = asyncio.run(upload_file_signed_url(file,signed_url))
                        if error is not None:
                            raise Exception(f"Error upload file: {error}")
                        else:
                            if response.status_code ==200:
                                #update garment state
                                avatar_id, pose_id, garment_id = parse_gcp_url(glb_path, type = "garment")
                                update_response = asyncio.run(update_garment_state_func(garment_id, avatar_id, pose_id, "glbUploaded"))
                                try:
                                    if update_response["updateGarmentState"]["status"]==200:
                                        print(update_response)
                                        st.success("Create garment successfully")
                                    else:
                                        raise Exception(f"Error update garment state: {update_response}")
                                except:
                                    raise Exception(f"Error update garment state: {update_response}")
                            else:
                                raise Exception(f"Error upload file: {response.text}")
                            
                except Exception as error:
                    try:
                        error = str(response.errors[0])
                    except:
                        pass
                    raise Exception(f"Error create garment: {error}")
        except Exception as e:
            st.write(e)
            pass        
def list_garments():
    st.title("List of garments")
    try:
        garment = asyncio.run(list_garment_func())["garments"]
        garment = pd.DataFrame(garment)
        if garment.empty:
            st.write("No garments found")
            return None
        garment['createdAt'] = pd.to_datetime(garment['createdAt'],format='%Y-%m-%dT%H:%M:%S.%fZ')
        garment['updatedAt'] = pd.to_datetime(garment['updatedAt'], format='%Y-%m-%dT%H:%M:%S.%fZ')
        st.dataframe(garment,hide_index=True)
    except Exception as e:
        st.write("Error fetching garment: ",e)

    