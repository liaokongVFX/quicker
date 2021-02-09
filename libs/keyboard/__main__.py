# -*- coding: utf-8 -*-
import hotkey
import fileinput
import json
import sys

def print_event_json(event):
    print(event.to_json(ensure_ascii=sys.stdout.encoding != 'utf-8'))
    sys.stdout.flush()
hotkey.hook(print_event_json)

parse_event_json = lambda line: hotkey.KeyboardEvent(**json.loads(line))
hotkey.play(parse_event_json(line) for line in fileinput.input())