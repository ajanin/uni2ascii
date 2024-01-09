# uni2ascii

Convert unicode to closest ASCII equivalent.

There are many unicode glyphs whose appearance is very similar to ASCII characters. This script converts these codepoints to their ASCII equivalent. For example, the string `і lоѵе üńісοdе` contains only 2 ASCII characters, despite the fact that all but `üń` look fine at first glance. To convert to ASCII:

    > echo і lоѵе üńісοdе | uni2ascii
    i love unicode

The default action is to leave untouched any non-ascii that `uni2ascii.py` doesn't know about. This can be overridden with command line arguments. Call `uni2ascii -h` for help.

You can also call from python:

    from uni2ascii import uni2ascii
    ascii_string = uni2ascii('і lоѵе üńісοdе')

It's quite easy to add new transliterations by just copying and pasting offending strings into the code. See the function `get_translits()` in `__init__.py`. Feel free to contact me or do a pull request if you find useful ones that aren't there.

## Notes

`uni2ascii` was written to handle particular data we had on hand. There are plenty of missing transliterations. I'm happy to add new ones!

Input encoding must be utf-8.

Feel free to modify - it's not likely it'll work exactly correctly for you out of the box.

The code will no longer work in python2 -- I added some unicode normalization from `unicodedata` and haven't quite figured out how to make it work in python2 and python3 simultaneously.

This was not designed to thwart homograph attacks, but rather to help with text normalization of English, where unicode sometimes sneaks in.

## Install

    pip install uni2ascii-janin

For the most up to date:

    pip install git+https://github.com/ajanin/uni2ascii.git


## Alternatives

### The Python module `unidecode`

Very similar in spirit, but doesn't handle punctuation and makes some choices I disagree with.

### iconv

If you call `iconv -t //TRANSLIT`, it'll do some of what `uni2ascii` does, but a bunch of stuff is missing that is important to our application.

### Image processing approaches

There have been a few projects that actually look at the generated pixels to determine if two glyphs are too similar. I love the idea, but wanted more fine grain control.
