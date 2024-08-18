def process_changes(input_file, output_file):
    last_hangul = None  # 이전에 읽은 한글 문자

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 라인을 콜론(:)으로 분할하여 16진수 값, 한자, 한글을 추출
            parts = line.strip().split(':')
            if len(parts) != 3:
                continue  # 잘못된 형식의 라인은 무시
            
            hex_value = parts[1].strip()  # 16진수 값
            hanja = parts[0].strip()      # 한자
            hangul = parts[2].strip()     # 한글

            # 현재 한글 문자가 이전 한글 문자와 다른 경우
            if hangul != last_hangul:
                # 변경 내용을 출력 파일에 기록
                if last_hangul is not None:
                    # 변경전 한글 문자의 EUC-KR 16진수 값 계산
                    euc_kr_hex = ''.join([f'{b:02X}' for b in last_hangul.encode('euc-kr')])

                    outfile.write(f'{hex_value}, {euc_kr_hex} - (from {last_hangul} to {hangul}) - {hanja}\n')
                
                # 마지막 한글 문자 및 한자 업데이트
                last_hangul = hangul

# 사용 예시
input_file = 'before_processed_input.txt'
output_file = 'output3.txt'
process_changes(input_file, output_file)
