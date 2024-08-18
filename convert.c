#include <stdio.h>
#include <string.h>

// 한자 변환 규칙을 저장하는 이차원 배열
// 배열의 형식: {범위 상한, 변환값}
const unsigned short conversion_rules[][2] = {
    {0xCEC2, 0xB0CC}, // 0xCEC2 미만이면 0xB0CC으로 변환
    // 다른 규칙도 추가 가능
};

// 변환 규칙의 개수
#define RULE_COUNT (sizeof(conversion_rules) / sizeof(conversion_rules[0]))

// 한자가 있는지 확인하는 함수 (임시로 범위를 0xA4-0xFE로 가정)
int is_hanja(unsigned char c1, unsigned char c2) {
    return (c1 >= 0xA4 && c1 <= 0xFE);
}

// 변환 규칙을 적용하는 함수
void apply_conversion_rule(unsigned short combined, unsigned char *c1, unsigned char *c2) {
    for (int i = 0; i < RULE_COUNT; ++i) {
        if (combined < conversion_rules[i][0]) {
            *c1 = (conversion_rules[i][1] >> 8) & 0xFF;
            *c2 = conversion_rules[i][1] & 0xFF;
            break;
        }
    }
}

// 특정 범위에 해당하는 한자 변환 함수
void convert_hanja(unsigned char *str) {
    while (*str) {
        unsigned char c1 = *str;
        unsigned char c2 = *(str + 1);

        // 한자라면, 조건을 체크합니다.
        if (is_hanja(c1, c2)) {
            unsigned short combined = (c1 << 8) | c2;

            // 변환 규칙을 적용합니다.
            apply_conversion_rule(combined, str, str + 1);
        }
        // 다음 문자로 이동 (멀티바이트이므로 2바이트 이동)
        str += 2;
    }
}

int main() {
    unsigned char text[] = {0xB0, 0xA1, 0xC5, 0xD0, 0xCE, 0xC2, 0x00}; // 예시 문자열 (EUC-KR 인코딩)

    printf("Before conversion: ");
    for (int i = 0; i < strlen((char *)text); i++) {
        printf("%02X ", text[i]);
    }
    printf("\n");

    convert_hanja(text);

    printf("After conversion: ");
    for (int i = 0; i < strlen((char *)text); i++) {
        printf("%02X ", text[i]);
    }
    printf("\n");

    return 0;
}
