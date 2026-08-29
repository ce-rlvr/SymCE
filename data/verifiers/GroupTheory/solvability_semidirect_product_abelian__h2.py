import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If A is a finite abelian group and G is a semidirect product of A and B, then G is solvable."
    
    The witness can be a tuple (A, B, G) of SymPy PermutationGroups, 
    or just a single PermutationGroup G (in which case we use A=trivial, B=G).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            A, B, G = witness
            if isinstance(A, list):
                A = PermutationGroup(A)
            if isinstance(B, list):
                B = PermutationGroup(B)
        else:
            G = witness
            # If only G is provided, we construct A as the trivial subgroup of G 
            # and B as G itself. This satisfies G = A rtimes B.
            id_perm = Permutation([i for i in range(G.degree)])
            A = PermutationGroup([id_perm])
            B = G
    except Exception:
        return [False, False, False]

    # H_1: A is a finite abelian group
    try:
        h1_ok = bool(A.is_abelian)
    except Exception:
        h1_ok = False

    # H_2: G is a semidirect product of A and B
    try:
        # Check if A and B are subgroups of G
        A_in_G = all(g in G for g in A.generators)
        B_in_G = all(g in G for g in B.generators)
        
        # Check if A is a normal subgroup of G
        A_normal = A_in_G and all((~g * h * g) in A for h in A.generators for g in G.generators)
        
        # Check if G is the internal semidirect product of A and B
        # For finite subgroups with A normal, G = A rtimes B iff |G| = |A| * |B|
        order_ok = (G.order() == A.order() * B.order())
        
        h2_ok = bool(A_in_G and B_in_G and A_normal and order_ok)
    except Exception:
        h2_ok = False

    # neg_Q: G is NOT a solvable group
    try:
        neg_q_ok = not bool(G.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a finite abelian group",
    "H_2: G is a semidirect product of A and B",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2