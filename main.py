#!/usr/bin/env python3
"""Long Roast entry: emit one roast line for the judge.

The program takes no input and no arguments. It checks the roast once
(one line, one sentence, 1-200 characters) and writes it, with no
trailing newline, to entry.txt inside the output directory the harness
provides through MAKEFUN_OUTPUT_DIR.
"""

import os
import sys

ROAST = "My agent asks Gemini to count the characters, Gemini miscounts by five, and my agent thanks it for the help."
LIMIT = 200


def target_dir():
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not folder:
        folder = "out"
    return folder


def sound(line):
    if not line or line != line.strip():
        return "roast is empty or padded with whitespace"
    if "\n" in line or "\r" in line:
        return "roast must stay on one line"
    if line.count(".") != 1:
        return "roast must be exactly one sentence"
    if len(line) > LIMIT:
        return "roast is longer than 200 characters"
    return None


def drop(line, folder):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.chmod(path, 0o644)
    return path


def main(argv):
    if len(argv) != 1:
        print("usage: python3 main.py", file=sys.stderr)
        return 2
    problem = sound(ROAST)
    if problem is not None:
        print("invalid roast: " + problem, file=sys.stderr)
        return 1
    path = drop(ROAST, target_dir())
    print("wrote %d characters to %s" % (len(ROAST), path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
