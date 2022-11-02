import pathlib
import json

import requests
import xmltodict


MAIN_LIBRARY_PATH = pathlib.Path('~/Matrix Root/am. Anime/')
LOCAL_ANIME_LIBRARY_DIR = pathlib.Path('LOCAL_ANIME_LIBRARY/').resolve()
WATCHED_LIST_DIR = pathlib.Path('WATCHED_LIST/').resolve()
ANIME_DB = pathlib.Path('anime-offline-database.json')
MY_ANIME_LIST = pathlib.Path('animelist_1667042551_-_6743777.xml')
MAIN_DATA = xmltodict.parse(MY_ANIME_LIST.read_text())
ANIME_SEASON = {'SPRING': '03', 'SUMMER': '06', 'FALL': '09', 'WINTER': '12'}
COVERS = {'image/gif': '.gif', 'image/jpeg': '.jpeg', 'image/png': '.png'}

DESCRIPTOR = """{T}

premiered: {P}
type: {Y}
episodes: {E}/{W}
my score: {S}

Some Thoughts?
"""

class Anime:
    # my list
    title = 'str'
    score = int
    type = str
    episodes = int
    watched_episodes = int
    watched_dates = list

    # global db
    cover = str  # or None
    premiered = str  # or None

    dirname = str

    def make_dirname(self):
        if '/' in self.title:
            self.title = self.title.replace('/', ', ')
        self.dirname = f'{self.premiered} - {self.title} - {self.score} - {self.type}'

    def save_to_library(self):
        if not self.premiered: return
        anime_dir = LOCAL_ANIME_LIBRARY_DIR / self.dirname
        anime_dir.mkdir()
        descriptor = anime_dir / 'descriptor.txt'
        text = DESCRIPTOR.format(
            T=self.title,
            P=self.premiered,
            Y=self.type,
            E=self.episodes,
            W=self.watched_episodes,
            S=self.score
        )
        descriptor.write_text(text)

        self._save_cover(anime_dir)

    def _save_cover(self, anime_dir):
        if not self.cover:
            print('no cover for the', self.title)
            return

        if '.jpg' in self.cover or \
                '.jpeg' in self.cover or \
                '.gif' in self.cover or \
                '.png' in self.cover:
            pass
        else:
            print('no cover for the', self.title)
            return

        r = requests.get(self.cover, stream=True)
        mime = r.headers['Content-Type']
        if r.status_code == 200 and mime in COVERS:
            ext = COVERS[mime]
            cover = LOCAL_ANIME_LIBRARY_DIR / self.dirname / f'cover{ext}'
            cover.write_bytes(r.content)
        else:
            print('no cover for the', self.title)

    def save_to_watched_list(self):
        for date in self.watched_dates:
            filename = f'{date} - {self.title}.url'
            sub = WATCHED_LIST_DIR / date[:4]
            if not sub.exists():
                sub.mkdir()
            item = sub / filename
            item.write_text(str(MAIN_LIBRARY_PATH / self.dirname))


def main():
    if not LOCAL_ANIME_LIBRARY_DIR.exists():
        LOCAL_ANIME_LIBRARY_DIR.mkdir()
    if not WATCHED_LIST_DIR.exists():
        WATCHED_LIST_DIR.mkdir()

    list_of_anime = []

    animelist_data = xmltodict.parse(MY_ANIME_LIST.read_text())

    for anime in animelist_data['myanimelist']['anime']:
        try:
            populate_from_my_list(anime, list_of_anime)
        except Exception:
            print('animelist exception from', anime['series_title'])

    global_anime_data = json.loads(ANIME_DB.read_text())
    for anime in list_of_anime:
        try:
            populate_from_global_db(anime, global_anime_data)
        except Exception:
            print('global exception from', anime.title)

    for anime in list_of_anime:
        try:
            anime.make_dirname()
            anime.save_to_library()
            anime.save_to_watched_list()
        except Exception:
            print('save exception from', anime.title)


    print('Done.')
    exit(0)


def populate_from_my_list(entry:dict, list_of_anime:list):
    if entry['my_status'] != 'Completed':
        return

    anime = Anime()
    anime.title = entry['series_title']
    anime.score = entry['my_score']
    anime.type = entry['series_type']
    anime.episodes = entry['series_episodes']
    anime.watched_episodes = entry['my_watched_episodes']

    # watched_dates
    watched_dates = []
    t = entry['my_finish_date']  # like 2022-10-00
    if not t or t[:4] == '0000':
        print('date is missing:', anime.title)
        return
    elif t[5:7] == '00':
        t = t[:4]
    elif t[8:10] == '00':
        t = t[:7]
        y, m = t.split('-')
        t = y + '.' + m
    else:
        y, m, d = t.split('-')
        t = y + '.' + m + '.' + d
    watched_dates.append(t)

    old_dates = entry['my_comments']  # like 2010, 2015, 2020
    if old_dates:
        watched_dates += old_dates.split(', ')

    anime.watched_dates = watched_dates
    list_of_anime.append(anime)


def populate_from_global_db(anime:Anime, global_anime_data:dict):

    def do_stuff(data):
        anime.cover = data.get('picture')
        season = data.get('animeSeason')
        if not season: return
        anime.premiered = str(season['year']) + '.' + ANIME_SEASON[season['season']]

    def loop(second_time=False):
        for data in global_anime_data['data']:
            if not second_time and anime.title == data['title']:
                do_stuff(data)
            elif second_time and data.get('synonyms'):
                for synonym in data['synonyms']:
                    if anime.title == synonym:
                        do_stuff(data)

    loop()
    if not anime.premiered:
        loop(second_time=True)

    if not anime.premiered:
        print('premiered is missing:', anime.title)
        anime.premiered = None
        return


if __name__ == '__main__':
    main()
