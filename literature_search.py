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
    print("Start downloading the abstracts")
    for eid in search_result.EIDS:
        article = scopus.ScopusAbstract(eid, view="FULL")
        articles[eid] = article
        #time.sleep(200)  # six per second allowed, let's do five
        print(".", end="")
    print("\nAll downloaded")

    connections = []
    for article in articles.values():
        if not article.references:
            print("No references found for '{eid}'".format(eid=article.eid))
            continue
        for reference in article.references:
            print(".", end="")
            if reference in articles:
                connections.append((article, articles[reference]))

    return connections


def plot_scopus_network(connections):
    G = nx.DiGraph()
    G.add_edges_from([(article.title, reference.title) 
                     for (article, reference) in connections])
    nx.draw_networkx_nodes(G, nx.shell_layout(G))
    plt.show()


def main():
    query = "TITLE-ABS-KEY ( situation  AND awareness  AND vessel AND maritime )"
    connections = obtain_network_from_scopus(query)
    plot_scopus_network(connections)


if __name__ == "__main__":
    main()
