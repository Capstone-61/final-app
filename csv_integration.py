import os
import pandas as pd
from moviepy.editor import VideoFileClip, concatenate_videoclips
from typing import List, Tuple
from stitcher import create_summary_video_from_two_halves

def mmss_to_seconds(mmss: str) -> float:
    """Converts a timestamp in mm:ss format to seconds."""
    minutes, seconds = map(float, mmss.split("."))
    return minutes * 60 + seconds

def seconds_to_mmss(seconds: float) -> str:
    """Converts a time in seconds to mm:ss format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}.{seconds:02}"

def load_timestamps(match_name: str, half: int) -> List[Tuple[List[str], str]]:
    modality_timestamps = []
    match_folder = os.path.join(match_name)
    half_suffix = f"{half}_"

    for filename in os.listdir(match_folder):
        if filename.endswith(".csv") and filename.startswith(f"{match_name}{half_suffix}"):
            modality = filename.split('_')[-1].split('.')[0]  # Extract modality from filename
            filepath = os.path.join(match_folder, filename)
            df = pd.read_csv(filepath)
            df['Timestamp'] = df['Timestamp'].astype(str).str.replace(r'\.00$', '', regex=True)
            
            # Adjust timestamp for second half
            if half == 2 and "video" in modality:
                df['Timestamp'] = df['Timestamp'].apply(lambda t: seconds_to_mmss(mmss_to_seconds(t) - 45 * 60))
            
            modality_timestamps.append((df['Timestamp'].astype(str).tolist(), modality))
    
    return modality_timestamps

def cluster_events(modality_timestamps: List[Tuple[List[str], str]], time_window: float) -> List[Tuple[List[float], List[str]]]:
    all_timestamps = [
        (mmss_to_seconds(timestamp), modality)
        for timestamps, modality in modality_timestamps
        for timestamp in timestamps
    ]
    all_timestamps.sort()

    clusters = []
    current_cluster = [all_timestamps[0][0]]
    current_modalities = [all_timestamps[0][1]]

    for timestamp, modality in all_timestamps[1:]:
        if timestamp - current_cluster[-1] <= time_window:
            current_cluster.append(timestamp)
            current_modalities.append(modality)
        else:
            clusters.append((current_cluster, current_modalities))
            current_cluster = [timestamp]
            current_modalities = [modality]
    clusters.append((current_cluster, current_modalities))

    return clusters

def assign_weights(clusters: List[Tuple[List[float], List[str]]], modality_priority: dict) -> List[dict]:
    weighted_events = []
    for cluster, modalities in clusters:
        weight = sum(modality_priority.get(mod, 0) for mod in set(modalities))
        avg_timestamp = sum(cluster) / len(cluster)
        weighted_events.append({
            "timestamp": avg_timestamp,
            "weight": weight,
            "duration": 20 + (weight - 1) * 2
        })

    return weighted_events

def sort_by_weight(events: List[dict]) -> List[dict]:
    return sorted(events, key=lambda x: x["weight"], reverse=True)

def select_events_for_summary(events: List[dict], number_of_events: int) -> List[Tuple[float, float]]:
    selected_events = []
    for event in events[:number_of_events]:
        start_time = max(0, event['timestamp'] - (event['duration'] / 2))
        end_time = event['timestamp'] + (event['duration'] / 2)
        selected_events.append((start_time, end_time))

    return selected_events

def integrate_timestamps(match_name: str, time_window: float=90, number_of_events: int=10) -> List[Tuple[str, str]]:
    modality_priority = {'video': 5, 'audio': 2, 'tweets': 1}
    all_summary_events = []
    
    for half in [1, 2]:
        modality_timestamps = load_timestamps(match_name, half)
        clusters = cluster_events(modality_timestamps, time_window)
        # print(clusters)
        weighted_events = assign_weights(clusters, modality_priority)
        sorted_events = sort_by_weight(weighted_events)
        # print(sorted_events)
        summary_events = select_events_for_summary(sorted_events, number_of_events // 2)
        
        #sort by start time
        summary_events.sort(key=lambda x: x[0])
        all_summary_events.extend(summary_events)


    return [(seconds_to_mmss(start), seconds_to_mmss(end)) for start, end in all_summary_events]

def create_summary_video_from_two_halves(video1_path, video2_path, timestamps1, timestamps2, output_path):
    video1 = VideoFileClip(video1_path)
    video2 = VideoFileClip(video2_path)

    timestamps1_seconds = [(mmss_to_seconds(start), mmss_to_seconds(end)) for start, end in timestamps1]
    timestamps2_seconds = [(mmss_to_seconds(start), mmss_to_seconds(end)) for start, end in timestamps2]

    clips1 = [video1.subclip(start, end) for start, end in timestamps1_seconds]
    clips2 = [video2.subclip(start, end) for start, end in timestamps2_seconds]

    all_clips = clips1 + clips2
    summary_video = concatenate_videoclips(all_clips)

    summary_video.write_videofile(output_path, codec="libx264")

    for clip in all_clips:
        clip.close()
    video1.close()
    video2.close()

# Example usage
if __name__ == "__main__":
    match_name = "Port_vs_Spain"
    print(f"Generating summary for match: {match_name}")
    time_window = 90.0
    number_of_events = 10

    summary = integrate_timestamps(match_name, time_window, number_of_events)

    video1_path = f"{match_name}_1.mp4"
    video2_path = f"{match_name}_2.mp4"
    output_path = f"{match_name}_summary.mp4"

    half1_timestamps = summary[:number_of_events // 2]
    half2_timestamps = summary[number_of_events // 2:]

    create_summary_video_from_two_halves(video1_path, video2_path, half1_timestamps, half2_timestamps, output_path)
