from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips

def mmss_to_seconds(mmss: str) -> float:
    """
    Converts a timestamp in mm:ss format to seconds.
    
    :param mmss: Timestamp in "mm:ss" format.
    :return: Time in seconds.
    """
    minutes, seconds = map(int, mmss.split("."))
    return minutes * 60 + seconds

def create_summary_video(base_video_path, timestamps, output_path):
    """
    Creates a summary video from specified time segments in the base video.

    Parameters:
        base_video_path (str): Path to the base video file.
        timestamps (list of tuples): List of (start_time, end_time) tuples in seconds.
        output_path (str): Path to save the output summary video.
    """
    # Load the base video
    base_video = VideoFileClip(base_video_path)

    timestamps_seconds= [(mmss_to_seconds(start), mmss_to_seconds(end)) for start, end in timestamps]

    # Extract video segments
    clips = [base_video.subclip(start, end) for start, end in timestamps_seconds]

    # Concatenate the segments
    summary_video = concatenate_videoclips(clips)

    # Write the summary video to file
    summary_video.write_videofile(output_path, codec="libx264")

    # Close video clips to free resources
    for clip in clips:
        clip.close()
    base_video.close()

def create_summary_video_from_two_halves(video1_path, video2_path, timestamps1, timestamps2, output_path):
    """
    Creates a single summary video by concatenating specified time segments from two halves.

    Parameters:
        video1_path (str): Path to the first half video file.
        video2_path (str): Path to the second half video file.
        timestamps1 (list of tuples): List of (start_time, end_time) tuples in mm:ss format for the first half.
        timestamps2 (list of tuples): List of (start_time, end_time) tuples in mm:ss format for the second half.
        output_path (str): Path to save the output summary video.
    """
    # Load the base videos
    video1 = VideoFileClip(video1_path)
    video2 = VideoFileClip(video2_path)

    # Convert timestamps to seconds for each half
    timestamps1_seconds = [(mmss_to_seconds(start), mmss_to_seconds(end)) for start, end in timestamps1]
    timestamps2_seconds = [(mmss_to_seconds(start), mmss_to_seconds(end)) for start, end in timestamps2]

    # Extract video segments for each half
    clips1 = [video1.subclip(start, end) for start, end in timestamps1_seconds]
    clips2 = [video2.subclip(start, end) for start, end in timestamps2_seconds]

    # Concatenate the segments from both halves
    all_clips = clips1 + clips2  # Combine clips from both halves
    summary_video = concatenate_videoclips(all_clips)

    # Write the summary video to file
    summary_video.write_videofile(output_path, codec="libx264")

    # Close video clips to free resources
    for clip in all_clips:
        clip.close()
    video1.close()
    video2.close()


# Example usage
# base_video_path = "France_vs_Croatia.mp4"
# timestamps = [('17:50', '18:10'), ('27:45', '28:05'), ('33:35', '33:55'), ('37:55', '38:15'), ('68:50', '69:05')]  # example timestamps in seconds
# output_path = "summary_video.mp4"

# create_summary_video(base_video_path, timestamps, output_path)
