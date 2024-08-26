import whisper
import ffmpeg
import argparse
import os

def extract_audio(video_file, audio_file):
    """Extract audio from video file."""
    ffmpeg.input(video_file).output(audio_file).run(overwrite_output=True)

def generate_subtitles(audio_file):
    """Generate subtitles from audio file using Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    subtitles = []
    
    for i, segment in enumerate(result['segments']):
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        subtitles.append({
            'index': i + 1,
            'start': start_time,
            'end': end_time,
            'text': text
        })
    
    return subtitles

def save_subtitles_to_file(subtitles, output_file):
    """Save the subtitles to an SRT file."""
    with open(output_file, 'w') as f:
        for subtitle in subtitles:
            f.write(f"{subtitle['index']}\n")
            f.write(f"{format_time(subtitle['start'])} --> {format_time(subtitle['end'])}\n")
            f.write(f"{subtitle['text']}\n\n")

def format_time(seconds):
    """Format time in SRT format (HH:MM:SS,MS)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def main():
    parser = argparse.ArgumentParser(description="Generate subtitles from an MP4 file.")
    parser.add_argument('video_file', type=str, help="Path to the MP4 file")
    parser.add_argument('output_file', type=str, help="Path to save the SRT file")
    args = parser.parse_args()

    # Paths for intermediate audio file
    audio_file = 'temp_audio.wav'

    try:
        # Extract audio from video
        extract_audio(args.video_file, audio_file)

        # Generate subtitles
        subtitles = generate_subtitles(audio_file)
        
        if not subtitles:
            print("No subtitles generated.")
            return

        # Display subtitles options
        print("Generated subtitles:")
        for subtitle in subtitles:
            print(f"{subtitle['index']}. {subtitle['text']}")

        # Save subtitles to file
        save_subtitles_to_file(subtitles, args.output_file)

        print(f"Subtitles saved to {args.output_file}")

    finally:
        # Clean up temporary audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)

if __name__ == "__main__":
    main()

