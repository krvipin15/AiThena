import PyPDF2
from typing import List, Dict, Optional
from io import BytesIO
import yt_dlp
import os
import docling

def extract_text_and_chapters(file) -> List[Dict]:
    # Try Docling first
    try:
        pdf_bytes = file.file.read()
        doc = docling.Document.from_bytes(pdf_bytes)
        chapters = []
        for section in doc.sections:
            chapters.append({
                'title': section.title or f'Section {len(chapters)+1}',
                'content': section.text
            })
        if chapters:
            return chapters
    except Exception as e:
        pass  # Fallback to PyPDF2
    file.file.seek(0)
    pdf_reader = PyPDF2.PdfReader(file.file)
    chapters = []
    full_text = ""
    for page in pdf_reader.pages:
        full_text += page.extract_text() or ""
    split_text = full_text.split('Chapter')
    for idx, chapter in enumerate(split_text[1:], 1):
        chapters.append({
            'title': f'Chapter {idx}',
            'content': chapter.strip()
        })
    return chapters if chapters else [{"title": "Full Text", "content": full_text.strip()}]

def download_youtube_audio(youtube_url: str, output_dir: str = "downloads") -> Optional[str]:
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        wav_file = filename.rsplit('.', 1)[0] + '.wav'
        return wav_file if os.path.exists(wav_file) else None

def transcribe_audio(audio_path: str) -> str:
    # Placeholder: Integrate with Granite Speech 8B or Whisper API
    return "[Transcript of audio would be here]" 