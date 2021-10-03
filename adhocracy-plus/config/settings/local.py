# replace 'your.domain' with your desired domain
BASE_URL = 'https://adhocracy18.home'
#ALLOWED_HOSTS = [u'adhocracy18',u'adhocracy18.home', u'localhost']
ALLOWED_HOSTS = [u'*']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# database config - we recommend postgresql for production purposes
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'aplus-test-database',
  }
}

# forward outgoing emails to a local email proxy
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='127.0.0.1'

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False

# General settings
CONTACT_EMAIL = 'contact@adhocracy18'

# folder for user-uploads, directly served from the webserver (see nginx example below). Must be created manually.
MEDIA_ROOT='/var/local/media'

# replace the value below with some random value
SECRET_KEY = u'a§527g48htr6z%ewrzfe98jg5gb7swhftzde'
PRIVKEY=SECRET_KEY
# some basic security settings for serving the website over https - see django docu
CSRF_COOKIE_SECURE=True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True


FILE_UPLOAD_PERMISSIONS = 0o644

# Default X-Frame-Options header value
#X_FRAME_OPTIONS = 'SAMEORIGIN'

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

CAPTCHA_URL= 'https://captcheck.netsyms.com/api.php'
#CAPTCHA_TEST_ACCEPTED_ANSWER='true'


