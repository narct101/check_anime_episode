#!/usr/bin/env python
import sys
import requests
import json

url_animedub = "http://sonarr.sshlab.io/api/v3"
url_animesub = "http://sonarr-anime.sshlab.io/api/v3"
api_token = "CHANGE_ME_TO_API_TOKEN"   ## tied to url_animedub
api_token2 = "CHANGE_ME_TO_API_TOKEN"  ## tied to url_animesub

headers = {'Accept' : 'application/json', 'content-type': 'application/json'}
debug = ""

##
## search through all episodes since "id" does not correlate between sonarr instances
##
def search_episodes(ep_id, tvdbid, series_title, all_data):
    series_id = []
    ## quickly run through all series to find the series the episode is tied to
    for series in all_data:
        if series['title'] == series_title:
            series_id = series['id']
    ## if we don't find series match, quit out of definition
    if series_id == []:
        return
    ## get all episodes from a single series
    response = requests.get(url_animedub + '/episode' + '?apikey=' + api_token + '&seriesID=' + str(series_id), headers=headers)
    all_episodes = response.json()
    ## loop through each episode of this anime series
    for episode in all_episodes:
        ## check if file exists on sonarr side
        if episode['hasFile'] and episode['tvdbId'] == tvdbid:
            return ep_id

## delete episode
## we need episode['episodeFileId'] to delete file
def delete_episode(ep_fileid):
    response = requests.delete(url_animesub + '/episodefile/' + str(ep_fileid) + '?apikey=' + api_token2 , headers=headers)
    #print(response.status_code + "\n" + response.json())

## unmonitor episode
## we need episode['id'] to unmonitor file
def unmonitor_episode(ep_id):
    body = {
        "episodeIDs": [
            ep_id
        ],
        "monitored": False
    }
    response = requests.put(url_animesub + '/episode/monitor' + '?apikey=' + api_token2, headers=headers, data=json.dumps(body))
    #print(response.status_code + "\n" + response.json())

##
## -----------------------------------------------------------------------
##

if __name__ == "__main__":
    args = sys.argv
    delete_parameter = "disabled"
    
    anime_dub_series = []
    episodes_to_process = {}

    if args[1] == "--delete":
        print("STATUS: delete parameter enabled")
        delete_parameter = "enabled"
    else:
        print("STATUS: delete paramater NOT detected...")

    print('--------------------------------------------------')

    ## request all series from sonarr
    response = requests.get(url_animedub + '/series' + '?apikey=' + api_token, headers=headers)
    #print(response_API.status_code)
    all_dub_series = response.json()

    ## request all series from sonarr-anime
    response = requests.get(url_animesub + '/series' + '?apikey=' + api_token2, headers=headers)
    #print(response_API.status_code)
    anime_sub_series = response.json()

    ## filter out for tag 25 (dual)
    for series in all_dub_series:
        if series['tags'] == [25]:
            anime_dub_series.append(series)
            #print('found series - ' + series['title'])

    ## check for downloaded episodes in sonarr-anime
    for series in anime_sub_series:
        ## get all episodes from a single series
        response = requests.get(url_animesub + '/episode' + '?apikey=' + api_token2 + '&seriesID=' + str(series['id']), headers=headers)
        anime_episode = response.json()
        ## debug section
        print('Checking Series - ' + series['title'])
        ## loop through each episode of this anime series
        for episode in anime_episode:
            ## check if file exists on sonarr-anime side
            if episode['hasFile'] == True:
                ## if sonarr-anime has file, search anime_dub_series for match
                result = search_episodes(episode['id'], episode['tvdbId'], series['title'], anime_dub_series)
                if result:
                    #print('found episode - ' + episode['title'] + ' -- ' + str(series['title']))
                    episodes_to_process.setdefault(series['title'], []).extend([episode['title']])
                    ## only delete episodes if user has passed the "--delete" parameter
                    if delete_parameter == "enabled":
                        unmonitor_episode(episode['id'])
                        delete_episode(episode['episodeFileId'])

    ## debug section
    print('--------------------------------------------------')
    print('--- Results (delete mode: %s) ---' % delete_parameter)
    print('Found ' + str(len(episodes_to_process)) + ' series to delete')
    print('Found', sum(len(v) for v in episodes_to_process.values()), 'episodes to delete')
    print('--------------------------------------------------')
    if episodes_to_process:
        for series, episodes in episodes_to_process.items():
            print("series - " + series)
            for ep in episodes:
                print('-- ' + ep)
            print("\n")
    if episodes_to_process:
        print('--------------------------------------------------')
