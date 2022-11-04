#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup
import os
import json
from urlparse import urlparse
import urllib
import urllib2


proxiesSSR = {
    "http": "http://127.0.0.1:1087",
    "https": "http://127.0.0.1:1087",
}



class YoutubeAPI:
    youtube_key = ""

    apis = {
        'videos.list': 'https://www.googleapis.com/youtube/v3/videos',
        'search.list': 'https://www.googleapis.com/youtube/v3/search',
        'channels.list': 'https://www.googleapis.com/youtube/v3/channels',
        'playlists.list': 'https://www.googleapis.com/youtube/v3/playlists',
        'playlistItems.list': 'https://www.googleapis.com/youtube/v3/playlistItems',
        'activities': 'https://www.googleapis.com/youtube/v3/activities',
    }

    page_info = {}

    def __init__(self, params):

        if not params:
            raise ValueError('The configuration options must be an array..')

        if 'key' not in params:
            raise ValueError('Google API key is required, please visit http://code.google.com/apis/console')

        self.youtube_key = params['key']

    def get_video_info(self, video_id):

        api_url = self.get_api('videos.list')
        params = {
            'id': video_id,
            'key': self.youtube_key,
            'part': 'id, snippet, contentDetails, player, statistics, status'
        }
        apiData = self.api_get(api_url, params)

        return self.decode_single(apiData)

    def get_videos_info(self, video_ids):

        ids = video_ids
        if not isinstance(video_ids, basestring):
            ids = video_ids.join(',')

        api_url = self.get_api('videos.list')
        params = {
            'id': ids,
            'part': 'id, snippet, contentDetails, player, statistics, status'
        }
        api_data = self.api_get(api_url, params)

        return self.decode_list(api_data);

    def search(self, q, max_results=10):

        params = {
            'q': q,
            'part': 'id, snippet',
            'maxResults': max_results
        }

        return self.search_advanced(params)

    def search_videos(self, q, max_results=10, order=None):

        params = {
            'q': q,
            'type': 'video',
            'part': 'id, snippet',
            'maxResults': max_results
        }
        if order is not None:
            params['order'] = order

        return self.search_advanced(params)

    def search_channel_videos(self, q, channel_id, max_results=10, order=None):

        params = {
            'q': q,
            'type': 'video',
            'channelId': channel_id,
            'part': 'id, snippet',
            'maxResults': max_results
        }
        if order is not None:
            params['order'] = order

        return self.search_advanced(params)

    def search_advanced(self, params, page_info=False):

        api_url = self.get_api('search.list')
        if params is None or 'q' not in params:
            raise ValueError('at least the Search query must be supplied')

        api_data = self.api_get(api_url, params)
        if page_info:
            return {
                'results': self.decode_list(api_data),
                'info': self.page_info
            }
        else:
            return self.decode_list(api_data)

    def paginate_results(self, params, token=None):

        if token is not None:
            params['pageToken'] = token
        if params:
            return self.search_advanced(params, True)

    def get_channel_by_name(self, username, optional_params=False):

        api_url = self.get_api('channels.list')
        params = {
            'forUsername': username,
            'part': 'id,snippet,contentDetails,statistics,invideoPromotion'
        }
        if optional_params:
            params += optional_params

        api_data = self.api_get(api_url, params)
        return self.decode_single(api_data)

    def get_channel_by_id(self, id, optional_params=False):

        api_url = self.get_api('channels.list')
        params = {
            'id': id,
            'part': 'id,snippet,contentDetails,statistics,invideoPromotion'
        }
        if optional_params:
            params += optional_params

        api_data = self.api_get(api_url, params)
        return self.decode_single(api_data)

    def get_playlists_by_channel_id(self, channel_id, optional_params={}):

        api_url = self.get_api('playlists.list')
        params = {
            'channelId': channel_id,
            'part': 'id, snippet, status'
        }
        if optional_params:
            params += optional_params

        api_data = self.api_get(api_url, params)
        return self.decode_list(api_data)

    def get_playlist_by_id(self, id):

        api_url = self.get_api('playlists.list')
        params = {
            'id': id,
            'part': 'id, snippet, status'
        }
        api_data = self.api_get(api_url, params)
        return self.decode_single(api_data)

    def get_playlist_items_by_playlist_id(self, playlist_id, max_results=50):

        api_url = self.get_api('playlistItems.list')
        params = {
            'playlistId': playlist_id,
            'part': 'id, snippet, contentDetails, status',
            'maxResults': max_results
        }
        api_data = self.api_get(api_url, params)
        return self.decode_list(api_data)

    def get_activities_by_channel_id(self, channel_id):

        if channel_id is None:
            raise ValueError('ChannelId must be supplied')

        api_url = self.get_api('activities')
        params = {
            'channelId': channel_id,
            'part': 'id, snippet, contentDetails'
        }
        api_data = self.api_get(api_url, params)
        return self.decode_list(api_data)

    def parse_vid_from_url(self, youtube_url):

        if 'youtube.com' in youtube_url:
            params = self._parse_url_query(youtube_url)
            return params['v']
        elif 'youtu.be' in youtube_url:
            path = self._parse_url_path(youtube_url)
            vid = path[1:]
            return vid
        else:
            raise Exception('The supplied URL does not look like a Youtube URL')

    def get_channel_from_url(self, youtube_url):

        if 'youtube.com' not in youtube_url:
            raise Exception('The supplied URL does not look like a Youtube URL')
        path = self._parse_url_path(youtube_url)
        if '/channel' in path:
            segments = path.split('/')
            channel_id = segments[len(segments) - 1]
            channel = self.get_channel_by_id(channel_id)
        elif '/user' in path:
            segments = path.split('/')
            username = segments[len(segments) - 1]
            channel = self.get_channel_by_name(username)
        else:
            raise Exception('The supplied URL does not look like a Youtube Channel URL')

        return channel

    def get_api(self, name):
        return self.apis[name]

    def decode_single(self, api_data):

        res_obj = json.loads(api_data)
        if 'error' in res_obj:
            msg = "Error " + res_obj['error']['code'] + " " + res_obj['error']['message']
            if res_obj['error']['errors'][0]:
                msg = msg + " : " + res_obj['error']['errors'][0]['reason']
            raise Exception(msg)
        else:
            items_array = res_obj['items']
            if isinstance(items_array, dict) or len(items_array) == 0:
                return False
            else:
                return items_array[0]

    def decode_list(self, api_data):

        res_obj = json.loads(api_data)
        if 'error' in res_obj:
            msg = "Error " + res_obj['error']['code'] + " " + res_obj['error']['message']
            if res_obj['error']['errors'][0]:
                msg = msg + " : " + res_obj['error']['errors'][0]['reason']
            raise Exception(msg)
        else:
            self.page_info = {
                'resultsPerPage': res_obj['pageInfo']['resultsPerPage'],
                'totalResults': res_obj['pageInfo']['totalResults'],
                'kind': res_obj['kind'],
                'etag': res_obj['etag'],
                'prevPageToken': None,
                'nextPageToken': None
            }
            if 'prevPageToken' in res_obj:
                self.page_info['prevPageToken'] = res_obj['prevPageToken']
            if 'nextPageToken' in res_obj:
                self.page_info['nextPageToken'] = res_obj['nextPageToken']

            items_array = res_obj['items']
            if isinstance(items_array, dict) or len(items_array) == 0:
                return False
            else:
                return items_array

    def api_get(self, url, params):

        params['key'] = self.youtube_key

        f = urllib2.urlopen(url + "?" + urllib.urlencode(params))
        data = f.read()
        f.close()

        return data

    def _parse_url_path(self, url):

        array = urlparse(url)
        return array['path']

    def _parse_url_query(self, url):

        array = urlparse(url)
        query = array['query']
        query_parts = query.split('&')
        params = {}
        for param in query_parts:
            item = param.split('=')
            if not item[1]:
                params[item[0]] = ''
            else:
                params[item[0]] = item[1]

        return params



def convert(source, crossrefQuery=''):
    
    params = {
        'q': 'Android',
        'type': 'video',
        'part': 'id, snippet',
        'maxResults': 50,
        'key': 'AIzaSyCcQ-bwoHrDnUSiwr0K6dMqFKDKkztYj_Q'
    }
    youtube = YoutubeAPI(params)
    
    
    channel = youtube.get_channel_by_name('MIT')

    print channel

    playlists = youtube.get_playlists_by_channel_id(channel['id'])

    print playlists


    print 'sds'

def main(argv):
    source = ''
    crossrefQuery = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:p:', ["url", "crossrefQuery", "proxy"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a
        if o in ('-p', '--proxy'):
            proxy = urllib2.ProxyHandler({
                'http': a,
                'https': a
            })
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)


    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery)

if __name__ == '__main__':
    main(sys.argv)
