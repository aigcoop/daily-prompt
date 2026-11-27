"""낱개 페이지들을 공통 디자인(assets/style.css, assets/page.js)으로 옮기고 저장 단추를 넣는다. 여러 번 실행해도 안전."""
import glob, re
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans+KR:wght@400;500;600&display=swap" rel="stylesheet">'
ICON = '<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true"><path d="M12 4v11M8 11l4 4 4-4M5 20h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
for f in sorted(glob.glob('p/*/index.html')):
    s = open(f, encoding='utf-8').read()
    # 머리: 글꼴 + 스타일 → 공통 파일
    s = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>\s*(<link rel="stylesheet" href="[^"]*style\.css[^"]*">|<style>.*?</style>)',
               FONTS + '\n<link rel="stylesheet" href="../../assets/style.css?v=2">', s, count=1, flags=re.S)
    # 001·견본: 단추 형식 통일
    s = s.replace('<div class="box" id="prompt">', '<div class="box" id="p1">')
    s = s.replace('<button type="button" id="copy">프롬프트 복사</button>',
                  '<button type="button" data-copy="p1" data-label="프롬프트 복사">프롬프트 복사</button>')
    s = s.replace('<p id="msg" role="status" aria-live="polite"></p>', '<p class="msg" id="m-p1" role="status" aria-live="polite"></p>')
    # 스크립트 → 공통 파일
    s = re.sub(r'<script>.*?</script>', '<script src="../../assets/page.js?v=2"></script>', s, count=1, flags=re.S)
    # 단계 제목
    s = re.sub(r'<h2>([^<·]+) · ([^<]+)</h2>', r'<h2><span class="step">\1</span>\2</h2>', s)
    # 출처
    s = s.replace('<p class="how" style="text-align:center;font-size:14px">출처 · AI로사쌤</p>', '<p class="credit">출처 · AI로사쌤</p>')
    # 저장 단추
    def fig(m):
        body = m.group(0)
        if 'class="dl"' in body:
            return body
        img = re.search(r'<img src="([^"?]+)', body)
        vid = re.search(r'<video src="([^"?]+)', body)
        if vid:
            link = '<a class="dl" href="%s" download="오늘의프롬프트-영상.mp4">%s영상 저장</a>' % (vid.group(1), ICON)
        elif img:
            link = '<a class="dl" href="%s" download="오늘의프롬프트-사진.jpg">%s사진 저장</a>' % (img.group(1), ICON)
        else:
            return body
        def cap(c):
            t = c.group(1).replace('AI로 만든 예시 사진이에요.', 'AI로 만든 예시 사진').replace('AI로 만든 예시 영상이에요. 눌러서 재생해 보세요.', 'AI로 만든 예시 영상').strip()
            return '<figcaption><span>%s</span>%s</figcaption>' % (t, link)
        return re.sub(r'<figcaption>(.*?)</figcaption>', cap, body, flags=re.S)
    s = re.sub(r'<figure>.*?</figure>', fig, s, flags=re.S)
    open(f, 'w', encoding='utf-8').write(s)
    print(f, s.count('class="dl"'), 'style.css' in s, 'page.js' in s, '<style>' in s)
