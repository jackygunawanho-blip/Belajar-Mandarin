import os
import asyncio
import edge_tts
from moviepy.editor import (
    ColorClip, TextClip, CompositeVideoClip,
    AudioFileClip, concatenate_videoclips
)
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

W, H = 1080, 1920
FPS = 24
BG_COLOR = (245, 245, 240)
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

SEGMENTS = [
    ("“你吃了吗”\n不是问你吃没吃",
     "如果你在中国听到‘你吃了吗’，别急着回答。"),
    ("它 = Hi",
     "这句话不是真的问你吃饭了没有。它就跟英语里的‘How are you’一样，就是个打招呼。"),
    ("正确回答：\n吃了，你呢？",
     "你只需要回一句‘吃了，你呢’，就可以了。千万别认真说你吃了什么。"),
    ("主页有 10 个\n这样的短语 PDF",
     "我整理了 10 个课本不教、但中国人天天用的短语，放在主页了。"),
]

async def tts(text, path):
    communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save(path)

def make_segment(text, voice_text, idx):
    audio_path = f"output/voice_{idx}.mp3"
    asyncio.run(tts(voice_text, audio_path))

    audio = AudioFileClip(audio_path)
    duration = audio.duration

    bg = ColorClip(size=(W, H), color=BG_COLOR, duration=duration)

    txt = TextClip(
        text,
        fontsize=90,
        color="black",
        font=FONT,
        method="caption",
        size=(W - 160, None),
        align="center",
    ).set_position("center").set_duration(duration)

    txt = txt.crossfadein(0.3).crossfadeout(0.3)

    clip = CompositeVideoClip([bg, txt]).set_audio(audio)
    return clip

def main():
    os.makedirs("output", exist_ok=True)

    clips = [make_segment(t, v, i) for i, (t, v) in enumerate(SEGMENTS)]
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile("output/video.mp4", fps=FPS, codec="libx264",
                          audio_codec="aac")

    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>你吃了吗</title>
<style>body{margin:0;background:#111;display:flex;
justify-content:center;align-items:center;height:100vh}
video{max-height:100vh;max-width:100%}</style></head>
<body><video src="video.mp4" controls autoplay loop></video></body>
</html>"""
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
