import logging
import sys

from imdb import IMDb

from src.imdbscraper.scraper import Scraper

"https://www.imdb.com/list/ls057577566/"
best_anime = [
    "0077013",
    "0078560",
    "0078570",
    "0081954",
    "0090479",
    "0091211",
    "0092386",
    "0096633",
    "0096686",
    "0106076",
    "0112159",
    "0112166",
    "0122356",
    "0138919",
    "0142183",
    "0159145",
    "0159172",
    "0159175",
    "0159208",
    "0168371",
    "0182629",
    "0182646",
    "0185133",
    "0196050",
    "0203082",
    "0205410",
    "0213338",
    "0251439",
    "0279077",
    "0286390",
    "0290223",
    "0296435",
    "0315008",
    "0318871",
    "0318898",
    "0326672",
    "0327386",
    "0346314",
    "0367439",
    "0380113",
    "0409630",
    "0421357",
    "0423731",
    "0434706",
    "0435961",
    "0437719",
    "0444745",
    "0444953",
    "0480489",
    "0481256",
    "0482855",
    "0488477",
    "0495212",
    "0500092",
    "0765491",
    "0807832",
    "0816397",
    "0816398",
    "0816407",
    "0845738",
    "0857297",
    "0877057",
    "0878036",
    "0928099",
    "0948103",
    "0962826",
    "0985344",
    "0989778",
    "0994314",
    "0995941",
    "10233448",
    "1029248",
    "1118804",
    "1132203",
    "1158671",
    "1169193",
    "1202625",
    "1203269",
    "1209386",
    "1279024",
    "1324968",
    "1334722",
    "1347975",
    "1352421",
    "1480925",
    "1584000",
    "1610860",
    "1690397",
    "1745240",
    "1847445",
    "1910272",
    "1945730",
    "1992935",
    "2061551",
    "2069441",
    "2098220",
    "2359704",
    "4279012",
    "4508902",
    "9335498",
]


class Runtime:

    def __init__(self, _logger):
        self._scraper = Scraper(_logger)
        self._logger = _logger

    def setup_logging(self, loglevel):
        logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
        logging.basicConfig(
            level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
        )

    def run(self, args):
        self.setup_logging(args.loglevel)
        self._logger.debug("Starting crazy calculations...")
        # self._scraper.runList([
        #      '6685272',  # repair
        #      '0133093',  # matrix
        #     '0877057',  # deathnote
        #     '2250912', '6320628', '10872600', # spiderman
        #      '1334722', # baccano
        #      '0948103', # gurrenn lagaan
        #     "0109830",
        #
        #     "0137523",
        # ])
        self._scraper.runList(best_anime)
        # self._scraper.runListWithMovies(IMDb().get_top250_movies())
        self._logger.info("Script ends here")
