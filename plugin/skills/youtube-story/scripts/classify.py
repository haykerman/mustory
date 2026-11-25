"""Topic and artist guesses from titles and channel names.

Generic rules only. Person-specific accuracy comes from channel -> topic overrides the agent writes after
reading the channel list (youtube-story: labels.json "channels" from to_label.tsv;
youtube-vs-spotify: labels.json "youtube_channels" from youtube_channels.tsv).
"""
import re
import unicodedata

MUSIC_CH = re.compile(r'vevo$|- topic$|records|music|official|sessions?$|radio|kcrw|colors|billboard|tiny desk|eurovision|'
                      r'audiotree|mahogany|lofi|synthwave|wave$|^creators$|band$', re.I)
MUSIC_T = re.compile(r'ambient|ambience|\bchill|lofi|lo-fi|\bhour of\b|\bvibes\b|chopin|sinfon|symphon|gregorian|\bjazz\b|\bblues\b|'
                     r'official (music )?video|official audio|\baudio\)|lyric|\blive\b|acoustic|\bcover\b|remix|\bft\.|\bfeat\.?\b|'
                     r'full album|\bmix\b|session|unplugged|music video|\balbum\b|tiny desk|instrumental|\bost\b|soundtrack|'
                     r'karaoke|\bsong\b|клип|official mv|\bmv\b|backing track|\bm/v\b', re.I)
DASHES = '\\-\u2010\u2011\u2012\u2013\u2014\u2015\u058a'  # incl. the Armenian hyphen ֊
ARTIST_SONG = re.compile(rf'^\s*([^{DASHES}|]{{2,45}}?)\s+[{DASHES}]\s+([^{DASHES}]{{2,90}})$')
KW = [
    ('Gaming', r'\b(league of legends|dota|gameplay|minecraft|gta|elden ring|fortnite|valorant|cs2|counter.?strike|playthrough|'
               r'speedrun|nintendo|playstation|xbox|steam deck|walkthrough|let\'?s play)\b'),
    ('Programming', r'\b(react|javascript|typescript|python|rust|golang|coding|programm\w*|developer|css|next\.?js|docker|kubernetes|'
                    r'neovim|vim|swiftui|api|backend|frontend|leetcode|algorithm|claude|chatgpt|openai|llm|sql|node\.?js|git)\b'),
    ('Tech', r'\b(iphone|ipad|android|samsung|galaxy|pixel|macbook|laptop|unboxing|review|apple|airpods|gadget|smartphone|'
             r'tesla|gpu|nvidia|keyboard|tech|linux|ubuntu|windows 1[01])\b'),
    ('News & politics', r'\b(trump|putin|ukraine|russia|biden|election|israel|gaza|iran|nato|zelensky|kremlin|politic\w*|war|'
                        r'news|parliament|minister|president)\b'),
    ('Comedy & entertainment', r'\b(prank|funny|try not to laugh|comedy|stand.?up|sketch|reaction|podcast|interview)\b|#shorts'),
    ('Science & learning', r'\b(history of|explained|science|physics|space|universe|documentary|how .* works|lecture)\b'),
    ('Playing music', r'\b(guitar lesson|bass lesson|chords|how to play|lyre|tin whistle|piano tutorial|fingerstyle|pedal|'
                      r'vocal (exercise|lesson)|singing lesson)\b'),
    ('Sports', r'\b(highlights|goal|nba|nfl|ufc|premier league|champions league|f1|formula 1|olympic)\b'),
    ('Food', r'\b(recipe|cooking|how to cook|street food|mukbang)\b'),
    ('Fitness & health', r'\b(workout|exercise|stretch|back pain|posture|yoga|diet|calories)\b'),
]
KW = [(c, re.compile(p, re.I)) for c, p in KW]
SCRIPTS = [('Armenian', r'[԰-֏]'), ('Russian/Cyrillic', r'[Ѐ-ӿ]'), ('Arabic', r'[؀-ۿ]'),
           ('Hebrew', r'[֐-׿]'), ('Hindi', r'[ऀ-ॿ]'), ('Korean', r'[가-힯]'),
           ('Japanese', r'[぀-ヿ]'), ('Chinese', r'[一-鿿]'), ('Greek', r'[Ͱ-Ͽ]'),
           ('Georgian', r'[Ⴀ-ჿ]'), ('Thai', r'[฀-๿]')]
SCRIPTS = [(n, re.compile(p)) for n, p in SCRIPTS]


def category(title, ch, labels):
    """labels: {channel name (case-insensitive): topic} from labels.json."""
    c = labels.get((ch or '').strip().lower())
    if c:
        return c
    if ch and MUSIC_CH.search(ch):
        return 'Music'
    if MUSIC_T.search(title):
        return 'Music'
    for cat, rx in KW:
        if rx.search(title):
            return cat
    if ARTIST_SONG.match(title) and len(title) < 90:
        return 'Music'
    for name, rx in SCRIPTS:
        if rx.search(title):
            return f'{name}-language other'
    return 'Other'


def norm(s):
    s = unicodedata.normalize('NFKC', s).lower()
    s = re.sub(r'vevo$|\s*-\s*topic$|official|music$|\(.*?\)|\[.*?\]', '', s)
    return re.sub(r'[^\w]', '', s)


COMPILATION = re.compile(r'eurovision|bbc|radio|kcrw|colors|billboard|npr|creators|mahogany|audiotree|siriusxm|2 meter|'
                         r'postmodern|sideshow|vevo dscvr|genius|cercle|boiler room|a colors show|mix', re.I)


def artist(title, ch):
    m = ARTIST_SONG.match(title)
    if m:
        a = re.sub(r'^\s*[\[【(][^\]】)]*[\]】)]\s*', '', m.group(1))  # drop "【Stage Mix】 " style prefixes
        # Keep duos whole ("Abor & Tynna"); cut featured guests, comma lists and bracketed translations.
        a = re.split(r'\s*(?:,| x | feat\.?| ft\.?| featuring | with )\s*', a, maxsplit=1, flags=re.I)[0]
        a = re.sub(r'\s*[(（][^)）]*[)）]\s*$', '', a).strip(' "\'«')
        if 1 < len(a) <= 40:
            return a
    if ch and not COMPILATION.search(ch):
        return re.sub(r'VEVO$|\s*-\s*Topic$', '', ch).strip()
    return None
