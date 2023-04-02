# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re


def find_floats(string, regex: str = r"^(?<!\d)(\d\.\d{2})(?:\s?%?)?$"):
    matches = re.finditer(regex, string, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                            end=match.end(), match=match.group()))
