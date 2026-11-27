"""사진 + 영상 낱개 페이지 하나를 만들고 pages.json에 추가한다.
사용: python3 tools/add_page.py 설정.json   (저장소 맨 위 폴더에서 실행)
설정: no, kind("person" 또는 "product"), image, video, img_prompt, vid_prompt,
      h1(강조 부분은 <em>), title, og, desc, alt, card"""
import json, os, re, subprocess, sys
from PIL import Image

c = json.load(open(sys.argv[1], encoding='utf-8'))
no = c['no']
os.makedirs('p/' + no, exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', c['video'], '-c:v', 'libx264', '-crf', '26',
                '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k',
                '-movflags', '+faststart', 'p/%s/video.mp4' % no], check=True)
im = Image.open(c['image']).convert('RGB')
im.thumbnail((1080, 1920))
im.save('p/%s/photo.jpg' % no, quality=88, optimize=True)
w, h = im.size

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')

def box(src, i, new):
    a = src.index('<div class="box" id="%s">' % i)
    b = src.index('</div>', a)
    return src[:a] + '<div class="box" id="%s">' % i + esc(new) + src[b:]

base = '003' if c['kind'] == 'person' else '005'
src = open('p/%s/index.html' % base, encoding='utf-8').read()
src = box(src, 'p1', c['img_prompt'])
src = box(src, 'p2', c['vid_prompt'])
src = re.sub(r'<h1>.*?</h1>', lambda m: '<h1>%s</h1>' % c['h1'], src, count=1, flags=re.S)
src = re.sub(r'<title>.*?</title>', lambda m: '<title>%s | AI로사쌤</title>' % c['title'], src, count=1)
src = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(c['og']) + ' | AI로사쌤 오늘의 프롬프트', src, count=1)
src = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(c['desc']), src, count=1)
src = src.replace('p/%s/photo.jpg' % base, 'p/%s/photo.jpg' % no)
src = src.replace('AI로사쌤 · %d번' % int(base), 'AI로사쌤 · %d번' % int(no))
src = re.sub(r'<img src="photo.jpg" width="\d+" height="\d+" alt="[^"]*"',
             lambda m: '<img src="photo.jpg" width="%d" height="%d" alt="%s"' % (w, h, esc(c['alt'])), src, count=1)
open('p/%s/index.html' % no, 'w', encoding='utf-8').write(src)

pages = json.load(open('pages.json', encoding='utf-8'))
assert not any(p['no'] == no for p in pages), '이미 있는 번호'
pages.append({"no": no, "title": c['card'], "kind": "사진 + 영상", "photo": "photo.jpg"})
json.dump(pages, open('pages.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(no, w, h, os.path.getsize('p/%s/photo.jpg' % no), os.path.getsize('p/%s/video.mp4' % no))
