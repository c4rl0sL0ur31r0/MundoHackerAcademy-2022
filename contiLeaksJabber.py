import csv
import io
import requests
from commonregex import CommonRegex
from gephistreamer import graph

from gephiConnector import gephiConnector


class contiLeaksJabber:
    def __init__(self):
        self.urls = [
            'https://raw.githubusercontent.com/NorthwaveSecurity/complete_translation_leaked_chats_conti_ransomware/main/jabber_chat_2020_translated.csv',
            'https://raw.githubusercontent.com/NorthwaveSecurity/complete_translation_leaked_chats_conti_ransomware/main/jabber_chat_2021_2022_translated.csv'
        ]
        self.stream = gephiConnector().connect()

    @staticmethod
    def __parser_actor(jabber):
        data = {}
        # print(jabber)
        if '@' in jabber:
            actor = jabber.split('@')
            name_actor = actor[0]
            domain = actor[1]
            # if domain != 'q3mcco35auwcstmt.onion':
            #    print(name_actor, domain)
            data['nameActor'] = name_actor.lower().strip()
            data['domainActor'] = domain
        else:
            data['nameActor'] = jabber
        print(data['nameActor'])
        return data

    @staticmethod
    def __get_url(url):
        r = requests.get(url)
        buff = io.StringIO(r.text)
        dr = csv.DictReader(buff)
        return dr

    def __extract_btc(self, body, node_a, node_c):
        etl = CommonRegex(body)
        btcs = set(etl.btc_addresses)
        if len(btcs) > 0:
            for btc in btcs:
                node_b = graph.Node(eid=btc, label=btc, custom_property='btc')
                self.stream.add_node(node_a, node_b)
                self.stream.add_node(node_b, node_c)
                edge_ab = graph.Edge(source=node_a, target=node_b, directed=True)
                edge_bc = graph.Edge(source=node_b, target=node_c, directed=True)
                edge_ac = graph.Edge(source=node_a, target=node_c, directed=True)

                self.stream.add_edge(edge_ab)
                self.stream.add_edge(edge_bc)
                self.stream.add_edge(edge_ac)
                self.stream.commit()

    def __parser_row(self, data):
        for row in data:

            actorFrom = self.__parser_actor(row['from'])
            actorTo = self.__parser_actor(row['to'])
            # node_a = graph.Node(eid=row['from'], label=actorFrom['nameActor'], custom_property='actor')
            # node_c = graph.Node(eid=row['to'], label=actorTo['nameActor'], custom_property='actor')
            node_a = graph.Node(eid=actorFrom['nameActor'], label=actorFrom['nameActor'], custom_property='actor')
            node_c = graph.Node(eid=actorTo['nameActor'], label=actorTo['nameActor'], custom_property='actor')
            self.stream.add_node(node_a, node_c)
            edge_ac = graph.Edge(source=node_a, target=node_c, directed=True)
            self.stream.add_edge(edge_ac)
            # streamG.commit()
            self.stream.commit()
            self.__extract_btc(body=row['body'], node_a=node_a, node_c=node_c)

    def run(self):
        for url in self.urls:
            data = self.__get_url(url=url)
            self.__parser_row(data=data)


contiLeaksJabber().run()
