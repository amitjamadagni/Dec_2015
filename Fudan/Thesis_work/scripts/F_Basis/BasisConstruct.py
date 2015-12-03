from sympy.abc import *
from sage.combinat.combination import Combinations
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

class BasisSpace:

    def __init__(self, edge_labels, fusion_rules):
        self.edge_labels = edge_labels
        self.fusion_rules = fusion_rules

    # addition of trivial fusion rules
    def addition_of_fusion_rules(self):
        for edge in self.edge_labels:
            self.fusion_rules.append([(edge, i), edge])
        return self.fusion_rules

    # fusion to dictionary
    def fusion_to_dict(self):
        fusion_dict = []
        for rule in self.fusion_rules:
            fusion_dict.append((rule[0],rule[1]))
        return dict(fusion_dict)

    # first node leaf construction
    def first_node_leaves_construction(self):
        final_comb = Combinations(self.edge_labels*2, 2).list()
        for comb in Combinations(self.edge_labels*2, 2):
            if i not in comb and comb[0]!=comb[1]:
                final_comb.append([comb[1], comb[0]])
        return final_comb

    # construction of first node (this can be directly done from fusion but we could use it later in the second node construction)
    def first_node(self):
        combination_list = self.first_node_leaves_construction()
        fusion_dict = self.fusion_to_dict()
        three_leaves = []
        for combination in combination_list:
            for key, value in fusion_dict.items():
                if set(combination) == set(key) and  key.count(i) == 1:
                    three_leaves.append([(combination[0], combination[1]), value])
                if tuple(combination) == key:
                    if value.args ==  ():
                        three_leaves.append([(combination[0], combination[1]), value])
                    else:
                        division = []
                        for arg in value.args:
                            division.append([(combination[0], combination[1]), arg])
                        three_leaves.append(division)
        return three_leaves

    # second node leaves construction
    def second_node_leaves(self):
        first_node = self.first_node()
        pair = []
        #for leaf in second_node_leaf:
        for node in first_node:
            for edge in self.edge_labels:
                if type(node[0]) != list:
                    pair.append(((node), (node[1], edge)))
                else:
                    s = []
                    for l in node:
                        s.append(((l),(l[1], edge)))
                    pair.append(s)
        return pair

    # construction of second node
    def second_node(self):
        leaves_combo = self.second_node_leaves()
        fusion_dict = self.fusion_to_dict()
        node = []
        for c in leaves_combo:
            if type(c) == list:
                for l in c:
                    leaves_combo.append(l)
        for combination in leaves_combo:
            for key, value in fusion_dict.items():
                if type(combination) != list:
                    if set(list(combination[1])) == set(list(key)) and  key.count(i) == 1:
                        node.append([combination[0],(combination[1][0], combination[1][1]), value])
                    else:
                        if tuple(combination[1]) == key:
                            node.append([combination[0], (combination[1][0], combination[1][1]), value])
        return node

    # Combining all the above methods to give out the final basis construction
    def basis_construct(self):
        adding_rules = self.addition_of_fusion_rules()
        ftd = self.fusion_to_dict()
        fnlc =  self.first_node_leaves_construction()
        fn = self.first_node()
        snlc = self.second_node_leaves()
        sn = self.second_node()
        basis =  [(s[0][0], s[1], s[2]) for s in sn]
        return basis

    def basis_graph_construct(self, basis):
        G = nx.Graph()
        G.add_node(1,pos=(1,4))
        G.add_node(2,pos=(3,4))
        G.add_node(3, pos=(2,2))
        G.add_node(4, pos=(5,4))
        G.add_node(5, pos=(3,0))
        G.add_node(6, pos=(3,-2))
        G.add_edges_from([[1,3],[2,3],[3,5],[4,5], [5,6]])
        pos=nx.get_node_attributes(G,'pos')
        fig = plt.figure()
        nx.draw_networkx_nodes(G,pos)
        nx.draw_networkx_edges(G,pos)
        nx.draw_networkx_edge_labels(G,pos, {(1,3):basis[0][0], (2,3):basis[0][1], (3,5):basis[1][0], (4,5):basis[1][1], (5,6):basis[2]})
        fig.savefig("diag.png")
        return None

    def basis_transform(self, basis_dynamics):
        fusion_rules = self.addition_of_fusion_rules()
        ftd = self.fusion_to_dict()
        combination = (basis_dynamics[1][1], basis_dynamics[0][1])
        new_sum = None
        for key, value in ftd.items():
            if set(list(combination)) == set(list(key)) and  key.count(i) == 1:
                new_sum = value
                break
            elif combination == key:
                new_sum = value
                break
        return ((basis_dynamics[1][1], basis_dynamics[0][1]),(new_sum, basis_dynamics[0][0]), basis_dynamics[2])

    def basis_graph_transform_construct(self, basis):
        G = nx.Graph()
        G.add_node(1, pos=(5,4))
        G.add_node(2, pos=(3,4))
        G.add_node(3, pos=(4,2))
        G.add_node(4, pos=(1,4))
        G.add_node(5, pos=(3,0))
        G.add_node(6, pos=(3,-2))
        G.add_edges_from([[1,3],[2,3],[3,5],[4,5], [5,6]])
        pos=nx.get_node_attributes(G,'pos')
        fig = plt.figure()
        nx.draw_networkx_nodes(G,pos)
        nx.draw_networkx_edges(G,pos)
        nx.draw_networkx_edge_labels(G,pos, {(1,3):basis[0][0], (2,3):basis[0][1], (3,5):basis[1][0], (4,5):basis[1][1], (5,6):basis[2]})
        fig.savefig("diag.png")
        return None
