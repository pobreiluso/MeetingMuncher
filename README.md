# MeetingMuncher

MeetingMuncher is a CLI tool designed for the efficient transcription and analysis of meeting audio. It leverages the power of OpenAI's APIs to transcribe audio content, summarize discussions, extract key points, identify action items, and analyze sentiment.

## Usage

    ```sh
    python3 meeting_minutes.py $OPENAI_API_KEY path_to_your_video_file.mp4


## Setup

Set your OpenAI API key as an environment variable:
    export OPENAI_API_KEY='your_openai_api_key'

### Prerequisites

- Python 3
- FFMPEG (for audio extraction)

### Installation

1. Clone the MeetingMuncher repository:

   ```sh
   git clone https://github.com/your-username/MeetingMuncher.git
   cd MeetingMuncher

2. To get started with MeetingMuncher, you'll need to install some prerequisites and set up your environment.

    ```sh
    pip3 install -r requirements.txt

3. Set your OpenAI API key as an environment variable:
    export OPENAI_API_KEY='your_openai_api_key'
