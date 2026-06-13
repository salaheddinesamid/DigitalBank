from datetime import date


def generate_user_credentials(first_name, last_name, CIN):
    username = "{}{}{}".format(str(first_name)[0].upper(), str(last_name)[0].upper(), CIN)
    password = "{}{}{}{}".format(str(last_name).upper(), str(first_name).upper(), CIN, date.today().year)

    return {
        "username" : username,
        "password" : password
    }
