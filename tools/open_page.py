"""잠긴 주제 하나를 연다.
사용: python3 tools/open_page.py 010   (저장소 맨 위 폴더, main 가지에서 실행)
잠긴 주제의 페이지·사진·영상은 vault 가지에만 보관돼 있고, 여기서 main으로 꺼내 온다."""
import json, subprocess, sys
no = sys.argv[1]
pages = json.load(open('pages.json', encoding='utf-8'))
page = next(p for p in pages if p['no'] == no)
assert page.get('locked'), '이미 열려 있는 번호'
subprocess.run(['git', 'fetch', '-q', 'origin', 'vault'], check=True)
subprocess.run(['git', 'checkout', 'FETCH_HEAD', '--', 'p/%s' % no], check=True)
page['locked'] = False
json.dump(pages, open('pages.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
subprocess.run([sys.executable, 'tools/build_index.py'], check=True)
print('열림:', no, page['title'])
