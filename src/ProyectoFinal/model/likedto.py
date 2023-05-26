#   LikeDTO

class LikeDto:

    def __init__(self,usr,tuit):
        self._usr = usr
        self._tuit = tuit

    @property
    def tuit(self):
        return self._tuit

    @property
    def usr(self):
        return self._usr

    def __str__(self):
        return f"{self.usr} : {self.tuit}"