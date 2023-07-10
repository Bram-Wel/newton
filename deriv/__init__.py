#!/usr/bin/python3
"""deriv package."""


from flask import Flask
from flask_login import LoginManager

import random
import asyncio
import json

# import deriv.models as models


app = Flask(__name__)
key = random.uniform(3.7, 13.1).hex()
app.config['SECRET_KEY'] = key
# deriv = __import__('deriv')
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# import deriv.models as models
from deriv.models import get_symbols
active_symbols = asyncio.run(get_symbols())

from deriv import routes

# authorise = asyncio.run(models.get_authorise(routes.api_key)
#                           ) if routes.api_key else None
