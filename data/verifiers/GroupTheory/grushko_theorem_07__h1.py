import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import itertools
import functools
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        # If the witness is provided as a tuple of 3 numbers: (rank_G, rank_H, rank_G_star_H)
        if isinstance(witness, tuple) and len(witness) == 3:
            if all(isinstance(x, (int, float)) for x in witness):
                rank_G, rank_H, rank_G_star_H = witness
                h1 = True
                h2 = True
                h3 = True
                neg_q = rank_G_star_H != rank_G + rank_H
                return [h1, h2, h3, neg_q]
        
        # If the witness is provided as a dictionary
        if isinstance(witness, dict):
            h1 = bool(witness.get('H_is_finitely_generated', True))
            h2 = bool(witness.get('is_free_product', True))
            h3 = bool(witness.get('rank_definition', True))
            rank_G = witness.get('rank_G', 0)
            rank_H = witness.get('rank_H', 0)
            rank_G_star_H = witness.get('rank_G_star_H', 0)
            neg_q = rank_G_star_H != rank_G + rank_H
            return [h1, h2, h3, neg_q]
            
        # If the witness is provided as an object with attributes
        h1 = bool(getattr(witness, 'H_is_finitely_generated', True))
        h2 = bool(getattr(witness, 'is_free_product', True))
        h3 = bool(getattr(witness, 'rank_definition', True))
        rank_G = getattr(witness, 'rank_G', 0)
        rank_H = getattr(witness, 'rank_H', 0)
        rank_G_star_H = getattr(witness, 'rank_G_star_H', 0)
        neg_q = rank_G_star_H != rank_G + rank_H
        return [h1, h2, h3, neg_q]
        
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: H is a finitely generated group",
    "H_2: G * H is the free product of G and H",
    "H_3: rank(K) denotes the minimum number of generators of a group K",
    "¬Q: rank(G * H) != rank(G) + rank(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3