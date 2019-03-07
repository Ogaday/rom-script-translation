"""
Simple module for translation using Microsoft Azure Machine Translation Service
"""
import os
import uuid

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


BASE_URL = "https://api.cognitive.microsofttranslator.com"
RELATIVE_URL = "/translate"
ENDPOINT = BASE_URL + RELATIVE_URL


try:
    KEY = os.environ["TRANSLATOR_TEXT_KEY"]    # MS Azure Translation key
except KeyError:
    print("Environment variable TRANSLATOR_TEXT_KEY is not set.")
    raise


def translate(source_text, to, from_=None):
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

    body = [
            {
                "text": source_text
            }
        ]

    r = session.post(ENDPOINT, headers=headers, params=params, json=body)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        # Error handling
        print("Error: {code} - {message}".format(**r.json()['error']))
        raise

    return r.json()[0]["translations"][0]["text"]


def bulk_translate(source_texts, to, from_=None):
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

    body = [{"text": source_text} for source_text in source_texts]

    r = session.post(ENDPOINT, headers=headers, params=params, json=body)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        # Error handling
        print("Error: {code} - {message}".format(**r.json()['error']))
        raise

    return [t['translations'][0]['text'] for t in r.json()]
