import mysql.connector as mariadb
import requests

import tools


SECRETS = {}


def get_tokens():
    """
    Extracts all api tokens from the database and saves it to a global dict. Saves database traffic and
    performance. Don't really have to care about security for this program...
    """

    mariadb_connection, cursor = tools.get_db_connection()

    sql_statement = "SELECT * from secrets"
    cursor.execute(sql_statement)
    res = cursor.fetchall()

    mariadb_connection.close()

    global SECRETS
    SECRETS = {
    "DISCORD": {
        "BOT_TOKEN": res[0]['client']
    },
    "TWITCH": {
        "CLIENT": res[1]['client'],
        "SECRET": res[1]['client_secret'],
        "OAUTH": res[1]['oauth']
    },    
    "TWITTER": {
        "CLIENT": res[2]['client'],
        "SECRET": res[2]['client_secret'],
        "BEARER": res[2]['bearer'],
        "OAUTH": res[2]['oauth'],
        "OAUTH_SECRET": res[2]['oauth_secret']
    }
}


def check_tokens():
    """
    Checks twitch oauth (user) token. Requests and stores a new one if old one is expired 
    or about to.
    """

    headers = {'Authorization': f"OAuth {SECRETS['TWITCH']['OAUTH']}"}
    r = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)
    # check if token is valid
    if r.status_code == 200:
        tools.LOGGER.info("Twitch user token validated.")
    # token not valid, request new one
    elif r.status_code == 401:
        # get new token
        r = requests.post(f"https://id.twitch.tv/oauth2/token?grant_type=client_credentials&client_id={SECRETS['TWITCH']['CLIENT']}&client_secret={SECRETS['TWITCH']['SECRET']}")
        r = r.json()
        oauth_new = r['access_token']

        # store new token
        mariadb_connection, cursor = tools.get_db_connection()
        sql_statement = "UPDATE secrets SET oauth = %s WHERE app = %s"
        values = (oauth_new, 'twitch')
        cursor.execute(sql_statement, values)
        mariadb_connection.commit()
        mariadb_connection.close()
        
        tools.LOGGER.info("Aquired new Twitch user token.")
    # something went wrong
    else:
        tools.LOGGER.error(f"Error checking Twitch user token: {r.text}")
