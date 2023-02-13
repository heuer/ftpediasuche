#
# ftmedia - ft:pedia meta data
#
# Written in 2023 by Lars Heuer
#
# To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring
# rights to this software to the public domain worldwide.
#
# This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with this software.
# If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
#
"""\
Tools to generate meta information about ft:pedia articles.
"""
import os
import re
import csv
from itertools import filterfalse, chain
from collections import Counter
from typing import Iterable, Tuple, Optional

_MAIN_CAT = re.compile(r'^([^(]+)\(([^)]+)\)$')
_CLEAN_MINI = re.compile(r'^Mini[^:]+:\s*')

_LATEX_DOC = r"""\documentclass[a4paper,12pt]{book}
\pagestyle{empty}
\usepackage[ngerman]{babel}
\usepackage{pdfpages}
\usepackage[hidelinks]{hyperref}
\renewcommand{\familydefault}{\sfdefault}
\begin{document}
% title %
\tableofcontents
\addtocontents{toc}{\protect\thispagestyle{empty}}
\newpage
% chapters %
\end{document}
"""

_LATEX_TITLE = r"""\begin{titlepage}
\begin{flushright}
{\huge\textbf{\textcolor{red}{f}\textcolor{blue}{t}\textcolor{gray}{:pedia}}\par}
{\large Sonderausgabe\par}
\vspace{4cm}
{\huge\textbf{% title %}\par}
\end{flushright}
\end{titlepage}"""


class ArticleData:
    """\
    Provides information like author(s), category, title, … about a ft:pedia article.
    """
    def __init__(self, issue: str, authors: Tuple[str, ...], category: str, title: str, pages: Tuple[int, int],
                 abstract: str):
        assert len(pages) == 2
        self.issue: str = issue  # ft:pedia issue: YYYY-M
        self.authors: Tuple[str, ...] = authors  # Tuple of length 1…n of authors
        self.category: str = category  # Name of the category
        self.title: str = title  # Title of the article
        self.pages: Tuple[int, int] = pages  # Tuple of length 2 (start page, end page)
        self.abstract: str = abstract

    @property
    def main_category(self) -> str:
        """\
        Returns the main category.

        I.e. 'Sensoren (Computing)' -> 'Computing'
        """
        m = _MAIN_CAT.match(self.category)
        return m.group(2) if m else self.category


def read_overview(src) -> Iterable[ArticleData]:
    """\
    Reads a CSV file with ft:pedia articles and yields the rows.

    The input source must be formatted like the CSV provided by <https://ftcommunity.de/ftpedia/overview/>
    The header is omitted.
    """
    with open(src) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            pg = row[4]
            pages = tuple(int(p) for p in pg.split('–')) if '–' in pg else (int(pg),) * 2
            yield ArticleData(row[0], tuple(author.strip() for author in row[1].split(',')), row[2], row[3], pages,
                              row[5])


def authors(articles: Iterable[ArticleData]) -> Iterable[str]:
    """\
    Returns a unique iterable over the authors of the provided iterable of article data.
    """
    seen = set()
    for author in filterfalse(seen.__contains__, chain.from_iterable(ad.authors for ad in articles)):
        seen.add(author)
        yield author


def author_occurrences(articles: Iterable[ArticleData]) -> dict[str, int]:
    """\
    Returns a dict of author -> number of articles from the provided iterable of article data.
    """
    return Counter(chain.from_iterable(ad.authors for ad in articles))


def remove_minimodel_prefix(title: str) -> str:
    """\
    Removes the "Mini-Modelle (number):" prefix from the title.
    """
    return _CLEAN_MINI.sub('', title)


_TEX_CONV = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
    '\\': r'\textbackslash{}',
    '<': r'\textless{}',
    '>': r'\textgreater{}',
}

_TEX_ESCAPE = re.compile('|'.join(re.escape(str(key)) for key in sorted(_TEX_CONV.keys(), key=lambda item: - len(item))))


def _tex_escape(text: str) -> str:
    """\
    Replaces chars with LaTeX escape sequences iff necessary.
    """
    return _TEX_ESCAPE.sub(lambda match: _TEX_CONV[match.group()], text)


def make_latex_doc(articles: Iterable[ArticleData], data_dir, title: Optional[str] = None) -> str:
    """\
    Returns a LaTeX document as string.
    """
    def pdf_section(article_data: ArticleData) -> str:
        article_title = _tex_escape(article_data.title)
        filename = os.path.join(data_dir, 'ftpedia-' + article_data.issue + '.pdf')
        page_from, page_to = article_data.pages
        return f'\\phantomsection\\addcontentsline{{toc}}{{section}}{{{article_title}}}\n' \
               f'\\includepdf[pages={{{page_from}-{page_to}}}]{{{filename}}}'
    res = _LATEX_DOC.replace('% chapters %', '\n'.join(map(pdf_section, articles)))
    if title:
        res = res.replace('% title %', _LATEX_TITLE.replace('% title %', _tex_escape(title)))
    return res
