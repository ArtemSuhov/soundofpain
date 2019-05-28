import os
import helpers
import wave
from pydub import AudioSegment
from pydub import effects
from classes import *


class Project:
    def __init__(self):
        self.files = {}
        self.fragments = []

        self.current_track = None

        self.rate = 44100
        self.channels = 2
        self.sampwidth = 2

    def add_wav(self, path):
        path = str(path) + ".wav"
        if not path or not os.path.exists(path):
            return "FAIL"
        track = Track(path)
        self.files[track.filename] = track
        return "OK"

    def add_mp3(self, path):
        path = str(path) + ".mp3"
        if not path or not os.path.exists(path):
            return "FAIL"
        song = AudioSegment.from_mp3(path)
        song.export(path[:len(path) - 4] + "_temp.wav", format="wav")
        track = Track(path[:len(path) - 4] + "_temp.wav")
        self.files[track.filename] = track
        self.select(track.filename)
        return "OK"

    def select(self, index):
        index = self._index_to_name(index)
        print(index)
        if not index:
            return "FAIL"
        self.current_track = self.files[index]
        return "OK"

    def set_point(self, time=None):
        if not time:
            time = 0
        if not isinstance(time, (int, float)):
            raise TypeError('Please, give me right time!')
        if time * self.rate >= self.current_track.nframes or time < 0:
            raise IndexError('Please, give me right time!')
        if time not in self.current_track.trackpoints:
            self.current_track.trackpoints.append(time)

    def trackpoints(self, track=None):
        track = self._index_to_name(track)
        if not track:
            track = self.current_track.filename
        self.files[track].trackpoints = sorted(self.files[track].trackpoints)
        return self.files[track].trackpoints.__repr__()

    def change_volume(self, path, coefficient):
        song = AudioSegment.from_file(path)
        song = song + coefficient
        song.export(path[:len(path) - 4] + "_louder.wav", format="wav")
        return "_louder.wav is ready"

    def reverse(self, path):
        song = AudioSegment.from_file(path)
        song.reverse().export(path[:len(path) - 4] + "_reverse.wav", format="wav")
        return "_reverse.wav is ready"

    def change_speed(self, path, coefficient):
        song = AudioSegment.from_file(path)
        effects.speedup(song, coefficient).export(path[:len(path) - 4] + "_speedup.wav", format="wav")
        return "_speedup.wav is ready"

    def add_to_line(self, begin_index, end_index, begin_in_project=None):
        if (begin_index >= end_index or begin_index >= len(self.current_track.trackpoints) or
                end_index >= len(self.current_track.trackpoints)):
            return False

        if not begin_in_project:
            begin_in_project = 0

        fragment = Track_in_line(self.current_track, begin_in_project, begin_index, end_index)
        if fragment not in self.fragments:
            self.fragments.append(fragment)

    def remove_from_line(self, project_num):
        del self.fragments[(project_num)]

    def _index_to_name(self, index):
        if isinstance(index, int) and index - 1 < len(self.files.keys()):
            index = list(self.files.keys())[index - 1]

        if index in self.files:
            return index
        return None

    def compile_fragment(self, start, end):
        result = [0 for i in range(int((end - start) * self.rate * self.channels))]
        for fragment in self.fragments:
            if fragment.start < end and fragment.end > start:
                data = fragment.get_data(start - fragment.start,
                                         min(end, fragment.end) - max(fragment.start, start))
                index = max(0, fragment.start - start)
                for i in helpers.bytes_to_numbers(data, self.sampwidth):
                    result[index] += int(i)
                    index += 1
        return helpers.numbers_to_bytes(result, self.sampwidth)

    def export(self, filename, start, end):
        with wave.open(filename, mode='wb') as f:
            f.setnchannels(self.channels)
            f.setsampwidth(self.sampwidth)
            f.setframerate(self.rate)
            i = 0
            for i in range(start, end, 5):
                f.writeframes(self.compile_fragment(i, i + 5))
        return 'OK'
