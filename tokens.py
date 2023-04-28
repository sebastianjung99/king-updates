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
