from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

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
            return {'status': False, 'msg': '無法取得轉錄稿'}

    except Exception as e:
        print(f"Error: {e}")
        return {'status': False, 'msg': e}
