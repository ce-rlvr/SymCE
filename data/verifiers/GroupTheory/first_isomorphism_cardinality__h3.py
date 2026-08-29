import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, phi = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            G_elements = list(G.generate())
            H_elements = list(H.generate())
            H_id = H.identity
            
            ker_size = 0
            im_set = set()
            
            if not callable(phi) and not isinstance(phi, dict):
                phi = dict(phi)
                
            for g in G_elements:
                if callable(phi):
                    val = phi(g)
                else:
                    if g not in phi:
                        raise ValueError("phi is not total")
                    val = phi[g]
                
                if val not in H_elements:
                    raise ValueError("phi does not map into H")
                
                if val == H_id:
                    ker_size += 1
                im_set.add(val)
                
            im_size = len(im_set)
            neg_q = (int(G.order()) != ker_size * im_size)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a finite group",
    "¬Q: The order of G does not equal the order of ker(phi) multiplied by the order of im(phi)"
]

N_HYP = 2
NEG_Q_INDEX = 2