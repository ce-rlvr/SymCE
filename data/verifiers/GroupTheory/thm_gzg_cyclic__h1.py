import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup for witness expressions
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

def is_quotient_cyclic(G):
    """
    Checks if the quotient group G/Z(G) is cyclic.
    """
    try:
        Z = G.center()
        q_order = G.order() // Z.order()
        
        if q_order == 1:
            return True
            
        factors = list(factorint(q_order).keys())
        
        # Check if there is an element g in G such that gZ generates G/Z.
        # gZ generates G/Z iff (gZ)^(q_order/p) != Z for all prime factors p of q_order.
        for g in G.elements:
            is_gen = True
            for p in factors:
                if (g**(q_order // p)) in Z:
                    is_gen = False
                    break
            if is_gen:
                return True
                
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    # H_1: Z(G) is the center of G
    # We verify this by checking if the witness is a valid group object with a center.
    try:
        Z = witness.center()
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: The quotient group G/Z(G) is cyclic
    try:
        h2_ok = is_quotient_cyclic(witness)
    except Exception:
        h2_ok = False

    # ¬Q: G is not an abelian group
    try:
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: The quotient group G/Z(G) is cyclic",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2