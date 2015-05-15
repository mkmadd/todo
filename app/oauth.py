"""
    OAuth Sign In code
    Miguel Grinberg's code
    https://github.com/miguelgrinberg/flask-oauth-example
    https://github.com/miguelgrinberg/flask-oauth-example/blob/master/oauth.py
    
    modified by Michael K. Maddeford
    modified to add Google and Github in addition to Facebook and Twitter
    modified to add crsf protection and token revoke
    all comments provided by MKM
    
"""

from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session, abort
# library imports below added by MKM
from json import loads
from flask_wtf.csrf import generate_csrf, validate_csrf
from urllib import urlencode
from requests import get, delete
from flask.ext.login import current_user

# added revoke method
class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass
    
    # Revoke access_token.  Handled differently by each provider
    def revoke(self, access_token):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


# Added by MKM
class GoogleSignIn(OAuthSignIn):
    # initialize with provider-specific info
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            base_url='https://www.googleapis.com/oauth2/v1/'
        )

    # set parameters of request (e.g. scope, state) and redirect to provider's
    # authorization url for authorization code
    def authorize(self):
        params = {
            'scope': 'openid email',
            'state' : generate_csrf(),
            'response_type': 'code',
            'redirect_uri': self.get_callback_url(),
            'approval_prompt': 'force'
        }
        return redirect(self.service.get_authorize_url(**params))

    # Handle provider callback.  Validate csrf, exchange authorization 
    # code for access token, then use access token to access user info
    def callback(self):
        # Make sure CSRF token was returned and is valid
        if not validate_csrf(request.args.get('state')):
            abort(403)

        if 'code' not in request.args:
            return None, None, None

        # exchange authorization code for access token
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=loads   # unique to Google; had to add decoder to work
        )

        # store access token for later revocation
        session['access_token'] = oauth_session.access_token

        # get user info
        userinfo = oauth_session.get('userinfo').json()
        
        # Google returns:
        # {u'family_name', u'name', u'picture', u'gender', u'email', 
        # u'link', u'given_name', u'id', u'verified_email'}
        
        social_id = 'google${}'.format(userinfo['id'])
        name = userinfo.get('given_name')
        email = userinfo.get('email')
        return (
            social_id,
            name,
            email
        )
    
    # Revoke access token, forcing user to login again on logout
    def revoke(self, access_token):
        url = ('https://accounts.google.com/o/oauth2/revoke?'
               'token={}').format(access_token)
        result = get(url)
        return result.status_code


# Added by MKM
class GithubSignIn(OAuthSignIn):
    # initialize with provider-specific info
    def __init__(self):
        super(GithubSignIn, self).__init__('github')
        self.service = OAuth2Service(
            name='github',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://github.com/login/oauth/authorize',
            access_token_url='https://github.com/login/oauth/access_token',
            base_url='https://api.github.com/'
        )

    # set parameters of request (e.g. scope, state) and redirect to provider's
    # authorization url for authorization code
    def authorize(self):
        params = {
            'scope': 'user:email',
            'state' : generate_csrf(),
            'response_type': 'code',
            'redirect_uri': self.get_callback_url(),
        }
        return redirect(self.service.get_authorize_url(**params))

    # Handle provider callback.  Validate csrf, exchange authorization 
    # code for access token, then use access token to access user info
    def callback(self):
        # Make sure CSRF token was returned and is valid
        if not validate_csrf(request.args.get('state')):
            abort(403)
        if 'code' not in request.args:
            return None, None, None

        # exchange authorization code for access token
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'redirect_uri': self.get_callback_url()
            }
        )

        # store access token for later revocation
        session['access_token'] = oauth_session.access_token

        # get user info
        userinfo = oauth_session.get('user').json()

        # Github returns:
        # {u'site_admin', u'subscriptions_url', u'gravatar_id', u'id', 
        # u'followers_url', u'following_url', u'followers', u'type',
        # u'public_repos', u'gists_url', u'events_url', u'html_url', 
        # u'updated_at', u'received_events_url', u'starred_url', 
        # u'public_gists', u'organizations_url', u'url', u'created_at', 
        # u'avatar_url', u'repos_url', u'following', u'login'}

        social_id = 'github${}'.format(userinfo['id'])
        name = userinfo.get('given_name') or userinfo.get('login')
        email = userinfo.get('email')
        return (
            social_id,
            name,
            email
        )

    # Revoke access token, forcing user to login again on logout
    def revoke(self, access_token):
        url = ('https://api.github.com/applications/{0}/tokens/'
               '{1}').format(self.consumer_id, access_token)
        result = delete(url, auth=(self.consumer_id, self.consumer_secret))
        return result.status_code


