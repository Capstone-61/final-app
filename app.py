import streamlit as st
import pandas as pd
import os
from moviepy.editor import VideoFileClip
from csv_integration import integrate_timestamps
from stitcher import create_summary_video
from audio import EventDetectionPipeline
# from video_module import create_video_timestamps

# from your_summarization_module import generate_summary



def create_audio_csv(video_path, output_path):
    """Create audio timestamps CSV from the video file."""
    # audio_timestamps = create_audio_timestamps(video_path)
    # audio_df = pd.DataFrame(audio_timestamps, columns=["Timestamp"])
    # audio_df.to_csv(output_path, index=False)

def create_video_timestamps(video_path):
    """Create video timestamps from the video file."""
    # video = VideoFileClip(video_path)




if __name__ == "__main__":
    # Set up the Streamlit app
    st.title("Sports Video Summarization System")

    # File input for video (compulsory)
    video_file1 = st.file_uploader("Upload the first half of a football video", type=["mp4"])

    video_file2 = st.file_uploader("Upload the second half of a football video", type=["mp4"])
    if video_file1 is None or video_file2 is None:
        st.warning("Please upload video files to proceed.")


    else:
        # File input for tweets CSV (optional)
        tweets_file = st.file_uploader("Upload an optional CSV file with tweets", type=["csv"])

        #enter the name of the match
        match_name = st.text_input("Enter the name of the match")

        if match_name is None:
            st.warning("Please enter the name of the match")

        # Run summarization when "Generate Summary" button is clicked
        if st.button("Generate Summary"):
            #check if the match has already added and timestamps of events have been generated
            if os.path.exists(match_name):
                #check if match directory contains the necessary files
                if not os.path.exists(f"{match_name}/{match_name}1_audio.csv") or not os.path.exists(f"{match_name}/{match_name}2_audio.csv") or not os.path.exists(f"{match_name}/{match_name}1_video.csv") or not os.path.exists(f"{match_name}/{match_name}2_video.csv"):
                    
                    
                    audioPipeline = EventDetectionPipeline()
                    audioPipeline.process_and_generate_csv(os.path.join(match_name, "first_half.mp4"), f"{match_name}1_audio.csv")
                    # create_audio_csv(os.path.join(match_name, f"second_half.mp4"), f"{match_name}/{match_name}2_audio.csv")
                timestamps=integrate_timestamps(match_name)


                st.video(f"{match_name}/{match_name}_summary.mp4")
            else:
                # create a directory for the match
                os.mkdir(match_name)
                # Save the uploaded video files
                with open(os.path.join(match_name, "first_half.mp4"), "wb") as f:
                    f.write(video_file1.getbuffer())
                with open(os.path.join(match_name, "second_half.mp4"), "wb") as f:
                    f.write(video_file2.getbuffer())
                
                # Generate the key timestamps CSV for each modality and save in match directory as "match_name_modality.csv"
                # audio_timestamps_1 = create_audio_timestamps(os.path.join(match_name, "first_half.mp4"))
                # audio_timestamps_2 = create_audio_timestamps(os.path.join(match_name, "second_half.mp4"))

                # video_timestamps_1 = create_video_timestamps(os.path.join(match_name, "first_half.mp4"))
                # video_timestamps_2 = create_video_timestamps(os.path.join(match_name, "second_half.mp4"))

                # twitter_timestamps = create_twitter_timestamps(tweets_file) if tweets_file else []

                # Save the timestamps in CSV files
                # audio_timestamps_1.to_csv(f"{match_name}/{match_name}1_audio.csv", index=False)
                # audio_timestamps_2.to_csv(f"{match_name}/{match_name}2_audio.csv", index=False)

                # video_timestamps_1.to_csv(f"{match_name}/{match_name}1_video.csv", index=False)
                # video_timestamps_2.to_csv(f"{match_name}/{match_name}2_video.csv", index=False)

                # if tweets_file:
                    # twitter_timestamps.to_csv(f"{match_name}/{match_name}_tweets.csv", index=False)
                
                # Generate the summary video
                # generate_summary(match_name)
                st.video(f"{match_name}/{match_name}summary.mp4")
