"""
Simple module for translation using Microsoft Azure Machine Translation Service
"""
import os
import uuid

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from source.utils import paginate


BASE_URL = "https://api.cognitive.microsofttranslator.com"
RELATIVE_URL = "/translate"
ENDPOINT = BASE_URL + RELATIVE_URL


try:
    KEY = os.environ["TRANSLATOR_TEXT_KEY"]    # MS Azure Translation key
except KeyError:
    print("Environment variable TRANSLATOR_TEXT_KEY is not set.")
    raise


def post_translate(source_text, to, from_=None):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = {
            "Ocp-Apim-Subscription-Key": KEY,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4())
        }

    params = {
            "api-version": "3.0",
            "to": to,
            "textType": "html"
        }
    if from_ is not None:
        params["from"] = from_

    if type(source_text) == str:
        body = [{"text": source_text}]
    else:
        body = [{"text": source_text} for source_text in source_text]

    r = session.post(ENDPOINT, headers=headers, params=params, json=body)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        # Error handling
        print("Error: {code} - {message}".format(**r.json()['error']))
        raise

    if type(source_text) == str:
        return r.json()[0]["translations"][0]["text"]
    else:
        return [t['translations'][0]['text'] for t in r.json()]


def translate(source_text, to, from_=None):
    """
    Make a translation request to the Microsoft Azure Translation Text Service

    Source text can either be a single string to translate or a list of strings

    If no source language is specified the service will detect the language

    The Microsoft azure request has limitations on size:
        * Each request must have no more than 100 lines to translate
        * The combined characters of each request must be less than 5000

    This function will automatically page through the supplied list of strings
    in order to not breach those limits.
    """
    if type(source_text) == str:
        return post_translate(source_text, to=to, from_=from_)
    else:
        translations = []
        for page in paginate(source_text, max_buffer=5000, max_lines=100):
            translations += post_translate(page, to=to, from_=from_)
        return translations
