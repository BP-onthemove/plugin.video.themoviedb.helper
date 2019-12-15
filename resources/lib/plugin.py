import xbmc
import xbmcgui
import xbmcaddon
import resources.lib.utils as utils
from resources.lib.globals import LANGUAGES, APPEND_TO_RESPONSE, TMDB_LISTS
from resources.lib.kodilibrary import KodiLibrary
from resources.lib.tmdb import TMDb
from resources.lib.omdb import OMDb
from resources.lib.fanarttv import FanartTV


class Plugin(object):
    def __init__(self):
        self.addon = xbmcaddon.Addon('plugin.video.themoviedb.helper')
        self.addonpath = self.addon.getAddonInfo('path')
        self.prefixname = 'TMDbHelper.'
        self.kodimoviedb = None
        self.koditvshowdb = None
        self.details_tv = None

        cache_long = self.addon.getSettingInt('cache_details_days')
        cache_short = self.addon.getSettingInt('cache_list_days')
        tmdb_apikey = self.addon.getSetting('tmdb_apikey')
        omdb_apikey = self.addon.getSetting('omdb_apikey')
        fanarttv_apikey = self.addon.getSetting('fanarttv_apikey')
        fanarttv_clientkey = self.addon.getSetting('fanarttv_clientkey')
        language = LANGUAGES[self.addon.getSettingInt('language')]
        mpaa_prefix = self.addon.getSetting('mpaa_prefix')

        self.tmdb = TMDb(
            api_key=tmdb_apikey, language=language, cache_long=cache_long, cache_short=cache_short,
            append_to_response=APPEND_TO_RESPONSE, mpaa_prefix=mpaa_prefix)

        self.omdb = OMDb(api_key=omdb_apikey, cache_long=cache_long, cache_short=cache_short) if omdb_apikey else None

        self.fanarttv = (
            FanartTV(
                api_key=fanarttv_apikey, client_key=fanarttv_clientkey, language=language,
                cache_long=cache_long, cache_short=cache_short)
            if self.addon.getSettingBool('fanarttv_lookup') else None)

    def textviewer(self, header, text):
        xbmcgui.Dialog().textviewer(header, text)

    def imageviewer(self, image):
        xbmc.executebuiltin('ShowPicture({0})'.format(image))

    def get_tmdb_id(self, query=None, itemtype=None, imdb_id=None, year=None, **kwargs):
        if kwargs.get('tmdb_id'):
            return kwargs.get('tmdb_id')
        query = utils.split_items(query)[0] if query else None
        itemtype = itemtype or TMDB_LISTS.get(kwargs.get('info'), {}).get('tmdb_check_id') or kwargs.get('type')
        return self.tmdb.get_tmdb_id(itemtype=itemtype, imdb_id=imdb_id, query=query, year=year, longcache=True)

    def get_omdb_ratings(self, item, cache_only=False):
        if self.omdb and item.get('infolabels', {}).get('imdbnumber'):
            ratings_awards = self.omdb.get_ratings_awards(imdb_id=item.get('infolabels', {}).get('imdbnumber'), cache_only=cache_only)
            if ratings_awards:
                item['infoproperties'] = utils.merge_two_dicts(item.get('infoproperties', {}), ratings_awards)
        return item

    def get_db_info(self, item, info=None, tmdbtype=None, dbid=None, imdb_id=None, originaltitle=None, title=None, year=None):
        kodidatabase = None
        if tmdbtype == 'movie':
            self.kodimoviedb = self.kodimoviedb or KodiLibrary(dbtype='movie')
            kodidatabase = self.kodimoviedb
        if tmdbtype == 'tv':
            self.koditvshowdb = self.koditvshowdb or KodiLibrary(dbtype='tvshow')
            kodidatabase = self.koditvshowdb
        if kodidatabase and info:
            return kodidatabase.get_info(info=info, dbid=dbid, imdb_id=imdb_id, originaltitle=originaltitle, title=title, year=year)
