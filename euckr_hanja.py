import hanja

def process_line(line):
    # 탭으로 분할하여 첫 번째 값(16진수 번호)과 글자들을 분리
    parts = line.strip().split('\t')

    # 첫 번째 값은 16진수 번호로 해석 (필요시 사용할 수 있음)
    hex_number = parts[0]

    # 나머지 글자들에 대해 각각 EUC-KR로 인코딩하고 16진수로 변환
    results = []
    for character in parts[1:]:
        # 빈 문자열인 경우 무시
        if character:
            # 한 글자에 대해 EUC-KR 인코딩 (2바이트)
            encoded_bytes = character.encode('euc-kr')
            # 각 글자의 인코딩 값을 16진수로 변환
            hex_value = f'{encoded_bytes[0]:02X}{encoded_bytes[1]:02X}'
            # 배열에 글자와 16진수 값을 튜플로 저장
            results.append((character, hex_value, hanja.translate(character, 'substitution')))
    
    return results

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 각 라인을 처리
            result = process_line(line)

            # 결과를 출력 파일에 쓰기
            for char, hex_val, hangeul in result:
                outfile.write(f'{char}: {hex_val}: {hangeul}\n')

# 사용 예시
input_file = 'codes.txt'
output_file = 'output2.txt'
process_file(input_file, output_file)