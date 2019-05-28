import os
import wave
import pyaudio
import threading
import sys
import collections
from audio import *
from player import *


def interface(project, player):
    def trymap(x):
        try:
            if int(x) == float(x):
                return int(x)
            return float(x)
        except:
            return x

    commands = {
        'add_wav': project.add_wav,
        'add_mp3': project.add_mp3,
        'trackpoint': project.set_point,
        'trackpoints': project.trackpoints,
        'change_speed': project.change_speed,
        'change_volume': project.change_volume,
        'reverse': project.reverse,
        'play': player.play,
        'select': project.select,
        'line': project.fragments,
        'in_line': project.add_to_line,
        'out_line': project.remove_from_line,
        'export_line': project.export
    }
    while True:
        line = organize(input(), '"', '\'')
        print(line)
        command = line[0]
        if command == 'quit':
            project.close()
            break
        args = []
        if len(line) > 1:
            args = map(trymap, line[1:])
        if command in commands:
            try:
                result = commands[command]
                if isinstance(result, type(project.add_wav)):
                    result = result(*args)
                if isinstance(result, (int, str, float, list)):
                    print(result)
            except Exception as ex:
                print('Wrong count of arguments', ex)


def organize(line, *args):
    result = []
    current = ''
    sym = ''
    for i in line:
        if i in args and sym == '':
            sym = i
            continue
        if i == sym or i == ' ' and not sym:
            result.append(current)
            sym = ''
            current = ''
            continue
        current += i
    if current:
        result.append(current)
    return result


def main():
    project = Project()
    player = Player()
    interface(project, player)


if __name__ == "__main__":
    main()
