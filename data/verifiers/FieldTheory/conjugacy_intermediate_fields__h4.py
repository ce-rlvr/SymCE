import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

def get_attr_or_key(obj, name):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)

def is_subgroup(H, G):
    if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
        return False
    try:
        return all(g in G for g in H.generators)
    except Exception:
        return False

def are_conjugate_subgroups(G, A, B):
    try:
        if A.order() != B.order():
            return False
        gens_A = A.generators
        elements = G.elements if hasattr(G, 'elements') else list(G.generate())
        for g in elements:
            # Check if g * A * g^-1 is contained in B
            if all((g * gen * ~g) in B for gen in gens_A):
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the Galois group G, and subgroups M1, M2, H1, H2.
    By the Fundamental Theorem of Galois Theory, intermediate fields correspond to subgroups.
    """
    G = get_attr_or_key(witness, 'G')
    M1 = get_attr_or_key(witness, 'M1')
    M2 = get_attr_or_key(witness, 'M2')
    H1 = get_attr_or_key(witness, 'H1')
    H2 = get_attr_or_key(witness, 'H2')
    
    # H_1: L/K is a finite Galois extension (represented by a finite permutation group)
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: G is the Galois group of L/K
    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: M1 and M2 are intermediate fields between K and L (represented by subgroups of G)
    try:
        h3 = is_subgroup(M1, G) and is_subgroup(M2, G)
    except Exception:
        h3 = False

    # ¬Q: M1 and M2 are conjugate iff H1 and H2 are conjugate is FALSE
    try:
        if not (is_subgroup(H1, G) and is_subgroup(H2, G)):
            neg_q = False
        else:
            m_conj = are_conjugate_subgroups(G, M1, M2)
            h_conj = are_conjugate_subgroups(G, H1, H2)
            # The conclusion is the biconditional (m_conj == h_conj).
            # The negated conclusion is that the biconditional fails (m_conj != h_conj).
            neg_q = (m_conj != h_conj)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: G is the Galois group of L/K",
    "H_3: M1 and M2 are intermediate fields between K and L",
    "¬Q: M1 and M2 are conjugate iff H1 and H2 are conjugate is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3