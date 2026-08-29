import sympy
from sympy.combinatorics import DihedralGroup, PermutationGroup, Permutation
from sympy.combinatorics.named_groups import CyclicGroup

# Top-level setup for standard groups
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4) # V4 is often a subgroup, but we bind standard names
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: D_2n is the dihedral group of order 2n",
    "H_2: phi is the homomorphism mapping the non-identity element of Z_2 to the inversion automorphism of Z_n",
    "¬Q: D_2n is not isomorphic to the external semidirect product Z_n \\rtimes_\\phi Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be an integer n.
    The dropped hypothesis from the true theorem is n >= 3.
    For n = 1 and n = 2, the standard geometric definition of the dihedral group 
    (symmetries of a regular n-gon) breaks down, making the isomorphism to the 
    semidirect product fail or become degenerate in strict formalizations.
    """
    n = witness
    
    # H_1: D_2n is the dihedral group of order 2n
    # This conceptually requires n to be a valid parameter for the group's existence.
    try:
        h1_ok = isinstance(n, int) and n >= 1
    except Exception:
        h1_ok = False
        
    # H_2: phi is the homomorphism mapping the non-identity element of Z_2 to the inversion automorphism of Z_n
    # This is a definitional setup that is valid for any positive integer n.
    try:
        h2_ok = isinstance(n, int) and n >= 1
    except Exception:
        h2_ok = False
        
    # ¬Q: D_2n is not isomorphic to the external semidirect product Z_n \rtimes_\phi Z_2
    # The conclusion fails for n < 3 because a regular 1-gon and 2-gon do not exist,
    # meaning the geometric dihedral group D_2n is undefined or degenerate, 
    # breaking the standard isomorphism theorem which assumes n >= 3.
    try:
        if not (isinstance(n, int) and n >= 1):
            neg_q_ok = False
        else:
            neg_q_ok = bool(n < 3)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]