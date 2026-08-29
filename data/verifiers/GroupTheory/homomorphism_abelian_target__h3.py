import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
        G, A, f = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H2: A is an abelian group
    try:
        h2_ok = isinstance(A, PermutationGroup) and bool(A.is_abelian)
    except Exception:
        h2_ok = False

    # neg_Q: The commutator subgroup is NOT contained in the kernel of f
    try:
        derived = G.derived_subgroup()
        
        # Find the identity element of A
        id_A = None
        try:
            for g in A.generators:
                id_A = g ** 0
                break
            if id_A is None:
                for g in A.elements:
                    if g * g == g:
                        id_A = g
                        break
        except Exception:
            pass
                    
        if id_A is None:
            neg_q_ok = False
        else:
            # Normalize f to be either a dict or callable
            if not isinstance(f, dict) and not callable(f):
                f_map = dict(f)
            else:
                f_map = f

            neg_q_ok = False
            # Check if there is any element in the derived subgroup that does not map to the identity of A
            for x in derived.elements:
                if isinstance(f_map, dict):
                    val = f_map[x]
                else:
                    val = f_map(x)
                    
                if val != id_A:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A is an abelian group",
    "not Q: The commutator subgroup is not contained in the kernel of f"
]

N_HYP = 2
NEG_Q_INDEX = 2