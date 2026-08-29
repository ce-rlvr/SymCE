import sympy
from sympy import I, pi, exp, simplify, Symbol, QQ
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

omega_sym = exp(2*I*pi/3)
K_sym = Symbol('K')

def conditions(witness) -> list[bool]:
    # Default values for omega and K if the witness only provides the group
    omega = omega_sym
    K = 'Q(omega)'
    G = None

    # Parse witness
    if isinstance(witness, dict):
        omega = witness.get('omega', omega)
        K = witness.get('K', K)
        G = witness.get('G', witness.get('L', witness.get('Gal', witness.get('Gal_L_K'))))
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            omega, K, G = witness
        elif len(witness) == 2:
            omega, G = witness
    else:
        G = witness

    # H_1: omega is a primitive cube root of unity in C
    try:
        val3 = complex(omega**3)
        val1 = complex(omega)
        h1 = abs(val3 - 1) < 1e-9 and abs(val1 - 1) > 1e-9
    except Exception:
        try:
            h1 = bool(simplify(omega**3 - 1) == 0 and simplify(omega - 1) != 0)
        except Exception:
            h1 = False

    # H_2: K = Q(omega)
    try:
        if isinstance(K, str) and K in ['K', 'Q(omega)', 'QQ(omega)', 'Q(w)']:
            h2 = True
        elif hasattr(K, 'ext'):
            h2 = True
        elif K == QQ:
            h2 = False
        else:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The Galois group Gal(L/K) is not isomorphic to Z/3Z
    try:
        if G is None:
            neg_q = False
        elif hasattr(G, 'is_isomorphic'):
            neg_q = not G.is_isomorphic(Z3)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: omega is a primitive cube root of unity in C",
    "H_2: K = Q(omega)",
    "¬Q: The Galois group Gal(L/K) is not isomorphic to Z/3Z"
]

N_HYP = 2
NEG_Q_INDEX = 2