import sys
sys.path.append('../../')

# tests/integration/test_end_to_end_workflow.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
from meeting_minutes import main  # Import the main function from your application

@patch('meeting_minutes.AudioExtractor.extract_audio')
@patch('meeting_minutes.AudioTranscriptionService.transcribe')
@patch('meeting_minutes.MeetingAnalyzer.summarize')
@patch('meeting_minutes.MeetingAnalyzer.extract_key_points')
@patch('meeting_minutes.MeetingAnalyzer.extract_action_items')
@patch('meeting_minutes.MeetingAnalyzer.analyze_sentiment')
@patch('meeting_minutes.DocumentManager.save_to_docx')
def test_end_to_end_workflow(
    mock_extract_audio, mock_transcribe, mock_summarize,
    mock_extract_key_points, mock_extract_action_items,
    mock_analyze_sentiment, mock_save_to_docx
):
    # Mocked responses should be adapted to what is expected from the real methods
    mock_transcription_response = MagicMock(text="Detailed transcription")
    mock_summary_response = "Concise summary"
    mock_key_points_response = ["Key point 1", "Key point 2"]
    mock_action_items_response = ["Action 1", "Action 2"]
    mock_sentiment_response = "Overall sentiment"
    
    # Set up the return values for the mocks
    mock_extract_audio.return_value = 'fake_audio_file.mp3'
    mock_transcribe.return_value = mock_transcription_response
    mock_summarize.return_value = mock_summary_response
    mock_extract_key_points.return_value = mock_key_points_response
    mock_extract_action_items.return_value = mock_action_items_response
    mock_analyze_sentiment.return_value = mock_sentiment_response
    
    # Run the main function
    main('fake_api_key', 'fake_video_file.mp4')
    
    # Assert that each mock was called as expected
    mock_extract_audio.assert_called_once_with('fake_video_file.mp4')
    mock_transcribe.assert_called_once_with('fake_audio_file.mp3')
    mock_summarize.assert_called_once_with()
    mock_extract_key_points.assert_called_once_with()
    mock_extract_action_items.assert_called_once_with()
    mock_analyze_sentiment.assert_called_once_with()
    
    # Ensure the save_to_docx is called with the expected content structure and filename
    mock_save_to_docx.assert_called_once_with({
        'abstract_summary': mock_summary_response,
        'key_points': mock_key_points_response,
        'action_items': mock_action_items_response,
        'sentiment': mock_sentiment_response
    }, 'fake_video_file.docx')
