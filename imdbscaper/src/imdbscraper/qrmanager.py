import subprocess


class QRManager:
    def write_qr(self, movie_id, title, kind):
        # """https://www.imdb.com/title/tt0133093/"""
        filename_imdb = self.get_filename(movie_id, title, "imdb")
        self._write_qr(filename_imdb, f"https://www.imdb.com/title/tt{movie_id}")
        filename_jw = self.get_filename(movie_id, title, "jw")
        self._write_qr(filename_jw, self.get_justwatch_link(title, kind))
        filename_wiki = self.get_filename(movie_id, title, "wiki")
        self._write_qr(filename_wiki, f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}")

        filename_imdb = self.add_label(filename_imdb, "IMDB")
        filename_jw = self.add_label(filename_jw, "JustWatch")
        filename_wiki = self.add_label(filename_wiki, "Wikipedia")

        subprocess.run([
            "convert",
            "+append",
            "-gravity",
            "South",
            filename_imdb,
            filename_jw,
            filename_wiki,
            "data/" + self.get_filename(movie_id, title, "final")
        ])

    def add_label(self, filename, label):
        anno_filename = "data/anno" + filename
        subprocess.run([
            "convert",
            "data/" + filename,
            # "-resize",
            # "70%",
            # "-unsharp",
            # "0.25x0.25+8+0.065",
            "-background",
            "White",
            f"label:{label}",
            "-gravity",
            "Center",
            "-append",
            "-background",
            "White",
            "-bordercolor",
            "White",
            "-border",
            "2x2",
            anno_filename
        ])
        return anno_filename

    def _write_qr(self, filename, url):
        print("writing to " + filename)
        subprocess.run([
            "qrencode",
            "-v", "5",
            "-d", "300",
            "-o",
            f"data/{filename}",
            url
        ])

    def get_filename(self, movie_id, title, type):
        return f"{title}_{type}_{movie_id}.png"

    def get_justwatch_link(self, title, kind):
        if kind == 'tv series':
            kind = 'tv-show'

        def prepare(inner):
            return inner.replace(' ', '-').replace(':', '').lower()

        return f"https://www.justwatch.com/us/{prepare(kind)}/{prepare(title)}"

    def get_qr_path(self, filename):
        return f"file:///Users/pbeagan/Downloads/MyHome/bin/imdbscaper/imdbscraper/src/imdbscraper/data/{filename}"
