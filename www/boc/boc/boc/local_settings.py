
### local_settings.py
### environment-specific settings
### example with a development environment
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'boc',
        'USER': 'root',
        'PASSWORD': 'Unfightable7!'
    }
}



STRIPE_PUBLIC_KEY = "pk_test_Wwl9beC1fBYmPmEBAxl4CxjB"
STRIPE_SECRET_KEY = "sk_test_29br76r10UWEnAn8JfCCTLTj"