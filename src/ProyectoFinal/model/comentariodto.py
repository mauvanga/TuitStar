# TuitDTO
from datetime import datetime

class ComentarioDto:

    def __init__(self,id,usr,contenido,tuit):
        self._id = id
        self._contenido = contenido
        self._time = datetime.now()
        self._usr = usr
        self._tuit = tuit

    @property
    def id(self):
        return self._id

    @property
    def contenido(self):
        return self._contenido

    @property
    def tuit(self):
        return self._tuit

    @property
    def time(self):
        return self._time

    @property
    def usr(self):
        return self._usr

    def __str__(self):
        formattedTime = self.time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.usr} : {formattedTime} : {self.contenido}"