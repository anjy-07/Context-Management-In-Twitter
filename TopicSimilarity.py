# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 21:31:21 2018

@author: shivangi
"""

from __future__ import division
from nltk.corpus import wordnet as wn
import math
import sys

# Parameters to the algorithm. Currently set to values that was reported
# in the paper to produce "best" results.
ALPHA = 0.2
BETA = 0.45

######################### word similarity ##########################

def get_best_synset_pair(word_1, word_2):
    """ 
    Choose the pair with highest path similarity among all pairs. 
    Mimics pattern-seeking behavior of humans.
    """
    max_sim = -1.0
    synsets_1 = wn.synsets(word_1)
    synsets_2 = wn.synsets(word_2)
    if len(synsets_1) == 0 or len(synsets_2) == 0:
        return None, None
    else:
        max_sim = -1.0
        best_pair = None, None
        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
               sim = wn.path_similarity(synset_1, synset_2)
               try:
                   if sim > max_sim:
                       max_sim = sim
                       best_pair = synset_1, synset_2
               except:
                   continue
        return best_pair

def length_dist(synset_1, synset_2):
    """
    Return a measure of the length of the shortest path in the semantic 
    ontology (Wordnet in our case as well as the paper's) between two 
    synsets.
    """
    l_dist = sys.maxsize
    if synset_1 is None or synset_2 is None: 
        return 0.0
    if synset_1 == synset_2:
        # if synset_1 and synset_2 are the same synset return 0
        l_dist = 0.0
    else:
        wset_1 = set([str(x.name()) for x in synset_1.lemmas()])        
        wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
        if len(wset_1.intersection(wset_2)) > 0:
            # if synset_1 != synset_2 but there is word overlap, return 1.0
            l_dist = 1.0
        else:
            # just compute the shortest path between the two
            l_dist = synset_1.shortest_path_distance(synset_2)
            if l_dist is None:
                l_dist = 0.0
    # normalize path length to the range [0,1]
    return math.exp(-ALPHA * l_dist)

def hierarchy_dist(synset_1, synset_2):
    """
    Return a measure of depth in the ontology to model the fact that 
    nodes closer to the root are broader and have less semantic similarity
    than nodes further away from the root.
    """
    h_dist = sys.maxsize
    if synset_1 is None or synset_2 is None: 
        return h_dist
    if synset_1 == synset_2:
        # return the depth of one of synset_1 or synset_2
        h_dist = max([x[1] for x in synset_1.hypernym_distances()])
    else:
        # find the max depth of least common subsumer
        hypernyms_1 = {x[0]:x[1] for x in synset_1.hypernym_distances()}
        hypernyms_2 = {x[0]:x[1] for x in synset_2.hypernym_distances()}
        lcs_candidates = set(hypernyms_1.keys()).intersection(
            set(hypernyms_2.keys()))
        if len(lcs_candidates) > 0:
            lcs_dists = []
            for lcs_candidate in lcs_candidates:
                lcs_d1 = 0
                if lcs_candidate in hypernyms_1:
                    lcs_d1 = hypernyms_1[lcs_candidate]
                lcs_d2 = 0
                if lcs_candidate in hypernyms_2:
                    lcs_d2 = hypernyms_2[lcs_candidate]
                lcs_dists.append(max([lcs_d1, lcs_d2]))
            h_dist = max(lcs_dists)
        else:
            h_dist = 0
    return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) / 
        (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))
    
def word_similarity(word_1, word_2):
    synset_pair = get_best_synset_pair(word_1, word_2)
    return (length_dist(synset_pair[0], synset_pair[1]) * 
        hierarchy_dist(synset_pair[0], synset_pair[1]))
        
######################### main / test ##########################

# the results of the algorithm are largely dependent on the results of 
# the word similarities, so we should test this first...
word_pairs = [
  ["asylum", "fruit", 0.21],
  ["autograph", "shore", 0.29],
  ["autograph", "signature", 0.55],
  ["automobile", "car", 0.64],
  ["bird", "woodland", 0.33],
  ["boy", "rooster", 0.53],
  ["boy", "lad", 0.66],
  ["boy", "sage", 0.51],
  ["cemetery", "graveyard", 0.73],
  ["coast", "forest", 0.36],
  ["coast", "shore", 0.76],
  ["cock", "rooster", 1.00],
  ["cord", "smile", 0.33],
  ["cord", "string", 0.68],
  ["cushion", "pillow", 0.66],
  ["forest", "graveyard", 0.55],
  ["forest", "woodland", 0.70],
  ["furnace", "stove", 0.72],
  ["glass", "tumbler", 0.65],
  ["grin", "smile", 0.49],
  ["gem", "jewel", 0.83],
  ["hill", "woodland", 0.59],
  ["hill", "mound", 0.74],
  ["implement", "tool", 0.75],
  ["journey", "voyage", 0.52],
  ["magician", "oracle", 0.44],
  ["magician", "wizard", 0.65],
  ["midday", "noon", 1.0],
  ["oracle", "sage", 0.43],
  ["serf", "slave", 0.39]
]
for word_pair in word_pairs:
    print("%s\t%s\t%.2f\t%.2f" % (word_pair[0], word_pair[1], word_pair[2], 
                                  word_similarity(word_pair[0], word_pair[1])))