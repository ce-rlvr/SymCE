import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer, Symbol
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
trivial = PermutationGroup([Permutation(0)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)

def get_min_relators(G, d):
    """
    Computes the minimal number of relators for a presentation of G with d generators.
    Returns None if it cannot be easily determined.
    """
    try:
        order = G.order()
    except Exception:
        return None

    if order == 1:
        return d if d >= 0 else None
    
    factors = sympy.factorint(order)
    if len(factors) != 1:
        return None
    p = list(factors.keys())[0]
    
    if order == p:
        return d if d >= 1 else None
        
    if order == p**2:
        is_cyclic = None
        if hasattr(G, 'is_cyclic'):
            try:
                is_cyclic = G.is_cyclic
            except Exception:
                pass
        if is_cyclic is None and hasattr(G, 'elements'):
            try:
                is_cyclic = any(g.order() == p**2 for g in G.elements)
            except Exception:
                pass
        if is_cyclic is None:
            return None
            
        if is_cyclic:
            return d if d >= 1 else None
        else:
            return d + 1 if d >= 2 else None
            
    return None

def parse_witness(witness):
    """
    Parses the witness into (G, d, r).
    Supports multiple convenient formats for the counterexample.
    """
    if isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            return witness[0], witness[1], witness[2]
        elif len(witness) == 4:
            return witness[0], witness[2], witness[3]
        elif len(witness) == 2:
            if isinstance(witness[0], (int, float)):
                return trivial, int(witness[0]), int(witness[1])
            else:
                G = witness[0]
                d = witness[1]
                r = get_min_relators(G, d)
                return G, d, r
    elif isinstance(witness, (int, float)):
        d = int(witness)
        r = get_min_relators(trivial, d)
        return trivial, d, r
    elif hasattr(witness, 'generators') and hasattr(witness, 'relators'):
        G = witness
        d = len(G.generators)
        r = len(G.relators)
        return G, d, r
    return witness, None, None

def conditions(witness) -> list[bool]:
    G, d, r = parse_witness(witness)
    
    # H_1: G is a finite p-group
    h1 = False
    try:
        if G is not None:
            order = G.order()
            if order == 1:
                h1 = True
            elif order != sympy.oo:
                factors = sympy.factorint(order)
                if len(factors) == 1:
                    h1 = True
    except Exception:
        pass

    # H_2: r is the minimal number of relators in a presentation of G with d generators
    h2 = False
    try:
        if G is not None and d is not None and r is not None:
            expected_r = get_min_relators(G, d)
            if expected_r is not None and r == expected_r:
                h2 = True
    except Exception:
        pass

    # ¬Q: r <= d^2 / 4 (The strict inequality r > d^2 / 4 fails)
    neg_q = False
    try:
        if d is not None and r is not None:
            if r <= (d**2) / 4.0:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: r is the minimal number of relators in a presentation of G with d generators",
    "¬Q: r <= d^2 / 4"
]

N_HYP = 2
NEG_Q_INDEX = 2