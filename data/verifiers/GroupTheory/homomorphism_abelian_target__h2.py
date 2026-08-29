import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools

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

def get_elements(group):
    if hasattr(group, 'elements'):
        elts = group.elements
        if callable(elts):
            return list(elts())
        return list(elts)
    elif hasattr(group, 'generate'):
        return list(group.generate())
    else:
        return list(group)

def conditions(witness):
    G = None
    A = None
    mapping = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, A, m = witness
            if isinstance(m, dict):
                mapping = m
            elif callable(m):
                mapping = {g: m(g) for g in get_elements(G)}
        elif hasattr(witness, 'domain') and hasattr(witness, 'codomain'):
            G = witness.domain
            A = witness.codomain
            mapping = {g: witness(g) for g in get_elements(G)}
    except Exception:
        pass

    h1 = False
    try:
        if G is not None and A is not None:
            G_elts = get_elements(G)
            A_elts = get_elements(A)
            if len(G_elts) > 0 and len(A_elts) > 0:
                if hasattr(G, 'identity') and hasattr(A, 'identity'):
                    h1 = True
    except Exception:
        h1 = False

    h2 = False
    try:
        if h1 and mapping is not None:
            G_elements = get_elements(G)
            A_elements = get_elements(A)
            
            if set(mapping.keys()) == set(G_elements):
                if all(v in A_elements for v in mapping.values()):
                    is_hom = True
                    for x in G_elements:
                        for y in G_elements:
                            if mapping[x * y] != mapping[x] * mapping[y]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    h2 = is_hom
    except Exception:
        h2 = False

    neg_q = False
    try:
        if h1 and mapping is not None:
            G_elements = get_elements(G)
            A_id = A.identity
            for x in G_elements:
                for y in G_elements:
                    commutator = x * y * (x**-1) * (y**-1)
                    if mapping[commutator] != A_id:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: f: G -> A is a group homomorphism",
    "¬Q: The commutator subgroup of G is not contained in the kernel of f"
]

N_HYP = 2
NEG_Q_INDEX = 2