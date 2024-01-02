from moviepy.editor import ImageSequenceClip
from app.utilities.image_helpers import generate_images
from app.utilities.audio_helpers import generate_audio
from app.utilities.subtitles_helpers import generate_subtitles

def create_video(script, title, description, hashtags, duration_per_image=6):
    """
    Creates a video from a given script, title, description, and hashtags.
    Generates images and audio, then combines them into a video.

    :param script: The script for the video content.
    :param title: The title of the video.
    :param description: The description of the video.
    :param hashtags: The hashtags associated with the video.
    :param duration_per_image: The duration each image is displayed in the video.
    :return: Path to the created video file.
    """
    # Generate images based on the script using DALL-E
    images = generate_images(script, title, description, hashtags)

    # Generate audio narration for the video using ElevenLabs
    audio_file_path = generate_audio(script)

    # Generate subtitles for the video
    subtitles = generate_subtitles(script)

    # Create a video clip from the images
    video_clip = ImageSequenceClip(images, durations=[duration_per_image] * len(images))

    # Set the audio of the video clip
    video_clip = video_clip.set_audio(audio_file_path)

    # Add subtitles to the video
    video_clip = video_clip.set_subtitles(subtitles)

    # Define the output video file path
    output_video_path = f"output_videos/{title.replace(' ', '_')}.mp4"

    # Write the video file to the specified path
    video_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

    # Return the path to the created video file
    return output_video_path
