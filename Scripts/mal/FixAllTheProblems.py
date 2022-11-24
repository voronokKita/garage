''' old descriptor:

some
text

premiered: 2009.06
type: TV
episodes: 26/26
my score: 6

Some thoughts?
'''

import re
from pathlib import Path

ANIME_SEASONS_SHORT = {'12': '1', '03': '2', '06': '3', '09': '4'}
ANIME_SEASONS_LONG = {'12': 'winter', '03': 'spring', '06': 'summer', '09': 'fall'}


dir_pattern = re.compile(r'\d\d\d\d\.\d\d')
suffix_pattern = re.compile(r'(.*)(TV|OVA|ONA|Movie|Special)$')

animename_pattern = re.compile(r'''  # 2021.03 - Mini Dragon - 9 - ONA
(\d\d\d\d\.\d\d\s-\s)
(.+)
(\s-\s\d+\s-\s)
(TV|OVA|ONA|Movie|Special)
''', re.I | re.VERBOSE)

main_dir = Path('main').resolve(strict=True)
all_files = main_dir.glob('*')

for item in all_files:
    try:
        if item.is_dir() and dir_pattern.fullmatch(item.name[:7]):
            dirname = item.name.strip()
            new_prefix = dirname[:5] + ANIME_SEASONS_SHORT.get(dirname[5:7])
            old_suffix = suffix_pattern.findall(dirname)[0][1]
            animename = animename_pattern.findall(dirname)[0][1]
            new_name = f'main/{new_prefix} - {animename} ({old_suffix})'
            item.rename(new_name)
    except Exception:
        print('rename error:', item.name)


print('done with renaming')

ol_descriptor_pattern = re.compile(r'''
(.+)  # title: 1 or 2 lines
(\npremiered:\s\d\d\d\d\.\d\d\n)
(type:\s\w+\n)
(episodes:\s\d+/\d+\n)
(my\sscore:\s\d+\n)
(\n.+)  # some other text
''', re.I | re.VERBOSE | re.DOTALL)

NEW_DESCRIPTOR_TEMPLATE = '''{TITLE}

studio:
premiered: {SEASON}, {YEAR}
type: {TYPE}
episodes: {EPISODES}
my score: {SCORE}

watched date(s):
- (date, short description)

OST: (bool, impression)
OP&ED list:
- (num, impression)

Some thoughts:
{THOUGHTS}

Characters:
'''

def process_descriptor(text):
    title = ''
    season = ''
    year = ''
    type_ = ''
    episodes = ''
    score = ''
    thoughts = ''

    result = ol_descriptor_pattern.findall(text)[0]
    if result:
        title = result[0].strip()

        premiered = result[1].strip()
        premiered = premiered.lstrip('premiered: ')
        year = premiered[:4]
        season = ANIME_SEASONS_LONG.get(premiered[5:])

        type_ = result[2].strip()
        type_ = type_.lstrip('type: ')

        episodes = result[3].strip()
        episodes = episodes.lstrip('episodes: ')

        score = result[4].strip()
        score = score.lstrip('my score: ')

        thoughts = result[5].strip()

        return NEW_DESCRIPTOR_TEMPLATE.format(
            TITLE=title,
            SEASON=season,
            YEAR=year,
            TYPE=type_,
            EPISODES=episodes,
            SCORE=score,
            THOUGHTS=thoughts,
        )
    else:
        return False

all_files = main_dir.rglob('*')
for item in all_files:
    if item.is_file() and item.name == 'descriptor.txt':
        old_text = item.read_text()
        new_text = process_descriptor(old_text)
        if new_text:
            item.write_text(new_text)
        else:
            print('descriptor error:', item.parent)

print('done')
