import streamlit as st
import os
import base64
import tempfile
from PIL import Image
import numpy as np
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

if 'clip_width' not in st.session_state:
    st.session_state.clip_width=0
if 'clip_height' not in st.session_state:
    st.session_state.clip_height=0
if 'clip_fps' not in st.session_state:
    st.session_state.clip_fps=0
if 'clip_to_frames' not in st.session_state:
    st.session_state.clip_to_frames=0
if 'clip_duration' not in st.session_state:
    st.session_state.clip_duration=0

st.title(':black[:film_frames: GIF Converter :film_frames:]')



#uploading the file

st.sidebar.header('Upload Files')
file_upload = st.sidebar.file_uploader("Select a File.", type=['mov', 'mp4'])

st.subheader('Disclaimer')
with st.expander('Show'):
    st.markdown('''
    Welcome to the App!
    
    This app's code is inspired by the Data Professor on Youtube.
    
    :cookie: To Use this app, Drag or Drop the file in the sidebar or directly browse the file.
    
    :cookie: Check and re-arrange the parameters of the generated GIF.
    
    :cookie: Press Generate. Wait for it to finish (It may take some time.)
    
    :cookie: If you are happy with the result press download. Now, use the gif as you may!
    
    :sparkling_heart: Enjoy! :sparkling_heart:
    
    '''
    )


if file_upload is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(file_upload.read())

    clip = VideoFileClip(tfile.name)

    st.session_state.clip_duration = clip.duration

    st.sidebar.header('Input Sliders')
    resolution_scaling = st.sidebar.slider('Scale the Video Resolution.', 0.0, 1.0, 0.5)
    select_speedx = st.sidebar.slider('Playback Speed', 0.1, 10.0, 5.0)
    select_export_ran = st.sidebar.slider('Select Export Range', 0, int(st.session_state.clip_duration),(0, int(st.session_state.clip_duration)))


    clip = clip.resize(resolution_scaling)
    st.session_state.clip_width = clip.w
    st.session_state.clip_height = clip.h
    st.session_state.clip_duration = clip.duration
    st.session_state.clip_to_frames = clip.duration*clip.fps
    st.session_state.clip_fps = st.sidebar.slider('FPS', 10, 60, 20)

    st.subheader('Values')
    c1, c2, c3 ,c4, c5 = st.columns(5)
    c1.metric('Width', st.session_state.clip_width, 'pixels')
    c2.metric('Height', st.session_state.clip_height, 'pixels')
    c3.metric('Duration', st.session_state.clip_duration, 'seconds')
    c4.metric('FPS', st.session_state.clip_fps, '')
    c5.metric('Total Frames', st.session_state.clip_to_frames, 'frames')

    st.subheader('Preview')

    with st.expander('Show Results'):
        select_frame =st.slider('Preview', 0, int(st.session_state.clip_duration), int(np.median(st.session_state.clip_duration)))
        clip.save_frame('result.gif', t=select_frame)
        frame_image = Image.open('result.gif')
        st.image(frame_image)

    st.subheader('Image Parameters')
    with st.expander('Show'):
        st.write(f'File Name: `{file_upload.name}`')
        st.write('Image Size:', frame_image.size)
        st.write('Resolution Scaling', resolution_scaling)
        st.write('Speed', select_speedx)
        st.write('Export Duration', select_export_ran)
        st.write('FPS',st.session_state.clip_fps)

    st.subheader('Generate')
    generate_gif = st.button('Generate!')

    if generate_gif:
        clip = clip.subclip(select_export_ran[0], select_export_ran[1]).speedx(select_speedx)

        frames = []
        for frame in clip.iter_frames():
            frames.append(np.array(frame))

        image_list = []

        for frame in frames:
            im = Image.fromarray(frame)
            image_list.append(im)

        image_list[0].save('export.gif', format='GIF', save_all=True, loop=0, append_images=image_list)


        st.subheader('Download')

        file_temp = open('export.gif', 'rb')
        contents = file_temp.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_temp.close()
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
        )

        fsize = round(os.path.getsize('export.gif')/(1024*1024),1)
        st.info(f'File Size: {fsize} MB', icon='💾')

        fname = file_upload.name.split('.')[0]
        with open('export.gif', 'rb') as file:
            btn = st.download_button(
                label='Download',
                data=file,
                file_name=f'{fname}_scaling-{resolution_scaling}_fps-{st.session_state.clip_fps}_speed-{select_speedx}_duration-{select_export_ran[0]}-{select_export_ran[1]}.gif',
                mime = 'image/gif'
            )

else:
    st.warning('Please Upload a File.')



