import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.group_constructs import DirectProduct
from sympy.matrices import eye, zeros
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

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: F is isomorphic to the direct product A \\times B",
    "¬Q: A is not the trivial group and B is not the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def extract_FAB(witness):
    if isinstance(witness, (tuple, list)) and len(witness) == 3:
        return witness[0], witness[1], witness[2]
    if hasattr(witness, 'F') and hasattr(witness, 'A') and hasattr(witness, 'B'):
        return witness.F, witness.A, witness.B
    if isinstance(witness, dict) and 'F' in witness and 'A' in witness and 'B' in witness:
        return witness['F'], witness['A'], witness['B']
    raise ValueError("Witness format not recognized")

def is_trivial(G):
    if hasattr(G, 'is_trivial'):
        val = G.is_trivial() if callable(G.is_trivial) else G.is_trivial
        if val is not None:
            return bool(val)
            
    if isinstance(G, FreeGroup):
        return len(G.generators) == 0
        
    if isinstance(G, PermutationGroup):
        try:
            return G.order() == 1
        except Exception:
            pass
            
    if isinstance(G, FpGroup):
        if len(G.generators) == 0:
            return True
            
    if hasattr(G, 'order'):
        try:
            if not isinstance(G, FpGroup):
                return G.order() == 1
        except Exception:
            pass
            
    return False

def is_free_group(G):
    if isinstance(G, FreeGroup):
        return True
    if isinstance(G, FpGroup) and len(G.relators) == 0:
        return True
    if hasattr(G, 'is_free_group'):
        val = G.is_free_group() if callable(G.is_free_group) else G.is_free_group
        if val is not None:
            return bool(val)
    if is_trivial(G):
        return True
    return False

def is_isomorphic(G, H):
    if hasattr(G, 'is_isomorphic'):
        try:
            return G.is_isomorphic(H)
        except Exception:
            pass
    if isinstance(G, FreeGroup) and isinstance(H, FreeGroup):
        return len(G.generators) == len(H.generators)
    if is_trivial(G) and is_trivial(H):
        return True
    return False

def is_isomorphic_to_direct_product(F, A, B):
    if hasattr(F, 'is_isomorphic_to_direct_product'):
        try:
            return F.is_isomorphic_to_direct_product(A, B)
        except Exception:
            pass

    if isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup):
        try:
            DP = DirectProduct(A, B)
            if hasattr(F, 'is_isomorphic'):
                return F.is_isomorphic(DP)
        except Exception:
            pass

    try:
        triv_A = is_trivial(A)
        triv_B = is_trivial(B)
        if triv_A and triv_B:
            return is_trivial(F)
        if triv_A:
            return is_isomorphic(F, B)
        if triv_B:
            return is_isomorphic(F, A)
    except Exception:
        pass

    # Mathematically, a free group is indecomposable as a direct product.
    # It cannot be isomorphic to A x B unless A or B is trivial.
    try:
        if is_free_group(F):
            return False
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    try:
        F, A, B = extract_FAB(witness)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(is_free_group(F))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_isomorphic_to_direct_product(F, A, B))
    except Exception:
        h2 = False

    try:
        neg_q = not is_trivial(A) and not is_trivial(B)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]