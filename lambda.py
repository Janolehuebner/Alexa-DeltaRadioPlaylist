#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import requests
import datetime

def songdata():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    now_minus_10 = now - datetime.timedelta(minutes=10)
    now_formatted= now.strftime('%Y-%m-%dT%H:%M:%S')
    now_minus_10_formated = now_minus_10.strftime('%Y-%m-%dT%H:%M:%S')

    request = requests.get('http://www.deltaradio.de/iris-search-live.json', params={"start": now_minus_10_formated, "end": now_formatted})
    data= request.json()
    song = data['result']['entry'][0]['song']['entry'][0]['title']
    artist = data['result']['entry'][0]['song']['entry'][0]['artist']['entry'][0]['name']
    return song+" von "+artist


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "Deltaradio Playlist (inoffiziell)",
            'content':  output
        },
        'shouldEndSession': True
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------

def get_response():

    session_attributes = {}
    card_title = "Deltaradio Playlist (inoffiziell) - Gerade läuft"
    speech_output = "Gerade läuft "+songdata()

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output))

def get_help_response():

    session_attributes = {}
    card_title = "Deltaradio Playlist (inoffiziell) - Hilfe"
    speech_output = "Ich kann dir sagen, was gerade bei Deltaradio läuft."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output))

# --------------- Events ------------------

def on_launch(launch_request, session):
    return get_response()

def on_intent(intent_request, session):

    intent_name = intent_request['intent']['name']

    if intent_name == "PlaylistIntent":
        return get_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    raise ValueError("Invalid intent")

# --------------- Main handler ------------------

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
