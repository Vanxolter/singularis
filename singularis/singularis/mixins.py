import requests
from singularis import settings


def reCAPTCHAValidation(token):
    ''' reCAPTCHA validation '''
    result = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token
        })

    return result.json()