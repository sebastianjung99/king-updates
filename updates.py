import requests

import tools
import tokens


def get_twitch_status(channel_name):
    """
    Checks if twitch channel is live.

    Parameters:
    ------------
    channel_name: :class:`String`
        Channel name to check.

    Returns:
    ------------
    :class:`bool`
        Wether channel is live or not.
    :class:`String`
        Stream title.
    """

    headers = {
        'Authorization': f"Bearer {tokens.SECRETS['TWITCH']['OAUTH']}",
        'Client-Id': tokens.SECRETS['TWITCH']['CLIENT']
    }
    r = requests.get(f'https://api.twitch.tv/helix/streams?user_login={channel_name}', headers=headers)

    # check if request was successful
    if r.status_code == 200:
        r = r.json()
    else:
        tools.LOGGER.error(f"Error checking Twitch user: {r.text}")

    # r['data'] should be filled if channel is live
    if len(r['data']) > 0:
        return True, r['data'][0]['title']
    else:
        return False, ""