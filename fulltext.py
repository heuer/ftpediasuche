#
# Fulltext index of ft:pedia issues.
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
import json
import xapian
import ftmedia

_STEMMER_NAME = 'german2'
_PREFIX_CAT = 'XCAT'
_PREFIX_YEAR = 'XY'


def create_fulltext_db(db_path, csv_path, text_path) -> None:
    """\
    Creates a fulltext index database.

    :param db_path: Path to the fulltext index.
    :param csv_path: Path to the CSV file.
    :param text_path: Path to the text files containing the text of an article. The directory should contain text
        files with the pattern 'YYYY-ISSUE_NUMBER-page-{FIRST_PAGE}-{LAST_PAGE}.txt'
    """
    db = xapian.WritableDatabase(db_path, xapian.DB_CREATE_OR_OPEN)
    term_generator = xapian.TermGenerator()
    term_generator.set_stemmer(xapian.Stem(_STEMMER_NAME))
    for article in ftmedia.read_overview(csv_path):
        doc = xapian.Document()
        term_generator.set_document(doc)
        page_first, page_last = article.pages
        category = article.category
        main_category = article.main_category
        title, year, issue_no = article.title, int(article.issue[:4]), int(article.issue[5:])
        identifier = f'{article.issue}-page-{page_first}-{page_last}'
        categories = f'{main_category} {category}'.lower()
        url = f'https://www.ftcommunity.de/ftpedia/{year}/{article.issue}/ftpedia-{article.issue}.pdf#page={page_first}'
        term_generator.index_text(title, 1, 'S')
        term_generator.index_text(categories, 1, _PREFIX_CAT)
        term_generator.index_text(str(year), 1, _PREFIX_YEAR)
        authors = []
        for author in article.authors:
            term_generator.index_text(author, 1, 'A')
            term_generator.increase_termpos()
            authors.append(author)
        term_generator.index_text(title)
        term_generator.increase_termpos()
        term_generator.index_text(categories)
        term_generator.increase_termpos()
        with open(f'{text_path}/{year}-{issue_no}-p-{page_first}-{page_last}.txt') as f:
            content = f.read()
            term_generator.index_text(content)
        doc.add_boolean_term(f'U{url}')
        doc.add_boolean_term(f'Q{identifier}')
        doc.add_value(0, xapian.sortable_serialise(year))
        doc.set_data(json.dumps(dict(title=title, authors=authors, url=url, issue=article.issue, pages=article.pages,
                                     main_category=main_category, category=category, year=year, issue_number=issue_no,
                                     content=content.strip())))
        db.replace_document(f'Q{identifier}', doc)
    db.flush()
    db.close()


def search_fulltext_db(db_path, query: str, offset: int = 0, pagesize: int = 10) -> dict:
    """\
    Searches the fulltext index.

    :param db_path: Path to the fulltext index.
    :param query: The query.
    :param offset: Starting point within the result set
    :param pagesize: Number of records.
    """
    db = xapian.Database(db_path)
    parser = xapian.QueryParser()
    stemmer = xapian.Stem(_STEMMER_NAME)
    parser.set_stemmer(stemmer)
    parser.set_stemming_strategy(parser.STEM_SOME)
    parser.add_rangeprocessor(xapian.NumberRangeProcessor(0))
    parser.add_prefix('title', 'S')
    parser.add_prefix('author', 'A')
    parser.add_prefix('category', _PREFIX_CAT)
    parser.add_prefix('year', _PREFIX_YEAR)
    q = parser.parse_query(query)
    enquire = xapian.Enquire(db)
    enquire.set_query(q)
    mset = enquire.get_mset(offset, pagesize)
    res = {'match_count': mset.get_matches_estimated()}
    matches = []
    res['matches'] = matches
    for match in mset:
        match_data = json.loads(match.document.get_data())
        content = match_data.pop('content')
        match_data['highlighted'] = mset.snippet(content, 500, stemmer).decode('UTF-8')
        matches.append(match_data)
    return res


if __name__ == '__main__':
    create_fulltext_db('./ft/', 'ftpedia_articles.csv', text_path='./ftpedia_txt/')
