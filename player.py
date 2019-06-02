import pyaudio
import threading
import time


class Player:
    def __init__(self, sampwidth=2, channels=2, rate=44100):
        self.pyaudio = pyaudio.PyAudio()
        self.player = self.pyaudio.open(format=self
                                        .pyaudio
                                        .get_format_from_width(sampwidth),
                                        channels=channels,
                                        rate=rate,
                                        output=True)
        self.sampwidth = sampwidth
        self.channels = channels
        self.rate = rate
        self.pos = 0

        self._thread = threading.Thread()
        self._thread.start()
        self._data = None
        self._nframes = 0
        self._frame_size = self.rate * self.channels * self.sampwidth

        self._pause = True

    def play(self, data=None):
        if data is not None:
            self.stop()
            time.sleep(0.01)
            self._data = data
            self._nframes = len(self._data) / self._frame_size
        self._pause = False
        self._thread = threading.Thread(target=self._play)
        self._thread.start()

    def _play(self):
        if self.pos >= self._nframes:
            self.pos = self._nframes
            self.pause()
        while not self._pause:
            self.player.write(self._data[self.pos * self._frame_size:(
                                        self.pos + 1) * self._frame_size])
            self.pos += 1

    def back(self, time=1):
        time = time * self.rate
        self.pos -= time
        if self.pos < 0:
            self.pos = 0
        time.sleep(0.001)

    def forward(self, time=1):
        time = time * self.rate
        self.pos += time
        if self.pos >= self._nframes:
            self.pos = self._nframes
        time.sleep(0.001)

    def pause(self):
        self._pause = True

    def stop(self):
        self._pause = True
        self.pos = 0

    def close(self):
        self.stop()
        time.sleep(0.01)
        self.player.close()
        self.pyaudio.terminate()

    @property
    def fulltime(self):
        try:
            return self._nframes / self._frame_size / self.rate
        except ZeroDivisionError:
            return 0

    @property
    def currenttime(self):
        try:
            return self.pos / self._nframes / self._frame_size / self.rate
        except ZeroDivisionError:
            return 0

    @property
    def isworking(self):
        return not self._pause
