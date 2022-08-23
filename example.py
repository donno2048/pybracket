# coding: brackets
from typing import Generator;def get_strings(text: str) -> Generator { # yeah, semicolon can come between any two statements
    flag_quote, flag_double_quote, start = False, False, 0;for i in range(len(text)) { # or even between conditions and loops
        j, odd = i - 1, False
        while text[j] == "\\" {
            j -= 1
            odd = not odd
        } if odd {continue} if not flag_quote and not flag_double_quote { # you can do that now
            if text[i] == "\'" {
                flag_quote, start = True, i
            }
            if text[i] == "\"" {
                flag_double_quote, start = True, i
            }
        }
        elif flag_double_quote {
            if text[i] == "\"" {
                flag_double_quote = False
                yield (start, i + 1)
            }
        }
        elif flag_quote {
            if text[i] == "\'" {
                flag_quote = False
                yield (start, i + 1)
            }
        }
    }
}