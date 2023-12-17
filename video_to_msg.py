from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import os


def youtube_video_to_txt(youtube_url, output_path='.'):
    try:
        os.environ["OPENAI_API_KEY"] = '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'

        # 取得YouTube影片
        yt = YouTube(youtube_url)

        # 選擇最高品質的影片串流
        # video_stream = yt.streams.get_highest_resolution()
        video_stream = yt.streams.filter(only_audio=True).first()

        # 下載影片
        video_stream.download(output_path)

        client = OpenAI()

        audio_file= open(f"{yt.title}.mp4", "rb")
        transcript = client.audio.transcriptions.create(
          model="whisper-1",
          file=audio_file,
          response_format="text"
        )
        return {'status': True, 'msg': f"標題：{yt.title}\n內容：{transcript}"}
    except Exception as e:
        return {'status': False, 'msg': '無法取得轉錄稿'}


def get_chinese_transcript(video_url):
    try:
        video_id = video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-TW','zh-Hant','zh-Hans','zh'])
        return transcript
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_transcript_to_msg(transcript, title):
    try:
        content = ''
        for entry in transcript:
            if len(entry['text']) > 4:
                content += f"{entry['text']}[@]"
        content = content.replace("[@]", ",")[:-1]
        return f"標題：{title}\n內容：{content}"
        #return content
    except Exception as e:
        print(f"Error saving transcript: {e}")

def save_transcript_to_file(transcript, file_path, title):
    try:
        content = ''
        for entry in transcript:
            if len(entry['text']) > 3:
                content += f"{entry['text']}[@]"
        content = content.replace("[@]", ",")[:-1]
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"標題：{title}\n")
            file.write(f"內容：{content}")
        print(f"轉錄稿已保存到 {file_path}")
    except Exception as e:
        print(f"Error saving transcript: {e}")

def get_youtube_msg(url):
    try:
        yt = YouTube(url)
        transcript = get_chinese_transcript(url)
        if transcript:
            youtube_msg = save_transcript_to_msg(transcript, yt.title)
            print(youtube_msg)
            return {'status': True, 'msg': youtube_msg}
        else:
            result = youtube_video_to_txt(url)
            return result

    except Exception as e:
        print(f"Error: {e}")
        result = youtube_video_to_txt(url)
        return result