# Modified by MKM to add CSRF protection and revoke
class FacebookSignIn(OAuthSignIn):
    # initialize with provider-specific info
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    # set parameters of request (e.g. scope, state) and redirect to provider's
    # authorization url for authorization code
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            state=generate_csrf(),
            redirect_uri=self.get_callback_url())
        )

    # Handle provider callback.  Validate csrf, exchange authorization 
    # code for access token, then use access token to access user info
    def callback(self):
        # Make sure CSRF token was returned and is valid
        if not validate_csrf(request.args.get('state')):
            abort(403)
        if 'code' not in request.args:
            return None, None, None
        
        # exchange authorization code for access token
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )

        # store access token for later revocation
        session['access_token'] = oauth_session.access_token
        
        # get user info
        userinfo = oauth_session.get('me').json()
        
        # Facebook returns:
        # {u'first_name', u'last_name', u'middle_name', u'name', u'locale', 
        # u'gender', u'verified', u'email', u'link', u'timezone', 
        # u'updated_time', u'id'}

        social_id = 'facebook${}'.format(userinfo['id'])
        name = userinfo.get('first_name') or userinfo.get('name')
        email = userinfo.get('email')
        return (
            social_id,
            name,
            email
        )

    # Revoke access token, forcing user to login again on logout
    def revoke(self, access_token):
        facebook_id = current_user.social_id.replace('facebook$', '')
        url = 'https://graph.facebook.com/{}/permissions'.format(facebook_id)
        result = delete(url, params={'access_token': access_token})
        return result.status_code


# Modified by MKM to add CSRF protection
class TwitterSignIn(OAuthSignIn):
    # initialize with provider-specific info
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    # set parameters of request (e.g. scope, state) and redirect to provider's
    # authorization url to get request token
    def authorize(self):
        csrf = generate_csrf()
        # Even using urllib.urlencode, the csrf token was getting cut off at
        # the hashes.  Needed to send it in two parts and reassemble it
        csrf_spl = csrf.split('##')
        q_str = urlencode({ 'state0': csrf_spl[0], 'state1': csrf_spl[1] })
        request_token = self.service.get_request_token(
            params={ 'oauth_callback':  \
                    '{0}?{1}'.format(self.get_callback_url(), q_str)}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    # Handle provider callback.  Validate csrf, exchange authorization 
    # code for access token, then use access token to access user info
    def callback(self):
        # Reassemble two parts of csrf token and join with two hashes
        csrf_p0 = request.args.get('state0')
        csrf_p1 = request.args.get('state1')
        csrf = '##'.join((csrf_p0, csrf_p1))
        
        # Make sure CSRF token was returned and is valid
        if not validate_csrf(csrf):
            abort(403)
            
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None
        
        # exchange request token for access token
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        
        # save for later (don't actually use this one)
        session['access_token'] = oauth_session.access_token
        
        # get user info
        userinfo = oauth_session.get('account/verify_credentials.json').json()
        
        # Twitter returns:
        # {u'follow_request_sent', u'profile_use_background_image', 
        # u'default_profile_image', u'id', 
        # u'profile_background_image_url_https', 
        # u'verified', u'profile_text_color', u'profile_image_url_https', 
        # u'profile_sidebar_fill_color', u'entities': {u'description': 
        # {u'urls': []}}, u'followers_count', u'profile_sidebar_border_color', 
        # u'id_str', u'profile_background_color', u'listed_count', 
        # u'is_translation_enabled', u'utc_offset', u'statuses_count', 
        # u'description', u'friends_count', u'location', u'profile_link_color', 
        # u'profile_image_url', u'following', u'geo_enabled', 
        # u'profile_background_image_url', u'screen_name', u'lang', 
        # u'profile_background_tile', u'favourites_count', u'name', 
        # u'notifications', u'url', u'created_at', u'contributors_enabled', 
        # u'time_zone', u'protected', u'default_profile', u'is_translator'}
        
        social_id = 'twitter${}'.format(userinfo['id'])
        name = userinfo.get('screen_name')
        email = userinfo.get('email')   # twitter does not easily provide email
        return (
            social_id,
            name,
            email
        )

    def revoke(self, access_token):
        # Twitter forces a login every time and don't see a way to revoke token
        # Just return 200
        return 200
