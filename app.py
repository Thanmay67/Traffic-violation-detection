import streamlit as st
import os
import time
from PIL import Image

# --- WEBSITE CONFIGURATION ---
st.set_page_config(page_title="Traffic Violation Hub", layout="wide", page_icon="🚨")

st.title("🚨 Red-Light Violation Live Dashboard")
st.write("Real-time traffic intersection monitoring and automated evidence collection.")
st.markdown("---")

IMAGE_DIR = r"C:\Users\thanm\Desktop\IR sensor trafic violation detector"
image_path = os.path.join(IMAGE_DIR, "latest_violation.jpg")

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📸 Latest Evidence Capture")
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            st.image(img, caption="Evidence Image (Automatically pulled from enforcement phone)", use_container_width=True)
        except Exception:
            st.info("Refreshing incoming image snapshot...")
    else:
        st.warning("No violations detected yet. System is actively monitoring the stop line.")

with col2:
    st.subheader("📊 System Status & Analytics")
    st.success("● Hardware Link: Connected (COM6)")
    st.success("● Camera Status: ADB Shutter Online")
    st.markdown("---")
    st.write("**How to simulate a violation:**")
    st.caption("1. Wait for the physical traffic light to turn RED.")
    st.caption("2. Pass a model car in front of the IR sensor.")
    st.caption("3. The webpage will automatically refresh to display the evidence photo.")

time.sleep(2)
st.rerun()