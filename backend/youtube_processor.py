import re
import os
from pathlib import Path
from typing import Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

class YouTubeProcessor:
    def __init__(self):
        self.transcript_dir = Path("data/youtube_transcript")
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_video_id(self, youtube_url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r"v=([a-zA-Z0-9_-]{11})",  # Standard watch URL
            r"youtu\.be/([a-zA-Z0-9_-]{11})",  # Short URL
            r"embed/([a-zA-Z0-9_-]{11})",  # Embed URL
        ]
        
        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                return match.group(1)
        return None
    
    def get_transcript(self, youtube_url: str) -> Tuple[bool, str]:
        """Get transcript from YouTube video"""
        try:
            video_id = self.extract_video_id(youtube_url)
            if not video_id:
                return False, "Invalid YouTube URL"
            
            # Try to get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format transcript as plain text manually instead of using TextFormatter
            transcript_text = ""
            for entry in transcript_list:
                transcript_text += entry['text'] + " "
            
            # Clean up the text
            transcript_text = transcript_text.strip()
            
            # Save transcript to file
            output_file = self.transcript_dir / f"{video_id}_transcript.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcript_text)
            
            return True, transcript_text
            
        except Exception as e:
            return False, f"Failed to get transcript: {str(e)}"
    
    def get_transcript_with_timestamps(self, youtube_url: str) -> Tuple[bool, str]:
        """Get transcript with timestamps"""
        try:
            video_id = self.extract_video_id(youtube_url)
            if not video_id:
                return False, "Invalid YouTube URL"
            
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format with timestamps
            formatted_transcript = ""
            for entry in transcript_list:
                start_time = int(entry['start'])
                minutes = start_time // 60
                seconds = start_time % 60
                timestamp = f"[{minutes:02d}:{seconds:02d}]"
                text = entry['text']
                formatted_transcript += f"{timestamp} {text}\n"
            
            # Save transcript to file
            output_file = self.transcript_dir / f"{video_id}_transcript_timestamped.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(formatted_transcript)
            
            return True, formatted_transcript
            
        except Exception as e:
            return False, f"Failed to get transcript: {str(e)}"
    
    def get_video_info(self, youtube_url: str) -> Tuple[bool, dict]:
        """Get basic video information"""
        try:
            video_id = self.extract_video_id(youtube_url)
            if not video_id:
                return False, {"error": "Invalid YouTube URL"}
            
            # Get transcript to check if available
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Calculate total duration
            if transcript_list:
                total_duration = transcript_list[-1]['start'] + transcript_list[-1]['duration']
                minutes = int(total_duration // 60)
                seconds = int(total_duration % 60)
                duration_str = f"{minutes}:{seconds:02d}"
            else:
                duration_str = "Unknown"
            
            return True, {
                "video_id": video_id,
                "duration": duration_str,
                "transcript_available": len(transcript_list) > 0,
                "transcript_length": len(transcript_list) if transcript_list else 0
            }
            
        except Exception as e:
            return False, {"error": f"Failed to get video info: {str(e)}"}

# Global instance
youtube_processor = YouTubeProcessor() 