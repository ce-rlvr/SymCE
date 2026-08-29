import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = AbelianGroup(2, 2)
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, phi) or (G, Z, phi) where:
      - G is a group
      - Z is the center of G (optional in witness, computed if absent)
      - phi is a mapping (callable, dict, or list of pairs) from G to G
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, phi = witness
                Z = G.center()
                h2 = True
            elif len(witness) == 3:
                G, Z, phi = witness
                try:
                    if hasattr(Z, 'elements'):
                        Z_set = set(Z.elements)
                    else:
                        Z_set = set(Z)
                    h2 = (Z_set == set(G.center().elements))
                except Exception:
                    h2 = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # neg_Q: phi(Z(G)) != Z(G)
    try:
        if hasattr(Z, 'elements'):
            Z_elems = set(Z.elements)
        else:
            Z_elems = set(Z)
            
        if callable(phi):
            phi_Z = set(phi(g) for g in Z_elems)
        elif isinstance(phi, dict):
            phi_Z = set(phi[g] for g in Z_elems)
        elif isinstance(phi, list) and all(isinstance(item, tuple) and len(item) == 2 for item in phi):
            phi_dict = dict(phi)
            phi_Z = set(phi_dict[g] for g in Z_elems)
        else:
            phi_Z = None
            
        if phi_Z is not None:
            neg_q = (phi_Z != Z_elems)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: phi(Z(G)) is not equal to Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2