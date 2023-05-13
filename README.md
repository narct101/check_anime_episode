# check_anime_episode
This script will monitor 2 Sonarr instances and delete episodes in the second instance if both have the same episode. For example, if you ahve 2 Sonarr instances (#1 for dual anime episodes and #2 for subbed anime only). The second instance will download the subbed anime first, but eventually the dual anime episodes will be acquired. How do you delete the subbed only anime episodes? This script is designed to remove the unwanted subbed only episodes.

## Edit Script for your environment
Make sure to change the url and api tokens to your instances.

Also change the series['tags'] value to whatever anime tag you use in the 1st Sonarr instance.  For example I use the "dual" tag to differentiate my anime series to only download dual audio anime.  You can get this value by running the below command.

### run this in powershell or linux command line
curl --request GET http://sonarr.sshlab.io/api/v3/tag?apikey=API_KEY_FOR_SONARR_DUB

## Parameters
If you include the "--delete" parameter the script will tell the 2nd Sonarr instance to delete it's episodes. If anything else is passed, the script will not delete any episodes and show you what can be deleted.

python3 check_anime_episodes.py --delete
