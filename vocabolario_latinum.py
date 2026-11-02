#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import unicodedata
from collections import Counter

# The vocabulary files are in the data folder next to this script
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

separator = '—' * 12

# True: CON numero della lezione | False: SENZA numero della lezione
show_lesson = True


def normalize(string):
    # lowercase, strip macrons and breves (ā → a), drop hyphens and punctuation
    string = unicodedata.normalize('NFKD', string.lower())
    string = ''.join(c for c in string if not unicodedata.combining(c))
    string = re.sub(r'[^\w\s]', '', string)
    # "neque ... neque ..." → "neque"
    words = string.split()
    return ' '.join(w for i, w in enumerate(words) if i == 0 or w != words[i - 1])


def variants(term):
    # Text in parentheses is optional: "(ad)monēre" → "admonēre", "monēre"
    match = re.search(r'\(([^()]*)\)', term)
    if not match:
        return [term]
    before, inside, after = term[:match.start()], match.group(1), term[match.end():]
    return variants(before + inside + after) + variants(before + after)


def keys_for(term):
    keys = []
    for variant in variants(term):
        # Alternative forms: "nōlī/nōlīte", "quī? quae? quod?", "Mārcus, Publius"
        for i, part in enumerate(re.split(r'[,/;?!\n]', variant)):
            key = normalize(part)
            # after the first form, short parts are only endings: "īrātus, a, um"
            if not key or (i > 0 and len(key) < 3):
                continue
            candidates = [key]
            # correlatives are split up in a text, so "nē ... quidem" is also found under "ne"
            if '...' in part:
                candidates.append(key.split()[0])
            for k in candidates:
                if k not in keys:
                    keys.append(k)
    return keys


def read_text_file(file_path, lesson, entries):
    with open(file_path, encoding='utf-8') as f:
        for chunk in f.read().split(separator):
            if not chunk.strip():
                continue
            if '—' not in chunk:
                print(f"Skipped entry without '—' in {lesson}: {chunk.strip()}")
                continue
            term, definition = (s.strip() for s in chunk.split('—', 1))
            # an identical entry in several files is shown once, with all its lessons
            entries.setdefault((term, definition), []).append(lesson)


def read_vocabulary():
    # (term, definition) → lessons it appears in, one lesson per file
    entries = {}
    for file in sorted(os.listdir(data_path)):
        if file.endswith('.txt'):
            read_text_file(os.path.join(data_path, file), os.path.splitext(file)[0], entries)
    return entries


def split_phrases(words, index, longest):
    # Longest match first, so "res publica" finds "rēs pūblica" rather than "rēs" + "pūblica"
    phrases = []
    i = 0
    while i < len(words):
        for j in range(min(len(words), i + longest), i, -1):
            phrase = ' '.join(norm for _, norm in words[i:j])
            if phrase in index or j == i + 1:
                phrases.append((' '.join(raw for raw, _ in words[i:j]), phrase))
                i = j
                break
    return phrases


def main():
    entries = read_vocabulary()

    # normalized key → every entry it can stand for ("hic" → hīc and hic)
    index = {}
    for term, definition in entries:
        for key in keys_for(term):
            index.setdefault(key, []).append((term, definition))
    longest = max((len(key.split()) for key in index), default=1)

    while True:
        try:
            val = input("Enter word(s): ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if val.strip().lower() == 'q':
            break

        words = [(raw, normalize(raw)) for raw in re.split(r'[\s,]+', val)]
        words = [(raw, norm) for raw, norm in words if norm]
        phrases = split_phrases(words, index, longest)
        counter = Counter(phrase for _, phrase in phrases)
        # each phrase once, in the order typed
        first_typed = {}
        for raw, phrase in phrases:
            first_typed.setdefault(phrase, raw)

        for phrase, raw in first_typed.items():
            if phrase in index:
                for term, definition in index[phrase]:
                    if show_lesson:
                        lessons = ', '.join(entries[(term, definition)])
                        print(f"{term}\n—\n{definition}\n\nCounter: {counter[phrase]} | [{lessons}]\n{separator}")
                    else:
                        print(f"{term}\n—\n{definition}\n{separator}")
            else:
                # right format for export
                print(f"No match for: {raw}\n—\n+++ Please, insert manually. +++\n\nCounter: {counter[phrase]}\n{separator}")
        print(f'Processed items: {len(words)}')


if __name__ == '__main__':
    main()
