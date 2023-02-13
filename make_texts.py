#!/usr/bin/env python3
import re
import subprocess
import ftmedia


_FTPEDIA_PATTERN = re.compile(r'(?:^|\b)ft:pedia\n', re.MULTILINE)
_ABB_PATTERN = re.compile(r'^Abb\.[^\n]+\n', re.MULTILINE)
_ISSUE_PATTERN = re.compile(r'(?:^|\b)Heft\s+[^\n]+\n', re.MULTILINE)
_PAGE_PATTERN = re.compile(r'^\d{1,3}\n', re.MULTILINE)


def clean_text(txt: str) -> str:
    """\
    Removes some from the given string.
    """
    res = _FTPEDIA_PATTERN.sub('', txt)
    res = _ABB_PATTERN.sub('', res)
    res = _ISSUE_PATTERN.sub('', res)
    res = _PAGE_PATTERN.sub('', res)
    return res


for article in ftmedia.read_overview('ftpedia_articles.csv'):
    first_page, last_page = map(str, article.pages)
    txt = subprocess.check_output(['pdftotext', '-f', first_page, '-l', last_page,
                                   './ftpedia_data/ftpedia-%s.pdf' % article.issue, '-']).decode('utf-8')
    with open('./ftpedia_txt/%s-p-%s-%s.txt' % (article.issue, first_page, last_page), 'w') as f:
        f.write(clean_text(txt))
