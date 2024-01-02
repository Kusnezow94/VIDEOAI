```python
from moviepy.editor import TextClip, CompositeVideoClip

def generate_subtitle_clips(script, font_path='app/static/fonts/OpenSans-Regular.ttf', font_size=24, color='white'):
    """
    Generates a list of TextClip objects for subtitles from the provided script.

    :param script: A string containing the full script to be converted into subtitles.
    :param font_path: Path to the font file to be used for the subtitles.
    :param font_size: Size of the font to be used for the subtitles.
    :param color: Color of the font.
    :return: A list of TextClip objects.
    """
    # Split the script into sentences to create separate subtitles
    sentences = script.split('. ')
    subtitle_clips = []

    for sentence in sentences:
        # Create a TextClip for each sentence
        subtitle_clip = TextClip(sentence, fontsize=font_size, font=font_path, color=color)
        subtitle_clips.append(subtitle_clip)

    return subtitle_clips

def composite_subtitles_on_video(video_clip, subtitle_clips, video_duration, interval=6):
    """
    Composites subtitles on the given video clip at specified intervals.

    :param video_clip: The main video clip on which subtitles need to be added.
    :param subtitle_clips: A list of TextClip objects to be used as subtitles.
    :param video_duration: Duration of the video clip.
    :param interval: Interval in seconds at which subtitles should change.
    :return: A CompositeVideoClip with subtitles added to the video.
    """
    # Calculate the start and end times for each subtitle clip
    times = [(start, min(start + interval, video_duration)) for start in range(0, video_duration, interval)]

    # Composite the subtitle clips onto the video clip at the calculated times
    composite_clips = [video_clip]
    for subtitle_clip, (start_time, end_time) in zip(subtitle_clips, times):
        composite_clips.append(subtitle_clip.set_start(start_time).set_duration(end_time - start_time).set_position('bottom'))

    # Create a final composite video clip with all the subtitles
    final_video = CompositeVideoClip(composite_clips, size=video_clip.size)

    return final_video
```