# 오늘의 프롬프트 (지쿱AI대학교 · 지쿱파트너스 교육용)

- 모음: index.html (tools/build_index.py 가 pages.json 으로 만든다)
- 낱개: p/번호/ (사진·영상·프롬프트). 낱개에는 모음으로 가는 링크를 넣지 않는다.
- 새 주제 추가: tools/add_page.py 설정.json → tools/build_index.py
- 잠금: pages.json 의 locked 가 true 인 주제는 main 가지에 미리보기 사진(thumb.jpg)만 있고,
  페이지·사진·영상은 vault 가지에만 있다. 그래서 주소에 번호를 직접 넣어도 열리지 않는다.
- 잠긴 주제 열기: python3 tools/open_page.py 번호 → 커밋 → main 에 올리기
- 새 주제를 잠긴 채로 추가하려면: vault 가지에도 같은 폴더를 올리고 main 에서는 thumb.jpg 만 남긴다.
