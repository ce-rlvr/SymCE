import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy import isprime

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

def is_normal_subgroup(H, G):
    if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    
    try:
        # Check if H is a subgroup of G
        for gen in H.generators:
            if not G.contains(gen):
                return False
    except Exception:
        return False
        
    try:
        # Check for normality: g * h * g^-1 in H for all generators g of G and h of H
        for g in G.generators:
            for h in H.generators:
                if not H.contains(g * h * ~g):
                    return False
    except Exception:
        return False
        
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            H = witness.get('H')
        else:
            G, p, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = isprime(p)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not is_normal_subgroup(H, G)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2