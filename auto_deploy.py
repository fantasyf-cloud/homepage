import os
import subprocess
from bs4 import BeautifulSoup


def update_site_and_push():
    # 규칙 1: PDF 파일 목록 탐색
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]

    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    btn_container = soup.find('div', class_='btn-container')
    tally_btn = soup.find('a', href='https://tally.so/r/b5DN4g')

    # btn-container 초기화
    btn_container.clear()

    # PDF 버튼 자동 생성
    for pdf in sorted(pdf_files):
        title = pdf.replace('.pdf', '')
        new_btn = soup.new_tag('a', href=pdf, **{'class': 'btn', 'target': '_blank'})
        new_btn.string = title
        btn_container.append(new_btn)

    # 규칙 1: 방명록 버튼은 항상 마지막 순서로 유지
    if tally_btn:
        btn_container.append(tally_btn)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    # 규칙 3: Git 동기화
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', '[Auto Deploy] Update pdf list and HTML'])
    subprocess.run(['git', 'push', 'origin', 'main'])


if __name__ == '__main__':
    update_site_and_push()
