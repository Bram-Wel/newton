#!/usr/bin/python3
"""Module describes functions that get data using the derivAPI."""

from deriv_api import DerivAPI
from rx import Observable
from flask_login import UserMixin

from deriv import login_manager, json


async def get_symbols():
    """Get active symbols.

    Return: Active Symbols
    """
    api = DerivAPI(app_id=1089)
    resp = await api.active_symbols({'active_symbols': "full",
                                     'product_type': "basic"})
    return resp['active_symbols']


async def get_authorise(api_token):
    """Authorize deriv account.

    Args:
        api_token (str): API token for the deriv account
    Return: Account information
    """
    api = DerivAPI(app_id=1089)
    if api_token:
        authorize = await api.authorize({'authorize': api_token})
    else:
        raise "Invalid Token! (Empty)"
    return authorize


@login_manager.user_loader
def load_user(user_id):
    """User loader callback."""
    # with open('deriv/deriv.json', encoding='utf-8') as file:
    #   authorise = json.load(file)
    # return User.get(user_id)
    # user = User(authorise['fullname'], authorise['loginid'],
    #            authorise['user_id'], authorise['email'],
    #            authorise['balance'], authorise['currency'])
    # return user if user.id == user_id else None
    from deriv.routes import user
    return user


class User(UserMixin):
    """User class for flask login manager."""

    # def __init__(self, fullname, loginid, user_id,
    #             email="", balance=0, currency="USD"):
    #    """Initialise class."""
    #    self.fullname = fullname
    #    self.loginid = loginid
    #    self.id = user_id
    #    self.email = email
    #    self.balance = balance
    #    self.currency = currency
    def __init__(self, arg):
        """Initialise class."""
        for key, value in arg.items():
            self.__setattr__(key, value)
        self.id = self.user_id
        del self.user_id

    @property
    def pretty_balance(self):
        """Print the balance prettily."""
        if len(str(self.balance)) > 3:
            return f"{self.balance:,} {self.currency}"
        return f"{self.balance} {self.currency}"
