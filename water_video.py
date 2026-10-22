import os
import asyncio
import edge_tts
from moviepy.editor import (
    ColorClip, ImageClip, TextClip, CompositeVideoClip,
    AudioFileClip, concatenate_videoclips
)
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

W, H = 1080, 1920
FPS = 24
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

SEGMENTS = [
    ((15, 23, 42), "高科技纳米净水器\n守护饮水健康", "欢迎了解我们的高科技纳米净水器，为您和家人的健康保驾护航。", False),
    ((30, 58, 138), "三层强效过滤\n去除泥沙、杂质与重金属", "采用三层核心滤芯，层层把关。您看，脏水进入机器后，强效拦截泥沙和重金属，流出来的就是纯净好水！", True),
    ((15, 23, 42), "600G大通量\n即滤即饮 无罐设计", "六百加仑大通量，即滤即饮不等待。智能无罐设计，完美节省厨房空间。", False),
    ((6, 78, 59), "权威认证\n低能耗 守护全家", "经权威认证，低能耗更省电，让全家人每天都能喝上放心的好水。", False),
]

async def tts(text, path):
    communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save(path)

def make_segment(bg_color, title_text, voice_text, show_image, idx):
    audio_path = f"output/voice_{idx}.mp3"
    asyncio.run(tts(voice_text, audio_path))
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # 1. 纯色背景
    bg = ColorClip(size=(W, H), color=bg_color, duration=duration)

    clips_to_composite = [bg]

    # 2. 中间的产品/滤芯图片（如果有要求显示）
    if show_image and os.path.exists("2.png"):
        # 提取2.png并缩放，放在屏幕正中间
        img = ImageClip("2.png").set_duration(duration)
        img = img.resize(height=1000) # 调整高度
        img = img.set_position("center")
        clips_to_composite.append(img)

    # 3. 屏幕上方的大字标题
    title = TextClip(
        title_text,
        fontsize=90,
        color="white",
        font=FONT,
        method="caption",
        size=(W - 100, None),
        align="center"
    ).set_position(("center", 200)).set_duration(duration)
    title = title.crossfadein(0.5)
    clips_to_composite.append(title)

    # 4. 添加底部字幕
    sub = TextClip(
        voice_text,
        fontsize=60,
        color="white",
        font=FONT,
        method="caption",
        size=(W - 100, None),
        align="center",
        bg_color="rgba(0,0,0,0.7)"
    ).set_position(("center", H - 300)).set_duration(duration)
    clips_to_composite.append(sub)

    clip = CompositeVideoClip(clips_to_composite).set_audio(audio)
    return clip

def main():
    os.makedirs("output", exist_ok=True)
    clips = [make_segment(c, t, v, s, i) for i, (c, t, v, s) in enumerate(SEGMENTS)]
    final = concatenate_videoclips(clips, method="compose")
    
    final = final.crossfadein(0.5)
    
    final.write_videofile("output/video.mp4", fps=FPS, codec="libx264", audio_codec="aac")

    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;background:#111;display:flex;justify-content:center;align-items:center;height:100vh}
video{max-height:100vh;max-width:100%}</style></head>
<body><video src="video.mp4" controls autoplay loop></video></body></html>"""
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
