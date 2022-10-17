
from gephistreamer import graph
from gephistreamer import streamer


class gephiConnector:

    def __init__(self):
        self.url_gephi = 'localhost'
        self.port_gephi = 8080
        self.workspace_gephi = 'workspace0'

    def connect(self):
        streamG = streamer.GephiWS(
            hostname=self.url_gephi,
            port=self.port_gephi,
            workspace=self.workspace_gephi
        )
        stream = streamer.Streamer(streamG)
        return stream


