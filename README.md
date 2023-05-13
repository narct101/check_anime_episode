# check_anime_episode
This script will monitor 2 Sonarr instances and delete episodes in the second instance if both have the same episode. For example, if you ahve 2 Sonarr instances (#1 for dual anime episodes and #2 for subbed anime only). The second instance will download the subbed anime first, but eventually the dual anime episodes will be acquired. How do you delete the subbed only anime episodes? This script is designed to remove the unwanted subbed only episodes.

## Parameters
If you include the "--delete" parameter the script will tell the 2nd Sonarr instance to delete it's episodes. If anything else is passed, the script will not delete any episodes and show you what can be deleted.

python3 check_anime_episodes.py --delete
