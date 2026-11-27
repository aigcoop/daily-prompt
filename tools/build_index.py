"""pages.json 목록으로 모음 페이지(index.html)와 작은 미리보기 사진을 만든다.
사용: python3 tools/build_index.py  (저장소 맨 위 폴더에서 실행)"""
import json, html
from PIL import Image

pages = json.load(open('pages.json', encoding='utf-8'))
cards = []
for p in pages:
    im = Image.open('p/%s/%s' % (p['no'], p['photo'])).convert('RGB')
    w, h = im.size
    cw = w
    ch = min(h, round(w * 4 / 3))
    top = int((h - ch) * 0.12)
    im = im.crop((0, top, cw, top + ch)).resize((360, 480))
    im.save('p/%s/thumb.jpg' % p['no'], quality=80, optimize=True)
    kind = p['kind'].replace(' + ', '+')
    cards.append('''    <li class="tile">
      <a class="open" href="p/%s/" aria-label="%d번 %s"><img src="p/%s/thumb.jpg?v=2" width="360" height="480" alt="" loading="lazy"></a>
      <span class="kind">%s</span><span class="num">%d</span>
      <button type="button" class="share" data-url="https://aigcoop.github.io/daily-prompt/p/%s/" data-title="%s" aria-label="%d번만 공유"><svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M12 15V4M8 8l4-4 4 4M5 13v5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    </li>''' % (p['no'], int(p['no']), html.escape(p['title'], quote=True), p['no'], html.escape(kind), int(p['no']),
               p['no'], html.escape(p['title'] + ' | AI로사쌤 오늘의 프롬프트', quote=True), int(p['no'])))

page = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>오늘의 프롬프트 모음 | AI로사쌤</title>
<meta property="og:site_name" content="지쿱AI대학교 · 지쿱파트너스 교육용 프롬프트">
<meta property="og:title" content="오늘의 프롬프트 모음 | AI로사쌤">
<meta property="og:description" content="매일 하나씩 올리는 사진·영상 프롬프트를 한곳에서 골라 복사하세요.">
<meta property="og:image" content="https://aigcoop.github.io/daily-prompt/p/%s/%s">
<meta property="og:type" content="website">
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans+KR:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css?v=6">
</head>
<body>
<main>
  <div class="day"><b>오늘의 프롬프트</b><span>AI로사쌤 · 모음</span></div>
  <p class="edu">지쿱AI대학교 · 지쿱파트너스 교육용 프롬프트</p>
  <h1>매일 하나씩, <em>프롬프트 모음</em></h1>
  <p class="how">사진을 누르면 예시와 프롬프트가 나와요. 지금 %d개가 있어요. 사진 오른쪽 아래의 <b>공유 단추</b>를 누르면 그 주제 하나만 보이는 링크가 공유돼요.</p>
  <p id="msg" class="toast" role="status" aria-live="polite"></p>
  <ul class="grid">
%s
  </ul>
  <p class="credit">지쿱AI대학교 · 지쿱파트너스 교육용 프롬프트<br>출처 · AI로사쌤 · 무단 복제와 재배포를 금합니다</p>
</main>
<script>
(function(){
  var msg=document.getElementById('msg');
  var timer;
  function say(text){msg.textContent=text;clearTimeout(timer);timer=setTimeout(function(){msg.textContent=''},3500)}
  function copied(btn){
    btn.classList.add('done');setTimeout(function(){btn.classList.remove('done')},2500);
    say('링크가 복사됐어요. 대화창에 붙여넣기 하세요.');
  }
  function manual(url){msg.textContent='이 주소를 길게 눌러 복사하세요: '+url}
  function copy(btn,url){
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(url).then(function(){copied(btn)}).catch(function(){manual(url)});
    }else{
      try{
        var t=document.createElement('textarea');t.value=url;t.setAttribute('readonly','');
        t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();
        var ok=document.execCommand('copy');document.body.removeChild(t);
        if(ok){copied(btn)}else{manual(url)}
      }catch(e){manual(url)}
    }
  }
  function share(btn){
    var url=btn.getAttribute('data-url'),title=btn.getAttribute('data-title');
    if(navigator.share){
      navigator.share({title:title,url:url}).catch(function(e){
        if(e&&e.name==='AbortError'){return}
        copy(btn,url);
      });
    }else{copy(btn,url)}
  }
  var bs=document.querySelectorAll('button[data-url]');
  for(var i=0;i<bs.length;i++){bs[i].addEventListener('click',function(){share(this)})}
})();
</script>
</body>
</html>
''' % (pages[-1]['no'], pages[-1]['photo'], len(pages), '\n'.join(cards))
open('index.html', 'w', encoding='utf-8').write(page)
print('index.html:', len(pages), 'pages')
