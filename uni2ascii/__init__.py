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

import argparse
import logging
import re
import unicodedata
import sys

name = "uni2ascii"

VERSION = "1.2.0"


class Global:
    """Stores globals. There should be no instances of Global."""

    # Map of utf-8=>ascii transliterations. Loaded the first time uni2ascii is called.
    translits = None

    # Regexp of lhs of translits. Loaded the first time uni2ascii is called.
    unicode_re = None

    # Command line args if called as a script
    args = None


def uni2ascii(line):
    """
    Replace unicode characters that look similar to ASCII with their ASCII
    equivalent.
    """

    if Global.translits is None:
        Global.translits = get_translits()
        Global.unicodere = re.compile(
            "|".join(
                map(re.escape, sorted(Global.translits.keys(), key=len, reverse=True))
            )
        )
    return re.sub(
        Global.unicodere,
        lambda mo: Global.translits[mo.group()],
        unicodedata.normalize("NFC", line),
    )


def get_translits():
    """
    Convenience function to make it easy to add translits in place.
    Returns a dict of unicode=>ascii.
    """
    translitstr = """
¡       i
²       2
³       3
⁴       4
⁵       5
⁶       6
⁷       7
⁸       8
⁹       9
⁰       0
❶       1
❷       2
❸       3
❹       4
❺       5
❻       6
❼       7
❽       8
❾       9
❿       10
➀       1
➁       2
➂       3
➃       4
➄       5
➅       6
➆       7
➇       8
➈       9
➉       10
➊       1
➋       2
➌       3
➍       4
➎       5
➏       6
➐       7
➑       8
➒       9
➓       10
´       '
Α       A
À       A
Á       A
Â       A
Ã       A
Ä       A
Å       A
Æ       AE
Β       B
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
Μ       M
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
ă       a
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
‘       '
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
‘       '
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
    for line in translitstr.split("\n"):
        line = line.strip()
        if line.startswith("#") or line == "":
            continue
        (lhs, rhs) = line.split()
        ret[unicodedata.normalize("NFC", lhs)] = rhs

    # The following are various width spaces with various other
    # interpretations (e.g. non-breaking). We render all these as a
    # single space. A codepoint goes here if it separates a word but
    # renders with no pixels, even if it's zero width.

    whites = """ : : : : : : : : :​:‌:‍:⁠: : :　:﻿"""

    for sp in whites.split(":"):
        ret[sp] = " "

    # The following are very thin spaces. They seem to be used for
    # kerning rather than word separation, so we map them to
    # nothing. YMMV.

    nothings = """ : """

    for sp in nothings.split(":"):
        ret[sp] = ""

    return ret


# Below here is the command line interface
def main():
    parse_arguments(sys.argv[1:])
    setup_logging()

    for line in sys.stdin:
        line = uni2ascii(line)

        # If there's remaining non-ascii, handle it according to arguments.
        # The default is to leave the line alone.

        if re.search(r"[^\x00-\x7f]", line):
            if Global.args.e:
                logging.error("Unexpected non-ascii. The line was:\n%s\n", line)
                sys.exit(1)
            if Global.args.X:
                continue
            if Global.args.r or Global.args.x:
                if Global.args.x:
                    replace = ""
                else:
                    replace = Global.args.r
                line = re.sub(r"[^\x00-\x7f]+", replace, line).strip()
        # If we get here, we should print a line
        print(line.encode("ascii", "ignore").decode("utf-8"), end="")


def parse_arguments(strs):
    parser = argparse.ArgumentParser(
        description="Replace utf8 characters that look similar to ASCII with their nearest ASCII equivalent. Version {VERSION}.".format(
            VERSION=VERSION
        )
    )
    parser.add_argument(
        "-loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Logging level (default %(default)s).",
    )
    parser.add_argument("-version", "--version", action="version", version=str(VERSION))
    mogroup = parser.add_mutually_exclusive_group()
    mogroup.add_argument(
        "-r", help="Replace remaining non-ascii characters with this string."
    )
    mogroup.add_argument(
        "-x", help="Remove remaining non-ascii characters.", action="store_true"
    )
    mogroup.add_argument(
        "-X",
        action="store_true",
        help="Silently remove lines containing any remaining non-ascii characters.",
    )
    mogroup.add_argument(
        "-e",
        action="store_true",
        help="Report an error and exit if there are any remaining non-ascii characters.",
    )
    Global.args = parser.parse_args(strs)


def setup_logging():
    numeric_level = getattr(logging, Global.args.loglevel, None)
    if not isinstance(numeric_level, int):
        raise ValueError(
            "Invalid log level: {loglevel}".format(loglevel=Global.args.loglevel)
        )
    logging.basicConfig(
        level=numeric_level,
        format="%(module)s:%(levelname)s:%(asctime)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
