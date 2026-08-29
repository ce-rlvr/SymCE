import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: ~ is a relation on G defined by x ~ y if there exists g in G such that gxg^{-1} = y
    # This hypothesis requires that G is a valid collection of elements where the operation is well-defined.
    try:
        G = list(witness)
        if len(G) == 0:
            h1 = False
        else:
            h1 = True
            # Verify that g * x * g^-1 is well-defined for all g, x in G
            for g in G:
                for x in G:
                    _ = g * x * g**-1
    except Exception:
        h1 = False

    # ¬Q: The relation ~ is NOT an equivalence relation on G
    try:
        if not h1:
            neg_q = False
        else:
            n = len(G)
            rel = [[False] * n for _ in range(n)]
            
            # Build the relation matrix
            for i in range(n):
                for j in range(n):
                    for g in G:
                        if g * G[i] * g**-1 == G[j]:
                            rel[i][j] = True
                            break
            
            is_equiv = True
            
            # Check Reflexivity
            for i in range(n):
                if not rel[i][i]:
                    is_equiv = False
                    break
            
            # Check Symmetry
            if is_equiv:
                for i in range(n):
                    for j in range(n):
                        if rel[i][j] and not rel[j][i]:
                            is_equiv = False
                            break
                            
            # Check Transitivity
            if is_equiv:
                for i in range(n):
                    for j in range(n):
                        for k in range(n):
                            if rel[i][j] and rel[j][k] and not rel[i][k]:
                                is_equiv = False
                                break
                                
            neg_q = not is_equiv
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: ~ is a relation on G defined by x ~ y if there exists g in G such that gxg^{-1} = y",
    "¬Q: The relation ~ is not an equivalence relation on G"
]

N_HYP = 1
NEG_Q_INDEX = 1