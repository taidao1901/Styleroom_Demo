import asyncio
import streamlit as st
from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os
from datetime import datetime
import pandas as pd

load_dotenv()

async def list_poses_func():
    transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
    try:
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = gql("""
                query {
                    poses{
                        id,
                        createdAt,
                        updatedAt,
                        name
                    }
                }
            """)
            result = await session.execute(query)
            return result
    except Exception as e:
        return e
async def create_pose_func(name):
    transport = AIOHTTPTransport(url=os.environ.get("STYLEROOM_URL"))
    try:
        async with Client(
            transport=transport, fetch_schema_from_transport=True,
        ) as session:
            query = gql("""
                mutation($input: CreatePoseInput!){
                    createPose(input: $input){
                    status,
                    id,
                    name
                }
                }
            """)
            result = await session.execute(query, variable_values={"input":{"name": name}})
            return result
    except Exception  as e:
        return e
def list_poses():
    st.title("List of poses")
    try:
        
        poses = asyncio.run(list_poses_func())["poses"]
        poses = pd.DataFrame(poses)
        try:
            poses['createdAt'] = pd.to_datetime(poses['createdAt'],format='%Y-%m-%dT%H:%M:%S.%fZ')
            poses['updatedAt'] = pd.to_datetime(poses['updatedAt'], format='%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            pass
        st.dataframe(poses,hide_index=True)
    except Exception as e:
        st.write("Error fetching poses", e)
        return None
def create_pose():
    with st.form(key="create_pose", clear_on_submit=True):
        st.title("Create a new pose")
        name = st.text_input("Name")
        submit = st.form_submit_button("Submit")
        try:
            if submit:
                #check empty
                if name is None or name == "":
                    st.error("Name cannot be empty")
                    return None
                #check exist
                pose_existed =  asyncio.run(list_poses_func())["poses"]
                pose_existed = pd.DataFrame(pose_existed)
                check_existed = pose_existed['name'].isin([name]).any()
                if check_existed:
                    st.error("Pose already existed")
                    return None
                response = asyncio.run(create_pose_func(name))["createPose"]
                if response['status']== 201:
                    st.success("Pose created successfully")
                else:
                    st.error("Pose created failed")
                return None
        except Exception as e:
            st.write("Error creating pose: ", e)
            return None                   