import os
import re

def create_anchor(text):
    anchor = re.sub(r'[^\w\s가-힣-]', '', text).strip()
    anchor = re.sub(r'[\s]+', '-', anchor)
    return anchor

def process_file_with_back_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

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
    
    # We will look for <a id="..."></a> to find section starts.
    # The end of a section is just before the beginning of the next section, or EOF.
    # We want to insert "[목차 돌아가기](#목차-table-of-contents)" at the end of each section.
    
    # Let's clean up existing back links first
    clean_lines = []
    for line in lines:
        if line.strip() != "[목차 돌아가기](#목차-table-of-contents)" and \
           line.strip() != "[⇧ 목차로 돌아가기](#목차-table-of-contents)":
            clean_lines.append(line)
            
    # Find TOC header to ensure it has an anchor (actually github auto generates id="목차-table-of-contents" for "## 목차 (Table of Contents)")
    
    # We need to find the line numbers where each section starts.
    section_starts = []
    for i, line in enumerate(clean_lines):
        for item in toc_items:
            anchor = create_anchor(item)
            if f'<a id="{anchor}">' in line:
                section_starts.append(i)
                break
                
    # Also add the end of file index
    section_starts.append(len(clean_lines))
    
    new_lines = []
    current_line = 0
    
    for idx in range(len(section_starts) - 1):
        start_idx = section_starts[idx]
        next_start_idx = section_starts[idx + 1]
        
        # Add all lines up to the end of this section
        while current_line < next_start_idx:
            new_lines.append(clean_lines[current_line])
            current_line += 1
            
        # Insert back to TOC link just before the next section
        new_lines.append("\n[목차 돌아가기](#목차-table-of-contents)\n\n")

    # Add any remaining lines
    while current_line < len(clean_lines):
        new_lines.append(clean_lines[current_line])
        current_line += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print(f"Successfully added back links to {filepath}")

if __name__ == "__main__":
    process_file_with_back_links(r"c:\Users\USER\.gemini\antigravity\lecture-materials\export\part1\커플 컨설턴트를 위한 AI 강좌 2f531092d98980cfbc95f3df2a3cd793.md")
