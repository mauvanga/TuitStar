# TuitDTO
from datetime import datetime

import sirope

client = sirope.Sirope()

class TuitDto:

    def __init__(self, id, usr, msg):
        self._id = id
        self._usr = usr
        self._msg = msg
        self._time = datetime.now()
        self._likes = 0

    @property
    def id(self):
        return self._id

    def get_id(self):
        return self.id

    @property
    def usr(self):
        return self._usr

    @property
    def msg(self):
        return self._msg

    @property
    def time(self):
        return self._time

    @property
    def likes(self):
        return self._likes

    def darLike(self):
        self._likes = self._likes + 1

    def quitarLike(self):
        if self._likes > 0:
            self._likes = self.likes - 1

    def __str__(self):
        formattedTime = self.time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.usr} : {formattedTime} : {self.msg} ({self.likes} likes)"
