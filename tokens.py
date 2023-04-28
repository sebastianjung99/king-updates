import mysql.connector as mariadb

import tools

db_login = tools.get_json("secrets.json")
mariadb_user = db_login['MARIADB']['USER']
mariadb_pwd = db_login['MARIADB']['PASSWORD']

mariadb_connection = mariadb.connect(user=mariadb_user, password=mariadb_pwd, database="king-updates", host="localhost", port="3306")
cursor = mariadb_connection.cursor(dictionary=True)

sql_statement = "SELECT * from secrets"
cursor.execute(sql_statement)
res = cursor.fetchall()

mariadb_connection.close()

SECRETS = {
    "DISCORD": {
        "BOT_TOKEN": res[0]['client']
    },    
    "TWITTER": {
        "CLIENT": res[2]['client'],
        "SECRET": res[2]['client_secret'],
        "BEARER": res[2]['bearer'],
        "OAUTH": res[2]['oauth'],
        "OAUTH_SECRET": res[2]['oauth_secret']
    },
    "TWITCH": {
        "CLIENT": res[1]['client'],
        "SECRET": res[1]['client_secret'],
        "OAUTH": res[1]['oauth']
    }
}

print("end")