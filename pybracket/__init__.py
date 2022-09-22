from codecs import register, CodecInfo, BufferedIncrementalDecoder
from encodings import search_function
from functools import reduce
from typing import Generator, Tuple
utf8 = search_function('utf8')
def get_strings(text: str) -> Generator:
    # I've spent around one hour creating and modifying a regex to match that then I just made this function after it didn't work
    flag_quote, flag_double_quote, start = False, False, 0
    # I won't bother matching tripled quotes and double-tripled quotes as I'll just treat any quotes as tripled and let the python error message handle it if the user had a mistake
    for i in range(len(text)):
        j, odd = i - 1, False
        while text[j] == "\\":
            j -= 1
            odd = not odd
        if odd: continue
        if not flag_quote and not flag_double_quote:
            if text[i] == "\'":
                flag_quote, start = True, i
            if text[i] == "\"":
                flag_double_quote, start = True, i
        elif flag_double_quote:
            if text[i] == "\"":
                flag_double_quote = False
                yield (start, i + 1) # returns one more at the end intentionally
        elif flag_quote:
            if text[i] == "\'":
                flag_quote = False
                yield (start, i + 1) # returns one more at the end intentionally
def indexes_to_list(indexes: Generator) -> list:
    return reduce(lambda x, y: x + list(range(*y)), [[]] + list(indexes))
def get_comments(text: str) -> Generator:
    strings = list(get_strings(text))
    for i in range(len(text)):
        if text[i] == "#" and i not in indexes_to_list(strings):
            yield (i, text[i:].find("\n") + i) # returns one more at the end intentionally   
def transform(text: str, indent_level: int = 0) -> str:
    text = text.lstrip()
    if not text: return ""
    irr, output = indexes_to_list(get_strings(text)) + indexes_to_list(get_comments(text)), "\n" + "\t" * indent_level # no need to calc irr each time, could use "index: int = 0" but doesn't matter
    for i in range(len(text)):
        if i not in irr:
            if text[i] == "{":
                return output + ":" + transform(text[i + 1:], indent_level + 1)
            if text[i] == "}":
                return output + transform(text[i + 1:], indent_level - 1)
            if text[i] in ";\n":
                return output + transform(text[i + 1:], indent_level)
        output += text[i] # slow but doesn't matter
    return output
def decoder(text: memoryview, errors='strict') -> Tuple[str, int]:
    output = transform(utf8.decode(text, errors=errors)[0]).lstrip()
    return output, len(output)
class IncrementalDecoder(BufferedIncrementalDecoder):
    def _buffer_decode(self, input, errors, final):
        return decoder(input, errors) if final else ('', 0)
def main():
    register(lambda i: CodecInfo(name='brackets', encode=utf8.encode, decode=decoder, incrementalencoder=utf8.incrementalencoder, incrementaldecoder=IncrementalDecoder) if i == 'brackets' else None)