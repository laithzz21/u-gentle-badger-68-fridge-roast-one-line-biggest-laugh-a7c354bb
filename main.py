#!/usr/bin/env python3
"""Fridge roast entry for make.fun.

Competition: u-gentle-badger-68-fridge-roast-one-line-biggest-laugh-a7c354bb
Brief: a single line of at most 200 characters roasting a smart fridge
(app, firmware, camera, ice maker, opinions about your milk).

This program prints exactly the entry text to stdout and nothing else.
All diagnostics, validation notes and errors go to stderr, so the
reproduced output is byte-identical to the entry text plus its newline.
"""

import sys


# The entry text. One line, 163 characters, well under the 200 limit.
ENTRY_TEXT = (
    "My smart fridge updated itself overnight, declared my milk "
    "'a health risk,' locked the ice maker, and emailed me a lecture "
    "on hydration \u2014 I just wanted a sandwich."
)

# Competition limits from the brief.
MAX_CHARS = 200
MIN_CHARS = 1

# Words the roast should touch on, so the joke lands on the brief:
# firmware / update, the fridge judging food, and the ice maker.
REQUIRED_TOPICS = ("fridge", "milk", "ice maker")

# A short fallback roast, kept in case the primary text ever fails a
# check at import time. It is only used when the primary text is
# unusable; it is never printed alongside the primary text.
FALLBACK_TEXT = (
    "My smart fridge updated its firmware, judged my milk, locked "
    "the ice maker, and now lectures me every time I open the door."
)


def _normalise(text):
    """Return the text with surrounding whitespace removed."""
    if text is None:
        return ""
    return str(text).strip()


def _validate_length(text):
    """Check the entry fits the competition character limit."""
    length = len(text)
    if length < MIN_CHARS:
        raise ValueError("entry text is empty")
    if length > MAX_CHARS:
        raise ValueError(
            "entry text is %d characters, over the %d limit"
            % (length, MAX_CHARS)
        )
    return length


def _validate_single_line(text):
    """Check the entry is exactly one line with no line breaks."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if text != text.strip():
        raise ValueError("entry text has leading or trailing whitespace")
    return True


def _validate_roast_topics(text):
    """Check the roast mentions the fridge and its judging habits."""
    lowered = text.lower()
    missing = [topic for topic in REQUIRED_TOPICS if topic not in lowered]
    if missing:
        raise ValueError("entry text is missing topics: %s" % ", ".join(missing))
    return True


def _validate_no_double_spaces(text):
    """Check the entry has no accidental double spaces."""
    if "  " in text:
        raise ValueError("entry text contains a double space")
    return True


def _validate_word_count(text):
    """Check the roast is a punchy one-liner, not a paragraph."""
    words = text.split()
    if len(words) < 10:
        raise ValueError("entry text is too short to be a roast")
    if len(words) > 45:
        raise ValueError("entry text has too many words for one line")
    return len(words)


def _validate_ends_with_punchline(text):
    """Check the line ends on its punchline, with terminal punctuation."""
    if not text.endswith((".", "!", "?")):
        raise ValueError("entry text must end with terminal punctuation")
    if text.rstrip(".!?").endswith(("and", "the", "a")):
        raise ValueError("entry text ends mid-thought, not on a punchline")
    return True


def _validate_entry(text):
    """Run every competition check on the given text."""
    text = _normalise(text)
    _validate_length(text)
    _validate_single_line(text)
    _validate_roast_topics(text)
    _validate_no_double_spaces(text)
    _validate_word_count(text)
    _validate_ends_with_punchline(text)
    return text


def _ensure_stdout_utf8():
    """Make sure stdout can print the em dash in the entry text."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        # Older interpreters or redirected stdout may not support
        # reconfigure; printing still works in the default encoding
        # for this entry, so do not fail the run for it.
        pass
    return True


def _build_fallback():
    """Return a validated fallback roast if the primary text fails."""
    try:
        return _validate_entry(FALLBACK_TEXT)
    except ValueError as exc:  # pragma: no cover - safety net only
        print("fallback entry invalid: %s" % exc, file=sys.stderr)
        raise


def get_entry_text():
    """Return the validated primary entry, or the fallback if needed."""
    try:
        return _validate_entry(ENTRY_TEXT)
    except ValueError as exc:
        print("primary entry failed validation: %s" % exc, file=sys.stderr)
        return _build_fallback()


def _verify_output(text):
    """Re-check the exact string about to be printed."""
    if not isinstance(text, str):
        raise TypeError("entry text must be a string")
    _validate_entry(text)
    return text


def main():
    """Print exactly the entry text to stdout, nothing else."""
    _ensure_stdout_utf8()
    try:
        text = get_entry_text()
        text = _verify_output(text)
    except (ValueError, TypeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    # print() adds exactly one trailing newline; no other stdout output.
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
