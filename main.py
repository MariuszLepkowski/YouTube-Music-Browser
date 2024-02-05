from ytmusicapi import YTMusic
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

YT_VIDEO_ENDPOINT = 'https://www.youtube.com/watch?v='
YT_PLAYLIST_ENDPOINT = 'https://www.youtube.com/playlist?list='
YT_API_KEY = os.environ['YT_API_KEY']

youtube = build("youtube", "v3", developerKey=YT_API_KEY)
yt = YTMusic('oauth.json')


def search_playlist_on_yt(search_query):
    """Searches for playlists on regular YT"""
    print('search_playlist_on_yt')

    playlist_found = False

    request = youtube.search().list(part='snippet', q=search_query)
    response = request.execute()

    for item in response['items']:
        if item['id']['kind'] == 'youtube#playlist':
            playlist_id = item['id']['playlistId']

            playlist_request = youtube.playlists().list(part="snippet", id=playlist_id)
            playlist_response = playlist_request.execute()

            if 'items' in playlist_response:
                playlist_title = playlist_response['items'][0]['snippet']['title']
                print(f"Playlist Title: {playlist_title} Playlist url: {YT_PLAYLIST_ENDPOINT}{playlist_id}")

                playlist_items_request = youtube.playlistItems().list(
                    part="contentDetails,snippet",
                    playlistId=playlist_id,
                    maxResults=50
                )
                playlist_items_response = playlist_items_request.execute()

                for item in playlist_items_response['items']:
                    video_id = item['contentDetails']['videoId']
                    video_title = item['snippet']['title']
                    print(f"{video_title} - Video URL: {YT_VIDEO_ENDPOINT}{video_id}")

    return playlist_found


def search_album_on_ytmusic(search_query):
    """Searches for each individual track on the requested album on YT Music"""
    print('search_album_on_ytmusic')

    album_found = False

    search_results = yt.search(query=search_query, filter='albums')

    for result in search_results:
        album_artist = result['artists'][1]['name']
        album_title = result['title']

        if all(word.lower() in album_artist.lower() for word in artist_query.lower().split()) or all(word in album_title.lower().split() for word in title_query.lower().split()):

            album_found = True
            print(album_artist, album_title)

            album_browseId = result['browseId']
            album_info = yt.get_album(browseId=album_browseId)

            album_tracklist = album_info['tracks']

            for track in album_tracklist:
                print(f"{track['trackNumber']}, {track['title']}, {YT_VIDEO_ENDPOINT}{track['videoId']}")

    return album_found


def search_playlist_on_ytmusic(search_query):
    """Searches for playlists on YT Music"""
    print('search_playlist_on_ytmusic')

    playlist_found = False

    search_results = yt.search(search_query, filter='playlists')

    for result in search_results:
        playlist_title_wordlist = result['title'].lower().split()

        if all(word in playlist_title_wordlist for word in artist_query.lower().split()) or all(word in playlist_title_wordlist for word in title_query.lower().split()):
            playlist_found = True

            playlist_info = yt.get_playlist(playlistId=result['browseId'])
            print(f"Playlist title: {result['title']} Playlist url: {YT_PLAYLIST_ENDPOINT}{playlist_info['id']}")
            playlist_tracklist = playlist_info['tracks']

            track_num = 0
            for track in playlist_tracklist:
                track_num += 1
                print(f"{track_num}: {track['title']}, {YT_VIDEO_ENDPOINT}{track['videoId']}")

    return playlist_found


def search_video_on_yt(search_query):

    """Searches for a video on regular YT"""
    print('search_video_on_yt')

    video_found = False

    request = youtube.search().list(part='snippet', q=search_query, type='video')
    response = request.execute()

    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        print(f"{video_title} - Video URL: {YT_VIDEO_ENDPOINT}{video_id}")

        video_found = True

    return video_found


try:
    artist_query = input('Type artist name: ')
    title_query = input('Type album/song title: ')
    
    search_query = artist_query + ' ' + title_query

    album_found = search_album_on_ytmusic(search_query)
    playlist_found = search_playlist_on_ytmusic(search_query)
    video_found = search_video_on_yt(search_query)

    if not (album_found or playlist_found) and not video_found:
        print("No results found.")

except IndexError:
    print("An error occurred.")







