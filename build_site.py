#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Builds the search page for GitHub Pages: copies web/index.html into _site/
# and writes every vocabulary entry, with its search keys, to _site/vocabolario.json

import json
import os
import re
import shutil
import sys

from vocabolario_latinum import read_vocabulary, keys_for

root = os.path.dirname(os.path.abspath(__file__))

# (long label, short label) for files that are not a numbered lesson
labels = {
    'composti_ferre': ('Composti di ferre', 'Comp. ferre'),
    'composti_ire': ('Composti di īre', 'Comp. īre'),
}


def lesson_labels(lesson):
    # "L_07" → "Lezione 7"
    match = re.fullmatch(r'L_(\d+)', lesson)
    if match:
        number = int(match.group(1))
        return f'Lezione {number}', f'Lez. {number}'
    return labels.get(lesson, (lesson.replace('_', ' '),) * 2)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, '_site')
    entries = read_vocabulary()

    # lessons in file order, leaving out empty files
    lessons = []
    for lesson_list in entries.values():
        for lesson in lesson_list:
            if lesson not in lessons:
                lessons.append(lesson)

    data = {
        'lessons': [dict(zip(('id', 'label', 'short'), (lesson, *lesson_labels(lesson)))) for lesson in lessons],
        'entries': [
            {'term': term, 'def': definition, 'lessons': lesson_list, 'keys': keys_for(term)}
            for (term, definition), lesson_list in entries.items()
        ],
    }

    os.makedirs(out, exist_ok=True)
    shutil.copy(os.path.join(root, 'web', 'index.html'), out)
    with open(os.path.join(out, 'vocabolario.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f"{len(data['entries'])} entries from {len(lessons)} files → {out}")


if __name__ == '__main__':
    main()
