import os
import requests
import sys
import subprocess
from docx import Document
import openai
import webbrowser


class AudioTranscriptionService:
    def __init__(self, model="whisper-1"):
        self.model = model

    def transcribe(self, audio_file_path):
        with open(audio_file_path, 'rb') as audio_file:
            transcription = openai.audio.transcriptions.create(
                model=self.model,
                file=audio_file
            )
        return transcription.text


class MeetingAnalyzer:
    def __init__(self, transcription):
        self.transcription = transcription

    def summarize(self):
        return self._get_openai_response("summarize into a concise abstract paragraph")

    def extract_key_points(self):
        return self._get_openai_response("identify and list the main points")

    def extract_action_items(self):
        return self._get_openai_response("extract action items")

    def analyze_sentiment(self):
        return self._get_openai_response("analyze the sentiment of the following text", message_key='message')

    def _get_openai_response(self, task_description, message_key='message.content'):
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0,
            messages=[
                {"role": "system", "content": f"You are an AI {task_description}."},
                {"role": "user", "content": self.transcription}
            ]
        )
        return response.choices[0].message.content


class DocumentManager:
    @staticmethod
    def save_to_docx(content, filename):
        doc = Document()
        for key, value in content.items():
            heading = key.replace('_', ' ').title()
            doc.add_heading(heading, level=1)
            doc.add_paragraph(value)
            doc.add_paragraph()
        doc.save(filename)


class VideoDownloader:
    @staticmethod
    def download_from_google_drive(drive_url):
        file_id = drive_url.split('/')[-2]
        direct_download_url = f'https://drive.google.com/uc?id={file_id}&export=download'
        local_filename = 'downloaded_video.mp4'
        with requests.get(direct_download_url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename


class AudioExtractor:
    @staticmethod
    def extract_audio(input_video, bitrate='56k'):
        print(f"Extracting audio from {input_video}...")
        output_audio = input_video.replace('.mp4', '.mp3')
        if os.path.exists(output_audio):
            answer = input(
                "Output audio file already exists. Delete it? (yes/no): ")
            if answer.lower() == 'yes':
                print(f"Deleting {output_audio}...")
                os.remove(output_audio)
            else:
                print("Audio extraction cancelled by user.")
                return output_audio

        print("Starting audio extraction with ffmpeg...")
        subprocess.run([
            'ffmpeg',
            '-i', input_video,
            '-b:a', bitrate,
            '-vn',
            output_audio
        ], check=True)
        print(f"Audio successfully extracted to {output_audio}")
        return output_audio


def login_with_google():
    webbrowser.open('https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=https://www.googleapis.com/auth/drive.readonly&response_type=code', new=2)


def main(api_key, file_path):
    try:
        print("Beginning video transcription process...")

        # login_with_google()
        audio_file = AudioExtractor.extract_audio(file_path)
        print("Audio extracted, starting transcription...")

        transcription_text = AudioTranscriptionService().transcribe(audio_file)
        print("Transcription completed.")

        print("Analyzing transcription...")
        analyzer = MeetingAnalyzer(transcription_text)
        meeting_info = {
            'abstract_summary': analyzer.summarize(),
            'key_points': analyzer.extract_key_points(),
            'action_items': analyzer.extract_action_items(),
            'sentiment': analyzer.analyze_sentiment()
        }
        print("Analysis completed.")

        print("Saving analyzed information to document...")
        DocumentManager.save_to_docx(
            meeting_info, file_path.replace('.mp4', '.docx'))

        print("Document saved: meeting_minutes.docx")

        print("\nMeeting Information:")
        for section, content in meeting_info.items():
            print(f"{section.title().replace('_', ' ')}:\n{content}\n")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python transcribe_video.py api_key file_path")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
