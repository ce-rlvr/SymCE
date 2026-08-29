import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo
from sympy.ntheory import factorint

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    # H_1: For every prime p dividing the order of G, the Sylow p-subgroups of G are cyclic
    h1 = False
    try:
        # Handle both method and property for order
        if callable(witness.order):
            order = witness.order()
        else:
            order = witness.order
            
        # If the group is infinite, there are no primes dividing its order,
        # making the condition vacuously true.
        if order == oo or order == 0:
            h1 = True
        else:
            primes = factorint(order).keys()
            h1 = True
            for p in primes:
                if p < 2:
                    continue
                sylow = witness.sylow_subgroup(p)
                
                # Handle both method and property for is_cyclic
                if callable(sylow.is_cyclic):
                    cyclic = sylow.is_cyclic()
                else:
                    cyclic = sylow.is_cyclic
                    
                if not cyclic:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # ¬Q: G is not a solvable group
    neg_q = False
    try:
        # Handle both method and property for is_solvable
        if callable(witness.is_solvable):
            solvable = witness.is_solvable()
        else:
            solvable = witness.is_solvable
            
        neg_q = not solvable
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: For every prime p dividing the order of G, the Sylow p-subgroups of G are cyclic",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1