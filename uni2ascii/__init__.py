# -*- coding: utf-8 -*-
#
# Convert unicode (encoded as utf-8) to the closest ascii equivalent.
#
# See README.md for more information.
#
# See LICENSE for licensing information.
#
#
# The basic idea is to assemble a regular expression that detects
# unicode that we know about. This happens the first time uni2ascii is
# called.
#
# Most of the meat is in setting up this regular expression, which
# happens in get_translits(). If you find new transliterations, you'd
# add them to get_translits().
#
# Note: I added transliterations and normalizations as I found them in
# our data by copying/pasting into get_translits() below. There are
# surely many more that aren't there yet.  I'm happy to add more!
#


import re
import unicodedata

name = 'uni2ascii'


class Global:
    """Stores globals. There should be no instances of Global."""

    # Map of utf-8=>ascii transliterations. Loaded the first time uni2ascii is called.
    translits = None

    # Regexp of lhs of translits. Loaded the first time uni2ascii is called.
    unicode_re = None

# end class Global


def uni2ascii(line):
    """
    Replace unicode characters that look similar to ASCII with their ASCII
    equivalent.
    """

    if Global.translits is None:
        Global.translits = get_translits()
        Global.unicodere = re.compile('|'.join(map(re.escape,
                                                   sorted(Global.translits.keys(),
                                                          key=len,
                                                          reverse=True))))
    return re.sub(Global.unicodere,
                  lambda mo: Global.translits[mo.group()],
                  unicodedata.normalize('NFC', line))
# end uni2ascii()


def get_translits():
    """
    Convenience function to make it easy to add translits in place.
    Returns a dict of unicode=>ascii.
    """
    translitstr = """
¡       i
²       2
³       3
´       '
À       A
Á       A
Â       A
Ã       A
Ä       A
Å       A
Æ       AE
Ç       C
È       E
É       E
Ê       E
Ë       E
Ì       I
Í       I
Î       I
Ï       I
Ð       D
Ñ       N
Ò       O
Ó       O
Ô       O
Õ       O
Ö       O
×       x
Ù       U
Ú       U
Û       U
Ü       U
Ý       Y
à       a
á       a
â       a
ã       a
ä       a
å       a
æ       ae
ç       c
è       e
é       e
ê       e
ë       e
ì       i
í       i
î       i
ï       i
ñ       n
ò       o
ó       o
ô       o
õ       o
ö       o
ù       u
ú       u
û       u
ü       u
ý       y
ÿ       y
ć       c
ę       e
ğ       g
ģ       g
ī       i
ń       n
ō       o
Œ       OE
œ       oe
š       s
Ÿ       Y
Ž       Z
ƒ       f
ɑ       a
ɡ       g
ʻ       '
̂       ^
̑       ^
ν       v
ο       o
ρ       p
а       a
б       6
е       e
о       o
р       p
с       c
у       y
х       x
ѕ       s
і       i
ј       j
ѵ       v
ӕ       ae
։       :
৪       8
৭       q
੧       q
ଃ       8
୨       9
ᵫ       ue
ṭ       t
‐       -
‒       -
–       -
—       -
―       -
’       '
“       "
”       "
…       ...
′       '
⁄        /
₁       1
₂       2
∕       /
≤       <=
≥       >=
★       *
Ꜳ      AA
ꜳ       aa
ﬀ       ff
ﬁ       fi
ﬃ      ffi
ﬄ      ffl
ﬆ       st
︰      :
"""
    ret = {}
    for line in translitstr.split('\n'):
        line = line.strip()
        if line.startswith('#') or line == '':
            continue
        (lhs, rhs) = line.split()
        ret[unicodedata.normalize('NFC', lhs)] = rhs

    # The following are various width spaces with various other
    # interpretations (e.g. non-breaking). We render all these as a
    # single space. A codepoint goes here if it separates a word but
    # renders with no pixels, even if it's zero width.

    whites = """ : : : : : : : : :​:‌:‍:⁠: : :　:﻿"""

    for sp in whites.split(':'):
        ret[sp] = ' '

    # The following are very thin spaces. They seem to be used for
    # kerning rather than word separation, so we map them to
    # nothing. YMMV.

    nothings = """ : """

    for sp in nothings.split(':'):
        ret[sp] = ''

    return ret
# end translits()
