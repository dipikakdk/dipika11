

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
"""__file__ in settings.py → "c:/project/hospitalmanagement/settings.py"
os.path.abspath(__file__) → "c:/project/hospitalmanagement/settings.py" (absolute path)
os.path.dirname(step2) → "c:/project/hospitalmanagement" (first parent)
os.path.dirname(step3) → "c:/project" (second parent = BASE_DIR)"""
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates') #os.path.join() combines base_dir with templates to create a full path  for example If BASE_DIR is /project/, then TEMPLATE_DIR becomes /project/templates/
STATIC_DIR=os.path.join(BASE_DIR,'static')




# Django automatically generates a secret key and puts it in settings.py,password of project 
SECRET_KEY = 'hpbv()ep00boce&o0w7z1h)st148(*m@6@-rk$nn)(n9ojj4c0'

#show errors
DEBUG = True

#all host allowed
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', #Provides the admin interface
    'django.contrib.auth', # Handles user authentication like login,logout,password 
    'django.contrib.contenttypes', #track all the models (tables) in project
    'django.contrib.sessions', #keeps track of users while they use the website.It stores information like login status or preferences between pages
    'django.contrib.messages', #Handles temporary messages to users (success/error)
    'django.contrib.staticfiles', #Manages static files (CSS, JS, images)
        'hospital', # main application for the hospital management system
        'widget_tweaks', #third_parrty apps for helps with form styling and customization
]

#Middleware is a set of tools that work automatically to handle
#  security, sessions, authentication, and messages in project
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', # Adds security features like HTTPS and headers
    'django.contrib.sessions.middleware.SessionMiddleware', # Manages user sessions
    'django.middleware.common.CommonMiddleware', # Handles URL normalization, redirects, and common tasks
    'django.middleware.csrf.CsrfViewMiddleware',  # Protects against CSRF attacks (security)
    'django.contrib.auth.middleware.AuthenticationMiddleware', #Manages user authentication
    'django.contrib.messages.middleware.MessageMiddleware',   # Handles temporary messages to users
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protects against clickjacking attacks
]

ROOT_URLCONF = 'hospitalmanagement.urls' #Points to hospitalmanagement/urls.py where all URL patterns are defined

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,  # If True, Django looks for templates in each app's templates directory
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
#WSGI is the interface between Django and the web server.This setting tells Django which file to use to run the project on a server.
WSGI_APPLICATION = 'hospitalmanagement.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital_management',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', default_storage_engine=INNODB, sql_require_primary_key=OFF",
            'charset': 'utf8mb4', #utf8mb4 is a character set that supports a wide range of characters including emojis and special characters
            'autocommit': True, #automatically commits transactions
            'connect_timeout': 5, #timeout for connection in 5 second 
        },
#These settings are used when running tests in Django to ensure data encoding is correct.        
        'TEST': {
            'CHARSET': 'utf8mb4', 
            'COLLATION': 'utf8mb4_unicode_ci',
        },
    }
}




AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Base URL to use when referring to static files
STATIC_URL = '/static/'

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (Uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Create necessary directories if they don't exist
os.makedirs(MEDIA_ROOT, exist_ok=True)
os.makedirs(os.path.join(MEDIA_ROOT, 'profile_pic'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'static', 'images'), exist_ok=True)

# Simplified static file finder configuration
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

LOGIN_REDIRECT_URL = '/afterlogin'

# Redirect URL after logout
LOGOUT_REDIRECT_URL = '/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#for contact us give your gmail id and password
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'from@gmail.com' # this email will be used to send emails
EMAIL_HOST_PASSWORD = 'xyz' # host email password required
# now sign in with your host gmail account in your browser
# open following link and turn it ON
# https://myaccount.google.com/lesssecureapps
# otherwise you will get SMTPAuthenticationError at /contactus
# this process is required because google blocks apps authentication by default
EMAIL_RECEIVING_USER = ['dipikakdk11@gmail.com'] # email on which you will receive messages sent from website
