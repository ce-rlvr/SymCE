import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    G = None
    H = None
    f = None
    try:
        if hasattr(witness, 'domain') and hasattr(witness, 'codomain'):
            G = witness.domain
            H = witness.codomain
            f = witness
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, H, f = witness
    except Exception:
        pass

    try:
        if G is None or H is None:
            h1 = False
        else:
            id_G = G.identity
            id_H = H.identity
            _ = list(G.elements)
            _ = list(H.elements)
            h1 = True
    except Exception:
        h1 = False

    try:
        if G is None or H is None or f is None:
            h2 = False
        else:
            h2 = True
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            
            for g in G_elements:
                val = f[g] if isinstance(f, dict) else f(g)
                if val not in H_elements:
                    h2 = False
                    break
                    
            if h2:
                for g1 in G_elements:
                    for g2 in G_elements:
                        val1 = f[g1] if isinstance(f, dict) else f(g1)
                        val2 = f[g2] if isinstance(f, dict) else f(g2)
                        val12 = f[g1 * g2] if isinstance(f, dict) else f(g1 * g2)
                        if val12 != val1 * val2:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    try:
        if H is None:
            h3 = False
        else:
            h3 = len(list(H.elements)) > 0
    except Exception:
        h3 = False

    try:
        if G is None or H is None or f is None:
            neg_q = False
        else:
            neg_q = False
            id_H = H.identity
            for g in list(G.elements):
                val = f[g] if isinstance(f, dict) else f(g)
                if val != id_H:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G \\to H is a group homomorphism",
    "H_3: H is a finite group",
    "¬Q: The image of f is not the trivial subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3