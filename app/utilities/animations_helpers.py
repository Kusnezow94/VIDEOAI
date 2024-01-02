from moviepy.editor import ImageSequenceClip
import os

def animate_images(image_folder, output_path, frame_rate=10):
    """
    Create an animation from a sequence of images stored in a folder.
    The images should be named in a sequence (e.g., img001.jpg, img002.jpg, etc.).
    The animation will be saved to the specified output path.

    :param image_folder: The path to the folder containing the image sequence.
    :param output_path: The path where the animated video will be saved.
    :param frame_rate: The number of frames per second in the output video.
    :return: None
    """
    # Ensure the image folder exists
    if not os.path.exists(image_folder):
        raise FileNotFoundError(f"The specified image folder does not exist: {image_folder}")

    # Get the list of all files in the image folder
    image_files = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if img.endswith(('.png', '.jpg', '.jpeg'))]

    # Ensure there are images to create a video
    if not image_files:
        raise ValueError("No images found in the specified folder to create a video.")

    # Create a video clip from the images
    clip = ImageSequenceClip(image_files, fps=frame_rate)

    # Write the video file to the specified output path
    clip.write_videofile(output_path, codec='libx264', audio=False)

    # Close the clip to release resources
    clip.close()