import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard algebra objects for Group Theory
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that if G is a nilpotent group of class c >= 1, 
    then Inn(G) is a nilpotent group of class c-1.
    
    The dropped hypothesis from the true theorem is that c > 1 (or G is non-abelian).
    For c = 1 (abelian groups), Inn(G) is the trivial group. In strict group theory 
    terminology, a "nilpotent group of class k" requires k >= 1. Thus, the trivial 
    group does not have class 0, making the conclusion false for c = 1.
    """
    try:
        # Witness can be a group G, or a tuple (G, c)
        if isinstance(witness, tuple):
            G, c = witness
        else:
            G = witness
            c = G.nilpotency_class
    except Exception:
        return [False, False, False]
        
    try:
        actual_c = G.nilpotency_class
        # H_1: The nilpotency class of G is c, where c >= 1
        H1 = (actual_c == c and c is not None and c >= 1)
    except Exception:
        H1 = False

    # H_2: Inn(G) is the group of inner automorphisms of G (definitional)
    H2 = True

    try:
        if H1:
            # Conclusion: Inn(G) is a nilpotent group of class c-1
            # Fails for c = 1 because class 0 is not a valid nilpotency class.
            Q = (c - 1 >= 1)
            neg_Q = not Q
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: The nilpotency class of G is c, where c >= 1",
    "H_2: Inn(G) is the group of inner automorphisms of G",
    "¬Q: Inn(G) is not a nilpotent group of class c-1"
]

N_HYP = 2
NEG_Q_INDEX = 2