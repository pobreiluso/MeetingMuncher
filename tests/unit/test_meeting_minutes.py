import sys
sys.path.append('../../')

from unittest.mock import patch, mock_open, ANY, Mock
from meeting_minutes import AudioTranscriptionService

@patch('openai.audio.transcriptions.create')
@patch("builtins.open", new_callable=mock_open, read_data="fake audio data")
def test_transcribe(mock_file_open, mock_transcriptions_create):
    mock_transcriptions_create.return_value = Mock(text="Test transcription")

    service = AudioTranscriptionService()
    result = service.transcribe('fake_audio_file_path.mp3')

    assert result == "Test transcription"
    mock_transcriptions_create.assert_called_once_with(model=service.model, file=ANY)
