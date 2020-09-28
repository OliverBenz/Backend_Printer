# Configuration
Under the `conDB` function in [main.py](../main.py), set the database information to fit your setup. 

    db = mysql.connector.connect(
        host="[mysq-ip]",
        user="[mysq-username]",
        passwd="[mysql-password]",
        database="[mysql_databasename]"
    )

By default, the backend will connect over port 3004. This can be changed under `app.run(host='0.0.0.0', port=3004)` in the [main.py](../main.py).
