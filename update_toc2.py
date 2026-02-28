import os
import re

def create_anchor(text):
    anchor = re.sub(r'[^\w\s가-힣-]', '', text).strip()
    anchor = re.sub(r'[\s]+', '-', anchor)
    return anchor

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    toc_items = [
        "노트북LM 완전정복",
        "소스추가",
        "웹 또는 리서치 자료에서 실패한 소스 삭제하기",
        "소스 품질 검사",
        "소스 목록 분류",
        "'Key Reference(핵심 참고문헌)'를 선정",
        "핵심 참고 문헌의 정열 순서 변경",
        "특정 참고 문헌과 연관된 보고서 매칭",
        "대화를 나눈 결과를 다시 소스로 추가하기",
        "소스: 텍스트",
        "비주얼 및 글자깨짐 방지(최소화) 프롬프트",
        "채팅 맞춤 설정",
        "노트북LM의 크롬의 확장을 통한 이미지 프롬프트 추가 활용",
        "구글AI스튜디오에서 슬라이드 내용을 오브젝트로 분리하기",
        "캡처 도구와 그림판 활용하기",
        "Gemini Gem x Notebook LM",
        "Opal 앱 만들기"
    ]
    
    new_toc_lines = ["## 목차 (Table of Contents)", ""]
    for item in toc_items:
        anchor = create_anchor(item)
        new_toc_lines.append(f"- [{item}](#{anchor})")

    new_toc_block = "\n".join(new_toc_lines) + "\n\n---\n"
    
    pattern = re.compile(r'## 목차 \(Table of Contents\).*?---\s*\n', re.DOTALL)
    content_no_toc = pattern.sub('', content)
    
    for item in toc_items:
        anchor = create_anchor(item)
        
        # Ensure we only inject anchor once
        anchor_tag = f'<a id="{anchor}"></a>'
        if anchor_tag not in content_no_toc:
            idx = content_no_toc.find(item)
            if idx != -1:
                content_no_toc = content_no_toc[:idx] + anchor_tag + content_no_toc[idx:]
            else:
                print(f"Warning: Could not find '{item}' in the document.")

    lines = content_no_toc.split('\n')
    insert_idx = 0
    if len(lines) > 0 and lines[0].startswith('# '):
        insert_idx = 1
        while insert_idx < len(lines) and lines[insert_idx].strip() == '':
            insert_idx += 1
            
    final_content = '\n'.join(lines[:insert_idx]) + '\n' + new_toc_block + '\n'.join(lines[insert_idx:])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"Successfully processed {filepath}")

if __name__ == "__main__":
    process_file(r"c:\Users\USER\.gemini\antigravity\lecture-materials\export\part1\커플 컨설턴트를 위한 AI 강좌 2f531092d98980cfbc95f3df2a3cd793.md")
