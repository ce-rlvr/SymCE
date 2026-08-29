import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
        else:
            G, H, f = witness
    except Exception:
        return [False, False, False]

    # H_1: f: G -> H is a surjective group homomorphism
    try:
        if hasattr(f, 'domain') and hasattr(f, 'codomain') and hasattr(f, 'is_surjective'):
            h1_ok = bool(f.domain == G and f.codomain == H and f.is_surjective())
        else:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            
            if isinstance(f, dict):
                func = lambda x: f.get(x, None)
                h1_ok = all(x in f for x in G_elements)
            elif isinstance(f, (list, tuple)) and all(isinstance(item, (list, tuple)) and len(item) == 2 for item in f):
                f_dict = dict(f)
                func = lambda x: f_dict.get(x, None)
                h1_ok = all(x in f_dict for x in G_elements)
            elif callable(f):
                func = f
                h1_ok = True
            else:
                h1_ok = False
                
            if h1_ok:
                image = set()
                H_elements_set = set(H_elements)
                for x in G_elements:
                    fx = func(x)
                    if fx not in H_elements_set:
                        h1_ok = False
                        break
                    image.add(fx)
                
                if h1_ok and image != H_elements_set:
                    h1_ok = False
                    
                if h1_ok:
                    for x in G_elements:
                        for y in G_elements:
                            if func(x * y) != func(x) * func(y):
                                h1_ok = False
                                break
                        if not h1_ok:
                            break
    except Exception:
        h1_ok = False

    # H_2: G is a solvable group
    try:
        h2_ok = bool(G.is_solvable)
    except Exception:
        h2_ok = False

    # neg_Q: H is NOT a solvable group
    try:
        neg_q = not bool(H.is_solvable)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to H",
    "H_2: G is a solvable group",
    "¬Q: H is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2