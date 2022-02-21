import concurrent
from concurrent.futures.thread import ThreadPoolExecutor

import imdb
from imdb import IMDb
import json
import re

from src.imdbscraper.qrmanager import QRManager


class Repository():
    ia: imdb

    def __init__(self, ia: imdb):
        self.ia = ia

    def get_movie(self, movie_id, info):
        return self.ia.get_movie(movie_id, info)

    def update(self, movie, param):
        return self.ia.update(movie, param)


class Scraper:

    def __init__(self, _logger):
        self._logger = _logger
        self._ia = IMDb()
        self.repository = Repository(self._ia)
        self.qr_manager = QRManager()

    def runList(self, movie_id_list):
        # movies = []
        # for i in movie_id_list:
        #     movies.append(self.run(i))
        # print(json.dumps(movies))
        results = []
        with ThreadPoolExecutor(max_workers=2) as pool:
            for each in pool.map(self.run, movie_id_list):
                results.append(each)
        dumps = json.dumps(results)
        print(dumps)
        with open("out.json", "w") as f:
            f.write(dumps)

    def runListWithMovies(self, movie_list):
        self.runList([i.movieID for i in movie_list])

    def run(self, movie_id):
        print(f"{movie_id} Calling get movie")
        movie = self.repository.get_movie(movie_id, info=('main', 'plot', 'parents_guide'))
        print(f"{movie_id} Ending get movie")
        return self.process_movie(movie, movie_id)

    def process_movie(self, movie, movie_id):
        # {
        #     "count": "1",
        #     "color": "black",
        #     "title": "Death Note",
        #     "icon": "clapperboard",
        #     "contents": [
        #         "text | An intelligent high school student goes on a secret crusade to eliminate criminals from the world after discovering a notebook capable of killing anyone whose name is written into it.",
        #         "rule",
        #         "property | Rating | 9.0/10",
        #         "fill | 10",
        #         "picture | data:image/gif;base64,R0lGODlhhACEAJEAAAAAAP///wAAAAAAACH5BAEAAAIALAAAAACEAIQAAAL/jI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8chQNf2jeeIvec+5PsdgsQgpYi89WjLJDDJHEKdkynVwJNCn1ut1Vj9EptNJPcaEI/DUUsWq/OSF0LFO13D3M/6vPcO6GcXN9iGZ3gkGLHHBlCmGIj4pzgHJynB6JC5CEl46ChH51n52XfZEAlmCarZ2VWoWjqJQ8o3qxTaamjFYJb7WSeL6Rq7Scorurb6SPtruxps/IsMG01sfdp77ZmaehZ8vN283MiMSw5N/D06LX4uzLlbFD4Or62c4H2rPyyP363ugS9Y9IpREuiOXwVqwNiha1hPGsF9Ad1MMbcJYMSD/7pYQXwnEdVFiqc0guQo0p/BbAhffcyYsGI8j4lKOsyHEqPMmjRb9uz38+OzlCuDDj1aLtm7e0ZJegzJlKepoOCUrtvIsiNPNSdVFvzajmu9q2LBPlSIVuxYn2q9hn0qM23bnErnmoUnF65KuzKEvjVZqy8JbHq7GhaMgrC5xc4Qi1B8i/FDwYCdBq6GsurEzX6BSn65s27mm5fxkrYa2XJjzDbXci4I9W9Mtx1husbZunDs16lZx9rKbaTWC7aXOt2Nu+hAolOZFl8OHCuaqMRH32YY3TB01BZpJ6981rpx3+AzKPwMeXJvooSRU1efbm9c8SGXa14YOr7u+bnrz/9bL5Vqw+lnH31qIDUgaFmZJkZpfCU41HacceVgWwgyJyCGBP4Hn4LTcTeTf9cF1x+JTdVGF1AijteZPRm6B2B1t32GnoHSTQWjb2Q5l5+Hpe24QXnvtXjXeTFuuCBsKTLIYl4VjohPhKeFB2Vhd9GYoZQzypZbkTZSxeFMNVa5IlntzXZicmM2OaWL5JloEnLl3Xffj8e5o1OSXO5X4oIrFihdnSAKiuKNIGKp35ABJipjUYoeSeRqYkJqZo/PffmoZ5SyZWKmkTLKm6YTwinehRK2mKObTAop6ZO/rZdqcWvK6hOPZPZoKp6Qlinard5xwOqo3p1KK5JpLvqpmm//5Qlml1kGqWuCedFZ6rMaBKsslXyy6ayxzcFK6pZvdpttud+CimqYlZLrKrDRphslp1V6mqqS8t3Loq3cNstvYktiJ+8X55bwp7oBAywqwf8KF+KBjfrrJ8Prfpiwu3pqG+fCc7lk8bF7Mjvxxksiq6V2bYrMMbQXr4pmyCg7Nu62sWoscF+AvlpxrxS3cDOhGrIn8Qs9t+kpsz4bzfC0NN+8Jo4WLrupsUr/2siDTCL6XZhzjqwzhVCjq2968Hoc6qQd+sxroduSnNTZJ9MMJNi1Piwp2nAHjHXRc7strqp2onv0nkZ6O+hNXneILNNdVyu31J2qLLOlBmP8peLXtLZc9+Qs94lGvYLzd9iLhmN66N4+fvw5vvSOvnLGwz5OeOOqUts65pS//g/r/BZr9unaguBk6b+37fvVHwRf9uA/W+433cMnj2vhuVN9Oe79Sk928xB+Xby9VnLPds7Pd4/6+DOv3G7q1wMO+sDhGx97uWIr77JLcjK+PP7nb/y3ua2CD0AVPQ1xwtMe/OTHtZgx5H7swt6QPAezCEpwghSsoAUviMEManCDHOygBz8IwhcUAAA7"
        #     ],
        #     "tags": [],
        #     "icon_back": "ace",
        #     "background_image": "https://m.media-amazon.com/images/M/MV5BODkzMjhjYTQtYmQyOS00NmZlLTg3Y2UtYjkzN2JkNmRjY2FhXkEyXkFqcGdeQXVyNTM4MDQ5MDc@._V1_.jpg"
        # }
        airDate, icon, kind, seasons, title, episodes = self.define_movie_info(movie)
        cover_image = self.define_cover_image(movie)
        color = self.define_show_color(movie)
        self.qr_manager.write_qr(movie_id, title, kind)
        x = {
            "count": 1,
            "title_size": "11",
            "color": color,
            "title": title,
            "icon": icon,
            "contents": [
                f"property | Genre | {', '.join(movie.data['genres'][0:3])}",
                "rule" if "plot" in movie.data else "",
                f"text | {movie.data['plot'][0].replace('(qv)', '').replace('_', '')}" if "plot" in movie.data else "",
                "rule" if "plot" in movie.data else "",
                f"property | Runtime | {movie.data['runtimes'][0]} minutes" if "runtimes" in movie.data else "",
                airDate,
                seasons,
                episodes,
                f"property | MPAA | {movie.data['mpaa'].split('for')[0]}" if "mpaa" in movie.data else "",
                "fill | 10",
                f"picture | {self.qr_manager.get_qr_path(self.qr_manager.get_filename(movie_id, title, 'final'))}"
            ],
            "background_image": cover_image,
        }
        return x

    def define_movie_info(self, movie):
        print(movie)
        kind = movie.data["kind"]
        title = movie.data["localized title"]
        isMovie = kind == "movie"
        isTvSeries = kind == "tv series"
        icon = ""
        airDate = ""
        seasons = ""
        episodes = ""
        if isMovie:
            icon = "clapperboard"
            if 'original air date' in movie.data:
                airDate = f"property | Original Air Date | {movie.data['original air date']}"
        if isTvSeries:
            print(f"{movie.movieID} Updating with episodes")
            self.repository.update(movie, 'episodes')
            print(f"{movie.movieID} End updating with episodes")
            icon = "tv"

            if 'series years' in movie.data:
                airDate = f"property | Series Years | {movie.data['series years']}"
            if 'seasons' in movie.data:
                seasons = f"property | Seasons | {len(movie.data['seasons'])}"
            ep = movie.data['episodes']
            episodes = f"property | Episodes | {sum([len(ep[x]) for x in ep])}"

        return airDate, icon, kind, seasons, title, episodes

    def define_cover_image(self, movie):

        cover_image = ""
        if "full-size cover url" in movie.data:
            cover_image = movie.data["full-size cover url"]
        elif "cover url" in movie.data:
            cover_image = movie.data["cover url"]
            # the following upscales the image
            cover_image = re.sub("\._V1.*", "._V1_QL75_UX300_CR0,3,300,440_.jpg", cover_image)
        return cover_image

    def define_show_color(self, movie):
        def check_genre(list_in):
            return list_in.intersection([x.lower() for x in movie.data["genres"][0:3]])

        color = 'black'

        if check_genre({
            "action",
            "adventure",
        }):
            color = "#800000"
        if check_genre({
            "sci-fi",
            "fantasy",
        }):
            color = "#337c18"

        if check_genre({
            "documentary",
            "reality tv",
        }):
            color = "#1611ba"
        if check_genre({
            "drama",
        }):
            color = "#8b00b5"
        if check_genre({
            "crime",
            "thriller",
        }):
            color = "#10404F"
        if check_genre({
            "romance",
        }):
            color = "#de5b87"
        return color
