#!/usr/bin/env python3

import time

import networkx as nx
import matplotlib.pyplot as plt
import scopus


def obtain_network_from_scopus(query):
    """
    Obtains a reference network from scopus for a given query
    """
    articles = {}
    search_result = scopus.ScopusSearch(query)
    for eid in search_result.EIDS:
        article = scopus.ScopusAbstract(view="FULL")
        articles[eid] = article
        time.sleep(200)  # six per second allowed, let's do five

    connections = []
    for article in articles.values():
        for reference in article.references:
            if reference in articles:
                connections.append((article, articles[reference]))

    return connections


def plot_scopus_network(connections):
    G = nx.DiGraph()
    G.add_edges_from([(article.title, reference.title) 
                     for (article, reference) in connections])
    nx.draw_networkx_nodes(G)
    plt.show()
