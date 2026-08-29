import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import Integer

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

def conditions(witness) -> list[bool]:
    # witness is expected to be a tuple (G, B)
    # where G is a PermutationGroup acting on X = {0, 1, ..., G.degree - 1}
    # and B is a subset of X.
    
    try:
        G, B = witness
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(B, (set, list, tuple)):
            # Check if G acts transitively
            transitive = G.is_transitive() if callable(G.is_transitive) else G.is_transitive
            if transitive:
                # Check if B is a subset of the domain X
                if all(isinstance(b, (int, Integer)) and 0 <= b < G.degree for b in B):
                    h1 = True
    except Exception:
        h1 = False

    try:
        G, B = witness
        deg = G.degree
        b_len = len(set(B))
        
        if b_len == 0:
            neg_q = (deg != 0)
        else:
            neg_q = (deg % b_len != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group acting transitively on a finite set X (and B is a subset of X)",
    "¬Q: The cardinality |B| does not divide the cardinality |X|"
]

N_HYP = 1
NEG_Q_INDEX = 1