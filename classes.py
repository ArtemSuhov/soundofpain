import wave
import os


class Track_in_line:
    def __init__(self, track, start, begin, end):
        self.track = track
        self.track.trackpoints = sorted(self.track.trackpoints)
        self.begin = self.track.trackpoints[begin]
        self.length = (self.track.trackpoints[end] - self.begin)
        self.start = start

    def get_data(self, begin=0, length=None):
        if begin < 0:
            begin = 0
        if length is None:
            length = self.length - begin
        return self.track.read_frames(self.begin + begin, length)

    @property
    def end(self):
        return self.begin + self.length

    def __repr__(self):
        return (f'{self.track} at {self.start} seconds from '
                f'{self.begin} seconds by {self.length} seconds')


class Track:
    def __init__(self, path):
        self.filename = os.path.basename(path)
        self.path = path
        self.format = path.split('.')[1]
        if self.format != 'wav':
            raise ValueError('Wrong file format')

        track = wave.open(path, 'rb')
        self.nframes = track.getnframes()
        self.sampwidth = track.getsampwidth()
        self.nchannels = track.getnchannels()
        self.rate = track.getframerate()
        self.framesize = self.nchannels * self.sampwidth

        self.trackpoints = [0, self.time]

    def read_frames(self, begin=0, length=None):
        if length is None:
            length = self.time
        with wave.open(self.path, mode='rb') as wav:
            wav.readframes(int(begin * self.rate))
            return wav.readframes(int(length * self.rate))

    @property
    def time(self):
        return round(self.nframes / self.rate, 2)

    def __repr__(self):
        return f'{self.path}'
