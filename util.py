import random

import flask


def generate_username():
    """
    If no username is provided, generate a random one and return it
    """   
    username = flask.request.args.get("usr")
    if username is None:
        username = str(random.randint(1001, 9998))
    else:
        username = username + str(random.randint(1001, 9998))
    return username