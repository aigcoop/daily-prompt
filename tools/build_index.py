"""pages.json 목록으로 모음 페이지(index.html)와 작은 미리보기 사진을 만든다.
사용: python3 tools/build_index.py  (저장소 맨 위 폴더에서 실행)"""
import json, html
from PIL import Image

pages = json.load(open('pages.json', encoding='utf-8'))
cards = []
for p in pages:
    im = Image.open('p/%s/%s' % (p['no'], p['photo'])).convert('RGB')
    w, h = im.size
    side = min(w, h)
    top = int((h - side) * 0.25)
    im = im.crop(((w - side) // 2, top, (w - side) // 2 + side, top + side)).resize((240, 240))
    im.save('p/%s/thumb.jpg' % p['no'], quality=82, optimize=True)
    cards.append('''    <li><a class="card" href="p/%s/">
      <img src="p/%s/thumb.jpg" width="240" height="240" alt="" loading="lazy">
      <span class="txt"><span class="no">%d번 · %s</span><span class="ttl">%s</span></span>
      <span class="go" aria-hidden="true">›</span>
    </a></li>''' % (p['no'], p['no'], int(p['no']), html.escape(p['kind']), html.escape(p['title'])))

page = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>오늘의 프롬프트 모음 | AI로사쌤</title>
<meta property="og:title" content="오늘의 프롬프트 모음 | AI로사쌤">
<meta property="og:description" content="매일 하나씩 올리는 사진·영상 프롬프트를 한곳에서 골라 복사하세요.">
<meta property="og:image" content="https://aigcoop.github.io/daily-prompt/p/%s/%s">
<meta property="og:type" content="website">
<link href="https://fonts.googleapis.com/css2?family=Jua&family=Gowun+Dodum&display=swap" rel="stylesheet">
<style>
/* 배치: 휴대폰 한 줄 세로 흐름 — 제목 → 주제 단추 목록(작은 사진 + 번호 + 제목) */
:root{
  --bg:#eef4f1;--card:#ffffff;--ink:#16302b;--soft:#5b716c;--line:#cfdcd7;
  --accent:#0c7a66;--mark:#ffe27a;
  --display:"Jua","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  --body:"Gowun Dodum","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#101b19;--card:#182724;--ink:#e6f1ee;--soft:#9db3ad;--line:#2c403b;
    --accent:#3fc4a8;--mark:#6b5a12;color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#101b19;--card:#182724;--ink:#e6f1ee;--soft:#9db3ad;--line:#2c403b;
  --accent:#3fc4a8;--mark:#6b5a12;color-scheme:dark;
}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.6}
main{max-width:520px;margin:0 auto;padding:20px 16px 40px;display:flex;flex-direction:column;gap:16px}
.day{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;
  border-bottom:2px solid var(--ink);padding-bottom:8px}
.day b{font-family:var(--display);font-weight:400;font-size:20px}
.day span{color:var(--soft);font-size:15px}
h1{font-family:var(--display);font-weight:400;font-size:28px;line-height:1.3;margin:0;text-wrap:balance}
h1 em{font-style:normal;background:linear-gradient(transparent 58%%,var(--mark) 58%%)}
.how{margin:0;color:var(--soft)}
ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.card{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--line);
  border-radius:14px;padding:10px;color:inherit;text-decoration:none}
.card img{width:76px;height:76px;border-radius:10px;object-fit:cover;flex:none;display:block}
.txt{display:flex;flex-direction:column;gap:2px;flex:1;min-width:0}
.no{color:var(--accent);font-size:14px}
.ttl{font-family:var(--display);font-size:19px;line-height:1.35;word-break:keep-all}
.go{font-size:28px;color:var(--soft);flex:none;padding-right:4px}
.card:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.card:active{border-color:var(--accent)}
</style>
</head>
<body>
<main>
  <div class="day"><b>오늘의 프롬프트</b><span>AI로사쌤 · 모음</span></div>
  <h1>매일 하나씩, <em>프롬프트 모음</em></h1>
  <p class="how">만들고 싶은 주제를 누르면 예시와 프롬프트가 나와요. 지금 %d개가 있어요.</p>
  <ul>
%s
  </ul>
  <p class="how" style="text-align:center;font-size:14px">출처 · AI로사쌤</p>
</main>
</body>
</html>
''' % (pages[-1]['no'], pages[-1]['photo'], len(pages), '\n'.join(cards))
open('index.html', 'w', encoding='utf-8').write(page)
print('index.html:', len(pages), 'pages')
