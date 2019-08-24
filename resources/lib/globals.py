import sys
import xbmcplugin
import xbmcaddon

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
# Get the add-on path
_addonpath = xbmcaddon.Addon().getAddonInfo('path')
# Addon name
_addonname = 'plugin.video.themoviedb.helper'
# Addon name for logging
_addonlogname = '[plugin.video.themoviedb.helper]\n'
# Property Prefix Name
_prefixname = 'TMDbHelper.'
# Get the api keys
_omdb_apikey = '?apikey={0}'.format(xbmcplugin.getSetting(_handle, 'omdb_apikey')) if xbmcplugin.getSetting(_handle, 'omdb_apikey') else None
_tmdb_apikey = xbmcplugin.getSetting(_handle, 'tmdb_apikey')
# Cache days
_cache_details_days = xbmcplugin.getSetting(_handle, 'cache_details_days')
_cache_details_days = int(_cache_details_days)
_cache_list_days = xbmcplugin.getSetting(_handle, 'cache_list_days')
_cache_list_days = int(_cache_list_days)

if not _cache_details_days or _cache_details_days < 14:
    _cache_details_days = 14
if not _cache_list_days or _cache_list_days < 1:
    _cache_list_days = 1

if _tmdb_apikey:
    _waittime = 0.2
    _tmdb_apikey = '?api_key={0}'.format(_tmdb_apikey)
else:
    _waittime = 2
    _tmdb_apikey = '?api_key=a07324c669cac4d96789197134ce272b'

# Get the MPAA prefix and add a space if we have a setting
_mpaaprefix = xbmcplugin.getSetting(_handle, 'mpaa_prefix')
_mpaaprefix = '{0} '.format(_mpaaprefix) if _mpaaprefix else ''
# Set http paths
OMDB_API = 'http://www.omdbapi.com/'
OMDB_ARG = '&tomatoes=True&plot=Full'
TMDB_API = 'https://api.themoviedb.org/3'
IMAGEPATH = 'https://image.tmdb.org/t/p/original/'

# Languages and Country
_language = '&language=en-US&include_image_language=en,null'
_country = 'US'
LANGUAGES = ['ar-AE', 'ar-SA', 'be-BY', 'bg-BG', 'bn-BD', 'ca-ES', 'ch-GU', 'cs-CZ',
             'da-DK', 'de-AT', 'de-CH', 'de-DE', 'el-GR', 'en-AU', 'en-CA', 'en-GB',
             'en-IE', 'en-NZ', 'en-US', 'eo-EO', 'es-ES', 'es-MX', 'et-EE', 'eu-ES',
             'fa-IR', 'fi-FI', 'fr-CA', 'fr-FR', 'gl-ES', 'he-IL', 'hi-IN', 'hu-HU',
             'id-ID', 'it-IT', 'ja-JP', 'ka-GE', 'kk-KZ', 'kn-IN', 'ko-KR', 'lt-LT',
             'lv-LV', 'ml-IN', 'ms-MY', 'ms-SG', 'nb-NO', 'nl-NL', 'no-NO', 'pl-PL',
             'pt-BR', 'pt-PT', 'ro-RO', 'ru-RU', 'si-LK', 'sk-SK', 'sl-SI', 'sr-RS',
             'sv-SE', 'ta-IN', 'te-IN', 'th-TH', 'tl-PH', 'tr-TR', 'uk-UA', 'vi-VN',
             'zh-CN', 'zh-HK', 'zh-TW', 'zu-ZA']
_languagesetting = xbmcplugin.getSetting(_handle, 'language')
if _languagesetting:
    _country = LANGUAGES[int(_languagesetting)][-2:]
    _language = '&language={0}&include_image_language={1},null'.format(LANGUAGES[int(_languagesetting)], LANGUAGES[int(_languagesetting)][:2])


