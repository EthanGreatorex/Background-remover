import streamlit as st
from rembg import remove
import io
from PIL import Image
import time

# Make sure the page is set to 'wide' as default
st.set_page_config(layout="wide")

# This function will remove the background from the user image
def remove_bg(user_image):
    image = Image.open(user_image)

    try:
        background_removed = remove(image)
    except Exception:
        st.error("Couldn't complete operation")
        return (True, None)
    else:
        return (False, background_removed)


# This converts a PIL image object into a set of bytes which can be downloaded
def image_byte_convert(image):
    image_buffer = io.BytesIO()
    image.save(image_buffer, format="PNG")
    image_bytes = image_buffer.getvalue()
    return image_bytes



# Main streamlit code starts here
st.header("Say Goodbye To Image Backgrounds 🥳")

github_link = 'https://www.github.com/EthanGreatorex/Background-Remover'
rembg_link = 'https://github.com/danielgatis/rembg'

st.info("The source code for this application is avaliable on my [github](%s) page." % github_link, icon="🚀")
st.info("\nHuge thanks to [rembg](%s) for creating an open-source image background removal library!" % rembg_link, icon="👏")

st.write("\nMany websites designed for removing a background from an image require login details.")
st.write("The purpose of this website is to create an easy and login-free solution.")

st.markdown("### Results Will Appear Below 👇")

# Flag to keep track of if the user has processed any images
image_completion = False

# Code for the sidebar
with st.sidebar:
    user_image = st.file_uploader(label=".", label_visibility="hidden" )

    destroy_button = st.button("Destroy Image Background")

    if destroy_button and user_image :
        flag = True
        while flag:
            with st.spinner("In Operation..."):
                flag, image = remove_bg(user_image)
                image_completion = True
            
            st.success("Completed!")

        bytes_image = image_byte_convert(image)
        
        try:
            st.download_button(
                            label="Download Result",
                            data=bytes_image,
                            key="image_bg_removed",
                            file_name="image-removed-background.png",
                            mime="image/png",
                        )
        except Exception:
            st.error("Cannot make image downloadable")
    
    elif destroy_button:
        st.error("You must upload an image first!")


# If the user has processed an image, we can display the results
if image_completion:
    st.balloons()
    st.image(image, caption="Image Result")

    st.success("Thank you for using this service!")



