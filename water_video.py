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

# 分成三段，分别展示三张图片的内容，并配上纯中文解说
# 格式: (背景色, 屏幕大字标题, 配音台词, 图片文件名)
SEGMENTS = [
    ((15, 23, 42), "600G大通量净水器\n强效降低TDS值", "欢迎了解我们的高科技净水器。六百加仑大通量，强效降低水中的TDS值，智能无罐设计，完美节省厨房空间。", "1.png"),
    ((30, 58, 138), "三层强效过滤系统\n拦截杂质与重金属", "它采用三层核心滤芯，层层把关。好比您看这张图，脏水进入机器后，强效拦截泥沙、杂质和重金属，流出来的就是纯净好水！", "2.png"),
    ((6, 78, 59), "权威认证 低能耗\n守护全家饮水健康", "经过权威机构认证，低能耗更省电。立刻为您的家人，提供安全清新的健康好水吧！", "3.png"),
]

async def tts(text, path):
    communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save(path)

def make_segment(bg_color, title_text, voice_text, img_file, idx):
    audio_path = f"output/voice_{idx}.mp3"
    asyncio.run(tts(voice_text, audio_path))
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # 1. 背景纯色
    bg = ColorClip(size=(W, H), color=bg_color, duration=duration)
    clips_to_composite = [bg]

    # 2. 顶部大字标题 (Y坐标 = 250)
    title = TextClip(
        title_text,
        fontsize=90,
        color="white",
        font=FONT,
        method="caption",
        size=(W - 100, None),
        align="center"
    ).set_position(("center", 250)).set_duration(duration)
    
    # 3. 居中显示图片 (完美缩放，留出上下空间)
    if os.path.exists(img_file):
        img = ImageClip(img_file).set_duration(duration)
        # 将图片统一缩放，最大宽度900，最大高度900，保证不遮挡文字
        img = img.resize(height=900)
        img = img.set_position("center")
        clips_to_composite.append(img)

    # 4. 底部中文字幕 (Y坐标 = 屏幕底部上方 200px)
    sub = TextClip(
        voice_text,
        fontsize=60,
        color="white",
        font=FONT,
        method="caption",
        size=(W - 100, None),
        align="center",
        bg_color="rgba(0,0,0,0.8)"
    ).set_position(("center", H - 350)).set_duration(duration)

    # 添加微弱的淡入效果
    title = title.crossfadein(0.5)
    sub = sub.crossfadein(0.5)

    clips_to_composite.extend([title, img, sub])

    clip = CompositeVideoClip(clips_to_composite).set_audio(audio)
    return clip

def main():
    os.makedirs("output", exist_ok=True)
    clips = [make_segment(c, t, v, img, i) for i, (c, t, v, img) in enumerate(SEGMENTS)]
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
