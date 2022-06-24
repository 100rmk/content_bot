import json
import logging
from datetime import datetime
from functools import partial
from typing import Optional

import requests
import requests.utils
from instaloader import Instaloader
from instaloader import (
    InstaloaderContext,
    ConnectionException,
    TwoFactorAuthRequiredException,
    BadCredentialsException,
    InvalidArgumentException
)
from instaloader.instaloadercontext import copy_session


class Instagram:
    def __init__(self, *, username: str, password: str, proxies: dict = None):
        self.__user = username
        self.__password = password
        self.__proxies = proxies

    def login(self):
        try:
            inst_loader = Instaloader()
            inst_loader.context = InstaContext(self.__proxies)
            inst_loader.login(self.__user, self.__password)
            return inst_loader
        except Exception as e:
            logging.error("Instagram connection error: %s", e)


class InstaContext(InstaloaderContext):
    def __init__(self, proxies: Optional[dict] = None):
        self.proxies = proxies if proxies else {}
        super().__init__()

    def login(self, user, passwd):
        """Not meant to be used directly, use :meth:`Instaloader.login`.

        :raises InvalidArgumentException: If the provided username does not exist.
        :raises BadCredentialsException: If the provided password is wrong.
        :raises ConnectionException: If connection to Instagram failed.
        :raises TwoFactorAuthRequiredException: First step of 2FA login done, now call
           :meth:`Instaloader.two_factor_login`."""
        # pylint:disable=import-outside-toplevel
        import http.client
        # pylint:disable=protected-access
        http.client._MAXHEADERS = 200
        session = requests.Session()
        session.proxies.update(self.proxies)
        session.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                                'ig_vw': '1920', 'ig_cb': '1', 'csrftoken': '',
                                's_network': '', 'ds_user_id': ''})
        session.headers.update(self._default_http_header())
        # Override default timeout behavior.
        # Need to silence mypy bug for this. See: https://github.com/python/mypy/issues/2427
        session.request = partial(session.request, timeout=self.request_timeout)  # type: ignore

        csrf_json = self.get_json('accounts/login/', {}, session=session)
        csrf_token = csrf_json['config']['csrf_token']
        session.headers.update({'X-CSRFToken': csrf_token})
        # Not using self.get_json() here, because we need to access csrftoken cookie
        self.do_sleep()
        # Workaround credits to pgrimaud.
        # See: https://github.com/pgrimaud/instagram-user-feed/commit/96ad4cf54d1ad331b337f325c73e664999a6d066
        enc_password = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), passwd)
        login = session.post('https://www.instagram.com/accounts/login/ajax/',
                             data={'enc_password': enc_password, 'username': user}, allow_redirects=True)
        try:
            resp_json = login.json()
        except json.decoder.JSONDecodeError as err:
            raise ConnectionException(
                "Login error: JSON decode fail, {} - {}.".format(login.status_code, login.reason)
            ) from err
        if resp_json.get('two_factor_required'):
            two_factor_session = copy_session(session, self.request_timeout)
            two_factor_session.headers.update({'X-CSRFToken': csrf_token})
            two_factor_session.cookies.update({'csrftoken': csrf_token})
            self.two_factor_auth_pending = (two_factor_session,
                                            user,
                                            resp_json['two_factor_info']['two_factor_identifier'])
            raise TwoFactorAuthRequiredException("Login error: two-factor authentication required.")
        if resp_json.get('checkpoint_url'):
            raise ConnectionException("Login: Checkpoint required. Point your browser to "
                                      "https://www.instagram.com{} - "
                                      "follow the instructions, then retry.".format(resp_json.get('checkpoint_url')))
        if resp_json['status'] != 'ok':
            if 'message' in resp_json:
                raise ConnectionException("Login error: \"{}\" status, message \"{}\".".format(resp_json['status'],
                                                                                               resp_json['message']))
            else:
                raise ConnectionException("Login error: \"{}\" status.".format(resp_json['status']))
        if 'authenticated' not in resp_json:
            # Issue #472
            if 'message' in resp_json:
                raise ConnectionException("Login error: Unexpected response, \"{}\".".format(resp_json['message']))
            else:
                raise ConnectionException("Login error: Unexpected response, this might indicate a blocked IP.")
        if not resp_json['authenticated']:
            if resp_json['user']:
                # '{"authenticated": false, "user": true, "status": "ok"}'
                raise BadCredentialsException('Login error: Wrong password.')
            else:
                # '{"authenticated": false, "user": false, "status": "ok"}'
                # Raise InvalidArgumentException rather than BadCredentialException, because BadCredentialException
                # triggers re-asking of password in Instaloader.interactive_login(), which makes no sense if the
                # username is invalid.
                raise InvalidArgumentException('Login error: User {} does not exist.'.format(user))
        # '{"authenticated": true, "user": true, "userId": ..., "oneTapPrompt": false, "status": "ok"}'
        session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self._session = session
        self.username = user
