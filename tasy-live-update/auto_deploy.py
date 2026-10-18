import os
import subprocess
from bs4 import BeautifulSoup

# 설정
GIT_PATH = r"C:\Program Files\Git\bin\git.exe"
SITE_BASE_URL = "https://tasy.net"
TALLY_URL = "https://tally.so/r/b5DN4g"

# PDF 버튼 자동생성에서 제외할 파일 (카카오톡 뷰어 등으로 대체된 항목)
PDF_BUTTON_EXCLUDE = {"엄마가될자격.pdf"}

# 수동 버튼: (표시 이름, 링크) — PDF 버튼 뒤, 방명록 버튼 앞에 추가
# auto_deploy.py를 실행해도 이 버튼들은 유지됩니다
CUSTOM_BUTTONS = [
    ("카카오톡뷰어", "kakaotalk-viewer.html"),  # 카톡 TXT·HWPX 뷰어 도구
]

# 이 스크립트가 있는 디렉토리를 작업 경로로 사용
REPO_DIR = os.path.dirname(os.path.abspath(__file__))


def run_git(args):
    result = subprocess.run(
        [GIT_PATH] + args,
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print("오류:", result.stderr)
    return result.returncode


def update_site_and_push():
    # 규칙 1: 루트 디렉토리의 PDF 파일 목록 탐색 (제외 목록 적용)
    pdf_files = sorted([
        f for f in os.listdir(REPO_DIR)
        if f.endswith('.pdf') and f not in PDF_BUTTON_EXCLUDE
    ])
    print(f"발견된 PDF: {pdf_files}")

    # index.html 읽기
    html_path = os.path.join(REPO_DIR, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    btn_container = soup.find('div', class_='btn-container')
    tally_btn = soup.find('a', href=TALLY_URL)

    # btn-container 초기화
    btn_container.clear()

    # PDF 버튼 자동 생성 (절대 URL 형식)
    for pdf in pdf_files:
        display_name = pdf.replace('.pdf', '').replace('_', ' ')
        href = f"{SITE_BASE_URL}/{pdf}"
        new_btn = soup.new_tag('a', href=href, **{'class': 'btn', 'target': '_blank'})
        new_btn.string = display_name
        btn_container.append(new_btn)
        print(f"버튼 추가: {display_name} → {href}")

    # 수동 버튼 추가 (PDF 뒤, 방명록 앞)
    for title, href in CUSTOM_BUTTONS:
        new_btn = soup.new_tag('a', href=href, **{'class': 'btn'})
        new_btn.string = title
        btn_container.append(new_btn)
        print(f"수동 버튼 추가: {title} → {href}")

    # 규칙 2: 방명록 버튼은 항상 마지막 순서로 유지
    if tally_btn:
        btn_container.append(tally_btn)

    # index.html 저장
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print("index.html 업데이트 완료")

    # 규칙 3: Git 동기화
    run_git(['add', '.'])
    run_git(['commit', '-m', '[Auto Deploy] Update pdf list and HTML'])
    run_git(['push', 'origin', 'main'])
    print("GitHub 푸시 완료 → Vercel 자동 배포 시작!")


if __name__ == '__main__':
    update_site_and_push()
