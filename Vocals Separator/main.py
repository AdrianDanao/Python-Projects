
import os
import subprocess
from demucs.separate import main as demucs_separate

def download_youtube_audio(youtube_url, output_folder):
    # Args:
    #     youtube_url (str): The URL of the YouTube video.
    #     output_folder (str): The folder where the downloaded audio will be saved.
    # Returns:
    #     tuple: A tuple containing the path of the downloaded audio file and the folder where it is saved.
    """
    Download audio from a YouTube video as an mp3 file using yt-dlp.
    """
    command = ["yt-dlp", "--print", "%(title)s", youtube_url]
    title = subprocess.check_output(command, text=True).strip().replace(" ", "_").replace("/", "_")  # Sanitize folder name
    
    song_folder = os.path.join(output_folder, title)
    os.makedirs(song_folder, exist_ok=True)
    
    output_file = os.path.join(song_folder, f"{title}.mp3")
    command = ["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3", "-o", output_file, youtube_url]
    subprocess.run(command, check=True)
    
    return output_file, song_folder

def isolate_vocals_with_demucs(input_file, output_folder):
    """
    Use Demucs to isolate vocals from the input audio file.
    """
    demucs_separate(["--mp3", "--two-stems", "vocals", "-n", "htdemucs", "-o", output_folder, input_file])
    vocals_file = os.path.join(output_folder, "htdemucs", os.path.splitext(os.path.basename(input_file))[0], "vocals.mp3")
    return vocals_file

def main():
    youtube_url = input("Enter YouTube URL: ")
    output_folder = "demucs_output"  # Folder to store Demucs output
    
    print("Downloading audio from YouTube...")
    input_mp3, song_folder = download_youtube_audio(youtube_url, output_folder)
    
    print("Isolating vocals with Demucs...")
    vocals_file = isolate_vocals_with_demucs(input_mp3, song_folder)
    print(f"Isolated vocals saved to: {vocals_file}")

if __name__ == "__main__":
    main()
