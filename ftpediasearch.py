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
from functools import partial
from bottle import Bottle, run, request, response, SimpleTemplate
from fulltext import search_fulltext_db

app = Bottle()

search = partial(search_fulltext_db, db_path='./ft/', pagesize=10)


@app.route('/')
def index():
    query = request.query.q
    page = int(request.query.page or '1')
    offset = (page - 1) * 10
    result = dict(match_count=0, matches=[])
    add_prev = offset > 0
    add_next = False
    if query:
        result = search(query=query, offset=offset)
        match_count = result['match_count']
        add_next = match_count > page * 10
        if match_count < offset:
            response.status = 400
            return 'Bad Request'
    return _TEMPLATE.render(query=query, result=result, add_prev=add_prev, add_next=add_next, page=page)


_TEMPLATE = SimpleTemplate("""<!DOCTYPE html>
<html>
  <head>
    <title>ft:pedia Volltextsuche</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <!-- CSS source: https://github.com/dohliam/dropin-minimal-css/blob/gh-pages/min/axist.min.css> License: MIT -->
    <style>:root{--primary:#1524d9;--light-primary:#2332ea;--secondary:#ff2e88;--light-secondary:#fc77b1;--red:red;--black:#212529;--white:#fdfdfd;--dark-gray:#343334;--gray:#616060;--light-gray:#ccc;--lighter-gray:#f6f6f6;--font-sans-serif:system-ui,-apple-system,segoe ui,roboto,ubuntu,helvetica,cantarell,noto sans,sans-serif;--font-monospace:menlo,monaco,lucida console,liberation mono,dejavu sans mono,bitstream vera sans mono,courier new,monospace,serif;--boder-radius:.2rem}*{box-sizing:border-box;margin:0;padding:0;text-rendering:geometricPrecision;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;-webkit-tap-highlight-color:transparent;font-family:var(--font-sans-serif)}html{font-size:calc(16px+((100vw - 600px) / 250));padding:0;text-decoration-skip-ink:"auto";line-height:1.953rem;margin:auto;min-height:100%;overflow-x:hidden;max-width:1140px}body{padding:0;margin:calc((100vh / 25) * 1.563) calc((100vw / 25) * 1.563);background-color:var(--white);color:var(--black);caret-color:var(--black);word-wrap:break-word}h1,h2,h3,h4,h5,h6{margin-bottom:1rem;margin-top:1em;font-weight:bold}h1{font-size:3.052rem;letter-spacing:-0.15rem;line-height:1}h2{font-size:2.441rem;letter-spacing:-0.12rem;line-height:1.2}h3{font-size:1.953rem;letter-spacing:-0.09rem;line-height:1.2}h4{font-size:1.563rem;letter-spacing:-0.06rem;line-height:1.3}h5{font-size:1.25rem;letter-spacing:-0.03rem;line-height:1.4}h6{font-size:1rem;letter-spacing:0;line-height:1.5}p{margin-bottom:1.563rem}p>*:last-child{margin-bottom:0}blockquote{border-left:1px solid var(--light-gray);padding:0 1rem;margin-bottom:1.563rem}a{color:var(--primary);text-decoration:none}@media(hover:hover){a:hover{text-decoration:underline}}small{font-size:.888rem}hr{border:0;height:2px;margin:1rem 0;background:var(--light-gray)}fieldset{border:0;padding:0;margin:0}label,legend{font-weight:bold;display:inline-block}input[type="email"],input[type="text"],input[type="number"],input[type="password"],input[type="date"],input[type="month"],input[type="week"],input[type="datetime"],input[type="datetime-local"],input[type="url"],input[type="search"],input[type="tel"],input:not([type]){display:block;padding:1rem;font-size:1rem;border:2px solid var(--lighter-gray);color:var(--black);appearance:none;border-radius:var(--boder-radius);background-color:var(--lighter-gray);-webkit-appearance:none;-moz-appearance:none}select{display:block;padding:1rem;font-size:1em;border:2px solid var(--lighter-gray);border-radius:var(--boder-radius);color:var(--black);background-color:var(--lighter-gray);appearance:none;-webkit-appearance:none;-moz-appearance:none}textarea{display:block;font-size:1rem;padding:1rem;line-height:1rem;color:var(--black);border-radius:var(--boder-radius);border:2px solid var(--lighter-gray);background-color:var(--lighter-gray);box-sizing:border-box;resize:none;appearance:none;-webkit-appearance:none;-moz-appearance:none}input:focus,select:focus,textarea:focus{outline:0;border:2px solid var(--primary)}input:invalid,select:invalid,textarea:invalid{border:2px solid var(--red);outline:0}input[type="checkbox"]:hover,input[type="radio"]:hover{cursor:pointer}input[type="submit"],input[type="reset"],input[type="button"],button{padding:.5rem 1.25rem;font-size:1rem;border:0;border-radius:var(--boder-radius);color:var(--lighter-gray);height:2.5rem;background-color:var(--primary);-webkit-appearance:none;-moz-appearance:none;font-weight:bold}@media(hover:hover){input[type="reset"]:hover,input[type="submit"]:hover,input[type="button"]:hover,button:hover{cursor:pointer;background-color:var(--light-primary)}}button:focus-visible,input[type="submit"]:focus-visible,input[type="reset"]:focus-visible,input[type="button"]:focus-visible{border-color:var(--light-primary);outline:0}input[disabled],button:disabled{background-color:var(--gray)}table{width:100%;border-collapse:collapse;margin:1.75rem 0;font-variant-numeric:tabular-nums}th,td{vertical-align:top;border-bottom:2px solid var(--light-gray);line-height:15px;padding:15px}th{font-weight:bold;text-align:left;color:var(--dark-gray)}code,pre{font-family:var(--font-monospace);color:var(--dark-gray);background-color:var(--lighter-gray);font-size:.8rem;vertical-align:middle;overflow:scroll;border-radius:var(--boder-radius)}code{white-space:nowrap;vertical-align:baseline;padding:0 .328rem}pre{white-space:pre;margin:.262rem 0;padding:.64rem 1rem}pre::after{content:" "}ul{margin:0;padding:0 1px;list-style:disc outside;font-variant-numeric:tabular-nums}ol{list-style:decimal outside}ol,ul{padding-left:1rem;margin-bottom:1rem}li{list-style-position:inside}kbd{display:inline-block;padding:0 .328rem;font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,Courier,monospace;font-size:.64rem;color:var(--dark-gray);vertical-align:middle;background-color:#f9f9f9;border:solid 1px #d8d8d8;border-bottom:solid 2px #a6a5a6;border-radius:5px}abbr{text-decoration:none;border-bottom:2px dashed #949394}@media(hover:hover){abbr:hover{cursor:help}}</style>
  </head>
  <body>
    <form action="/" method="get">
      <input name="q" type="text" value="{{ query }}" style="width: 40em">
      <input type="submit"> 
    </form>
    <div>
% for match in result['matches']:
  % url = match['url'] 
  <div>
    <h2><a href="{{ url }}">{{ match['title'] }}</a></h2>
    <dl>
      <dt>Autoren</dt>
      % for author in match['authors']:
        <dd>{{ author }}</dd>
      % end
      <dt>ft:pedia Ausgabe</dt>
      <dd>{{ match['issue'] }}</dd>
    </dl>
    <div>{{ !match['highlighted'] }}<div>
  </div>
% end
    </div>
    <div style="margin-top:2em">
% if add_prev:
      <a href="/?q={{ query }}&page={{ page - 1 }}">« Vorherige</a>
% end
% if add_next:
      <a href="/?q={{ query }}&page={{ page + 1 }}">Nächste »</a>
% end
    </div>
  </body>
</html>
""")

run(app)
