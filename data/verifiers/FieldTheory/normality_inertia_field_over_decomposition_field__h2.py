import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings for witness expressions
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
    """
    Given a witness tuple (G, D, I) representing the Galois group, decomposition group, 
    and inertia group respectively, checks if it is a valid counterexample.
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, D, I = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: L/K is a finite Galois extension (G is a finite group)
    try:
        h1_ok = bool(isinstance(G, PermutationGroup))
    except Exception:
        h1_ok = False
        
    # H_2: D is the decomposition group (D is a subgroup of G)
    try:
        h2_ok = bool(D.is_subgroup(G))
    except Exception:
        h2_ok = False
        
    # H_3: I is the inertia group (I is a subgroup of D)
    try:
        h3_ok = bool(I.is_subgroup(D))
    except Exception:
        h3_ok = False
        
    # ¬Q: The inertia field L^I is not a finite normal extension of the decomposition field L^D
    # By Galois correspondence, this means I is NOT a normal subgroup of D.
    try:
        neg_q_ok = bool(not D.is_normal(I))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: D is the decomposition group of w over v",
    "H_3: I is the inertia group of w over v",
    "¬Q: The inertia field L^I is not a finite normal extension of the decomposition field L^D"
]

N_HYP = 3
NEG_Q_INDEX = 3