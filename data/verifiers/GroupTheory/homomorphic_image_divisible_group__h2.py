import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    h1_ok = False
    neg_q_ok = False
    
    try:
        from sympy.combinatorics.homomorphisms import GroupHomomorphism, homomorphism
    except ImportError:
        GroupHomomorphism = type(None)
        homomorphism = None

    H = None
    try:
        if isinstance(witness, GroupHomomorphism):
            hom = witness
            H = hom.codomain
            h1_ok = (hom.image().order() == H.order())
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, H_candidate, images = witness
                if isinstance(images, dict):
                    hom = homomorphism(G, H_candidate, list(images.keys()), list(images.values()))
                else:
                    hom = homomorphism(G, H_candidate, G.generators, images)
            elif len(witness) == 4:
                G, H_candidate, gens, images = witness
                hom = homomorphism(G, H_candidate, gens, images)
            else:
                hom = None
            
            if hom is not None:
                H = H_candidate
                h1_ok = (hom.image().order() == H.order())
    except Exception:
        h1_ok = False

    try:
        if H is not None:
            # A finite group is divisible if and only if it is the trivial group (order 1).
            # This is because if |H| = m > 1, then for any x in H, x^m = e.
            # Thus, the equation x^m = h has no solution for h != e, meaning H is not divisible.
            is_divisible = (H.order() == 1)
            neg_q_ok = not is_divisible
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism",
    "¬Q: H is not a divisible group"
]

N_HYP = 1
NEG_Q_INDEX = 1