import os
import asyncio
import edge_tts
from moviepy.editor import (
    ImageClip, ColorClip, TextClip, CompositeVideoClip,
    AudioFileClip, concatenate_videoclips
)
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

W, H = 1080, 1920
FPS = 24
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# ==========================================
# 已经为你换成对应的 1.png, 2.png, 3.png
# ==========================================
SEGMENTS = [
    ("1.png", "600G大通量净水器\n强效降低TDS值 智能无罐设计", "欢迎了解Segar Hidup 600G净水器。它能有效降低百分之九十五的TDS值，采用智能无罐设计，节省空间。"),
    ("2.png", "高科技纳米过滤\n三层滤芯 层层把关", "它采用高科技纳米过滤技术，结合PAC、RO和T33三层滤芯，强效去除水中的细菌和重金属。"),
    ("3.png", "经临床测试认证\n低能耗 守护全家饮水健康", "经临床测试认证，低能耗更环保。立刻为您的家人，提供安全清新的健康好水吧！"),
]

async def tts(text, path):
    # 使用中文女声
    communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save(path)

def make_segment(img_path, subtitle, voice_text, idx):
    audio_path = f"output/voice_{idx}.mp3"
    asyncio.run(tts(voice_text, audio_path))
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # 处理图片铺满竖屏
    if img_path and os.path.exists(img_path):
        bg = ImageClip(img_path).set_duration(duration)
        scale = max(W / bg.w, H / bg.h)
        bg = bg.resize(scale).set_position("center")
        bg = bg.crop(x_center=bg.w/2, y_center=bg.h/2, width=W, height=H)
    else:
        bg = ColorClip(size=(W, H), color=(173, 216, 230), duration=duration)

    # 添加底部中文字幕
    txt = TextClip(
        subtitle,
        fontsize=75,
        color="white",
        font=FONT,
        method="caption",
        size=(W - 120, None),
        align="center",
        bg_color="rgba(0,0,0,0.7)",
        padding=20
    ).set_position(("center", H * 0.8)).set_duration(duration)

    txt = txt.crossfadein(0.2)
    clip = CompositeVideoClip([bg, txt]).set_audio(audio)
    return clip

def main():
    os.makedirs("output", exist_ok=True)
    clips = [make_segment(img, sub, voice, i) for i, (img, sub, voice) in enumerate(SEGMENTS)]
    final = concatenate_videoclips(clips, method="compose")
    
    # 视频之间加 0.5 秒的转场过渡
    final = final.crossfadein(0.5)
    
    final.write_videofile("output/video.mp4", fps=FPS, codec="libx264", audio_codec="aac")

    # 网页播放器
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;background:#111;display:flex;justify-content:center;align-items:center;height:100vh}
video{max-height:100vh;max-width:100%}</style></head>
<body><video src="video.mp4" controls autoplay loop></video></body></html>"""
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
