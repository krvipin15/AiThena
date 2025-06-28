# Import necessary modules
import re
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi

## youtube_transcript_api Documentation: https://pypi.org/project/youtube-transcript-api/
## Installation: pip install pathlib youtube_transcript_api

# Define the YouTube video URL
youtube_url = "https://www.youtube.com/watch?v=y2kg3MOk1sY"

# Extract the video ID from the YouTube URL using a regular expression
video_id = re.search(r"v=([a-zA-Z0-9_-]{11})", youtube_url).group(1)

# Define the directory path where the transcript will be saved
dir_path = Path("data/youtube_transcript")
# Create the directory and any necessary parent directories if they don't already exist
dir_path.mkdir(parents=True, exist_ok=True)

# Define the full output file path for the transcript
output_file_path = dir_path / f"{video_id}_transcript.txt"

# Notify the user that the transcript retrieval is starting
print("Getting YouTube Transcript...")

try:
    # Fetch the transcript using the YouTubeTranscriptApi
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Combine all text entries from the transcript into a single string
    text = " ".join([entry['text'] for entry in transcript])

    # Write the transcript text to a file with UTF-8 encoding
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Notify the user of the successful save
    print(f"Transcript saved to: {output_file_path}")

# Handle exceptions that might occur (e.g., transcript not available)
except Exception as e:
    print(f"Failed to get transcript: {e}")