# Categories pass tmdb_id to path using .format(*args)
CATEGORIES = {'cast':
              {'types': ['movie', 'tv'],
               'name': 'Cast',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}/credits',
               'key': 'cast',
               'list_type': 'person',
               'next_type': 'person',
               'next_info': 'details',
               'index': 1
               },
              'recommendations':
              {'types': ['movie', 'tv'],
               'name': 'Recommended',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}/recommendations',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 2
               },
              'similar':
              {'types': ['movie', 'tv'],
               'name': 'Similar',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}/similar',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 3
               },
              'crew':
              {'types': ['movie', 'tv'],
               'name': 'Crew',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}/credits',
               'key': 'crew',
               'list_type': 'person',
               'next_type': 'person',
               'next_info': 'details',
               'index': 4
               },
              'movie_keywords':
              {'types': ['movie'],
               'name': 'Keywords',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}/keywords',
               'key': 'keywords',
               'list_type': '{self.request_tmdb_type}',
               'next_type': 'keyword',
               'next_info': 'keyword_movies',
               'index': 5
               },
              'reviews':
              {'types': ['movie', 'tv'],
               'name': 'Reviews',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}/reviews',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '',
               'next_info': 'textviewer',
               'index': 6
               },
              'posters':
              {'types': ['movie', 'tv'],
               'name': 'Posters',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}/images',
               'key': 'posters',
               'list_type': 'image',
               'next_type': 'image',
               'next_info': 'imageviewer',
               'index': 7,
               },
              'fanart':
              {'types': ['movie', 'tv'],
               'name': 'Fanart',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}/images',
               'key': 'backdrops',
               'list_type': 'image',
               'next_type': 'image',
               'next_info': 'imageviewer',
               'index': 8,
               },
              'seasons':
              {'types': ['tv'],
               'name': 'Seasons',
               'path': '{self.request_tmdb_type}/{self.request_tmdb_id}',
               'key': 'seasons',
               'list_type': 'season',
               'next_type': 'tv',
               'next_info': 'episodes',
               'index': 9,
               },
              'episode_cast':
              {'types': ['episode'],
               'name': 'Cast',
               'path': 'tv/{self.request_tmdb_id}/season/{self.request_season}/episode/{self.request_episode}/credits',
               'key': 'cast',
               'list_type': 'person',
               'next_type': 'person',
               'next_info': 'details',
               'index': 1,
               },
              'episode_thumbs':
              {'types': ['episode'],
               'name': 'Thumbs',
               'path': 'tv/{self.request_tmdb_id}/season/{self.request_season}/episode/{self.request_episode}/images',
               'key': 'stills',
               'list_type': 'image',
               'next_type': 'image',
               'next_info': 'imageviewer',
               'index': 2,
               },
              'stars_in_movies':
              {'types': ['person'],
               'name': 'Cast in Movies',
               'path': 'person/{self.request_tmdb_id}/movie_credits',
               'key': 'cast',
               'list_type': 'movie',
               'next_type': 'movie',
               'next_info': 'details',
               'index': 1,
               },
              'stars_in_tvshows':
              {'types': ['person'],
               'name': 'Cast in Tv Shows',
               'path': 'person/{self.request_tmdb_id}/tv_credits',
               'key': 'cast',
               'list_type': 'tv',
               'next_type': 'tv',
               'next_info': 'details',
               'index': 2,
               },
              'crew_in_movies':
              {'types': ['person'],
               'name': 'Crew in Movies',
               'path': 'person/{self.request_tmdb_id}/movie_credits',
               'key': 'crew',
               'list_type': 'movie',
               'next_type': 'movie',
               'next_info': 'details',
               'index': 3,
               },
              'crew_in_tvshows':
              {'types': ['person'],
               'name': 'Crew in Tv Shows',
               'path': 'person/{self.request_tmdb_id}/tv_credits',
               'key': 'crew',
               'list_type': 'tv',
               'next_type': 'tv',
               'next_info': 'details',
               'index': 4,
               },
              'images':
              {'types': ['person'],
               'name': 'Images',
               'path': 'person/{self.request_tmdb_id}/images',
               'key': 'profiles',
               'list_type': 'image',
               'next_type': 'image',
               'next_info': 'imageviewer',
               'index': 5,
               },
              'search':
              {'types': ['movie', 'tv', 'person'],
               'name': 'Search {self.plural_type}',
               'path': 'search/{self.request_tmdb_type}',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 1,
               },
              'find':
              {'types': ['movie', 'tv'],
               'name': 'Find IMDb ID ({self.plural_type})',
               'path': 'find/{self.imdb_id}',
               'key': '{self.request_tmdb_type}_results',
               'index': 2,
               },
              'popular':
              {'types': ['movie', 'tv', 'person'],
               'name': 'Popular {self.plural_type}',
               'path': '{self.request_tmdb_type}/popular',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 3,
               },
              'top_rated':
              {'types': ['movie', 'tv'],
               'name': 'Top Rated {self.plural_type}',
               'path': '{self.request_tmdb_type}/top_rated',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 4,
               },
              'upcoming':
              {'types': ['movie'],
               'name': 'Upcoming {self.plural_type}',
               'path': '{self.request_tmdb_type}/upcoming',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 5,
               },
              'airing_today':
              {'types': ['tv'],
               'name': 'Airing Today',
               'path': '{self.request_tmdb_type}/airing_today',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 6,
               },
              'now_playing':
              {'types': ['movie'],
               'name': 'In Theatres',
               'path': '{self.request_tmdb_type}/now_playing',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 7,
               },
              'on_the_air':
              {'types': ['tv'],
               'name': 'Currently Airing',
               'path': '{self.request_tmdb_type}/on_the_air',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 8,
               },
              'discover':
              {'types': ['movie', 'tv'],
               'name': 'Discover',
               'path': 'discover/{self.request_tmdb_type}',
               'key': 'results',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 99,
               },
              'collection':
              {'types': ['movie'],
               'name': 'In Collection',
               'path': 'collection/{self.request_tmdb_id}',
               'key': 'parts',
               'list_type': '{self.request_tmdb_type}',
               'next_type': '{self.request_tmdb_type}',
               'next_info': 'details',
               'index': 99,
               },
              'keyword_movies':
              {'types': ['keyword'],
               'name': 'Keywords',
               'path': 'keyword/{self.request_tmdb_id}/movies',
               'key': 'results',
               'list_type': 'movie',
               'next_type': 'movie',
               'next_info': 'details',
               'index': 99,
               },
              'episodes':
              {'types': ['tv'],
               'name': 'Episodes',
               'path': 'tv/{self.request_tmdb_id}/season/{self.request_season}',
               'key': 'episodes',
               'list_type': 'episode',
               'next_type': 'episode',
               'next_info': 'details',
               'index': 99,
               },
              }

MAINFOLDER = ['search', 'find', 'popular', 'top_rated', 'upcoming', 'airing_today',
              'now_playing', 'on_the_air']

EXCLUSIONS = ['discover', 'collection', 'episodes']

GENRE_IDS = {"Action": 28,
             "Adventure": 12,
             "Animation": 16,
             "Comedy": 35,
             "Crime": 80,
             "Documentary": 99,
             "Drama": 18,
             "Family": 10751,
             "Fantasy": 14,
             "History": 36,
             "Horror": 27,
             "Kids": 10762,
             "Music": 10402,
             "Mystery": 9648,
             "News": 10763,
             "Reality": 10764,
             "Romance": 10749,
             "Science Fiction": 878,
             "Sci-Fi & Fantasy": 10765,
             "Soap": 10766,
             "Talk": 10767,
             "TV Movie": 10770,
             "Thriller": 53,
             "War": 10752,
             "War & Politics": 10768,
             "Western": 37}

APPEND_TO_RESPONSE = 'credits,images,release_dates,content_ratings,external_ids'
