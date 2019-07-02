import math
from typing import Optional

LETTER_NAMES = '''
    Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima
    Mike November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey
    Xray Yankee Zulu
'''.strip().split()

DIGIT_NAMES = 'Zero One Two Three Four Five Six Seven Eight Nine'.split()


class OrdinalNames:

    def __init__(self, _range: Optional[int] = None):
        if _range:
            self._digits = math.ceil(math.log10(_range / 26))
        else:
            self._digits = 0

    def __getitem__(self, num: int) -> str:
        parts = [LETTER_NAMES[num % 26]]
        num //= 26
        digits = 0
        while num > 0 or digits < self._digits:
            parts.append(DIGIT_NAMES[num % 10])
            num //= 10
            digits += 1
        return ' '.join(parts)


if __name__ == '__main__':
    import sys

    def usage():
        print('Usage:', __file__, '<count>', file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        usage()
    try:
        count = int(sys.argv[1])
    except ValueError:
        usage()

    names = OrdinalNames(count)
    for i in range(0, count):
        print(names[i])
