Unmaintained
============

Da der Vorschlag nun umgesetzt wird, schließe ich weitere Entwicklungen hier aus. 



ft:pedia Volltextsuche
======================

Vorschlag für eine alternative Volltextsuche über die ft:pedia Ausgaben basierend auf
[Xapian](https://xapian.org/). 


Installation
------------

Das Repository bringt außer der Volltext-Datenbank und dem Xapian Modul alles mit.

Die Xapian-Bindings lassen sich wie folgt installieren:

```shell
pip install sphinx xapian-bindings
```

Anschließend läßt sich die Volltext-Datenbank mit

```shell
python fulltext.py
```

erzeugen und die Weboberfläche mit 

```shell
python ftpediasearch.py
```

aufrufen.

Die Adresse "http://127.0.0.1:8080/" kann anschließend im Browser aufgerufen werden.


Grundsätzliches Vorgehen
------------------------

Zunächst müssen die PDF-Dateien in Textdateien umgewandelt werden. Das Script ```make_texts.py``` 
nimmt an, dass die PDFs in dem Verzeichnis ```./ftpedia_data/``` liegen und legt die Resultate
in ```./ftpedia_txt/``` ab. 

Das vorgenannte Script ```fulltext.py``` übernimmt das Erstellen der Datenbank sowie die
Suche. ```ftpediasearch.py``` dient lediglich der Demonstration.


Quellen
-------
[ft:pedia](https://ftcommunity.de/ftpedia/)

[ft:pedia Volltextsuche](https://ftcommunity.de/search/ftpedia-search/)

[CSV-Datei](https://ftcommunity.de/ftpedia/overview/)


