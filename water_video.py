import os
import asyncio
import edge_tts
from moviepy.editor import (
    ColorClip, TextClip, CompositeVideoClip,
    AudioFileClip, concatenate_videoclips
)
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

# 竖屏尺寸
W, H = 1080, 1920
FPS = 24
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# 重新设计的分镜（背景颜色, 大字, 配音）
SEGMENTS = [
    ((15, 23, 42), "高科技纳米净水器\n为您和家人保驾护航", "欢迎了解我们的高科技净水器，为您和家人的饮水健康保驾护航。"),
    ((30, 58, 138), "三层强效过滤\n去除杂质与重金属", "采用三层核心滤芯，层层把关，强效去除水中的泥沙、杂质和重金属。"),
    ((15, 23, 42), "600G 大通量\n智能无罐设计", "六百加仑大通量，即滤即饮，智能无罐设计，节省厨房空间。"),
    ((6, 78, 59), "低能耗认证\n守护全家饮水健康", "经权威认证，低能耗更省电，让家人喝上放心的好水。"),
]

async def tts(text, path):
    # 中文女声
    communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save(path)

def make_segment(bg_color, title_text, voice_text, idx):
    audio_path = f"output/voice_{idx}.mp3"
    asyncio.run(tts(voice_text, audio_path))
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # 纯色高级背景
    bg = ColorClip(size=(W, H), color=bg_color, duration=duration)

    # 屏幕正中间的大字
    title = TextClip(
        title_text,
        fontsize=100,
        color="white",
        font=FONT,
        method="caption",
        size=(W - 100, None),
        align="center"
    ).set_position("center").set_duration(duration)

    # 添加稍微的淡入动画
    title = title.crossfadein(0.5)
    
    clip = CompositeVideoClip([bg, title]).set_audio(audio)
    return clip

def main():
    os.makedirs("output", exist_ok=True)
    clips = [make_segment(c, t, v, i) for i, (c, t, v) in enumerate(SEGMENTS)]
    final = concatenate_videoclips(clips, method="compose")
    
    # 视频之间加 0.5 秒的转场过渡
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
