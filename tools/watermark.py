"""사진·영상에 교육용 표시(워터마크)를 넣는다."""
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEXT = '지쿱AI대학교 · 지쿱파트너스 교육용'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'

def overlay(w, h):
    """w×h 투명 그림: 왼쪽 아래에 흰 글씨 + 은은한 그림자"""
    size = max(14, round(w * 0.034))
    font = ImageFont.truetype(FONT, size, index=1)
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    x, y = round(w * 0.04), h - round(w * 0.04) - size - round(size * 0.3)
    sh = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((x, y), TEXT, font=font, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(size * 0.18))
    layer = Image.alpha_composite(layer, sh)
    layer = Image.alpha_composite(layer, sh)
    ImageDraw.Draw(layer).text((x, y), TEXT, font=font, fill=(255, 255, 255, 235))
    return layer

def mark_image(src, dst, quality=90):
    im = Image.open(src).convert('RGBA')
    out = Image.alpha_composite(im, overlay(*im.size)).convert('RGB')
    out.save(dst, quality=quality, optimize=True)
    return out.size

def mark_video(src, dst, tmp_png='/tmp/wm.png'):
    probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=width,height', '-of', 'csv=p=0', src], capture_output=True, text=True, check=True)
    w, h = [int(v) for v in probe.stdout.strip().split(',')[:2]]
    overlay(w, h).save(tmp_png)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-i', tmp_png, '-filter_complex', 'overlay=0:0',
                    '-c:v', 'libx264', '-crf', '26', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', dst], check=True)
