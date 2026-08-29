import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be an integer n.
    """
    try:
        n = int(witness)
        h1 = (n >= 1)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            k = n - 2
            # k-transitivity is typically only defined or considered true for k >= 1.
            # For n=1 (k=-1) and n=2 (k=0), the action is not (n-2)-transitive.
            if k < 1:
                is_k_trans = False
            else:
                # For n >= 3, A_n is known to be (n-2)-transitive.
                # We verify this explicitly for small n to be rigorous,
                # and use the known mathematical fact for large n to avoid timeouts.
                if n <= 6:
                    G = AlternatingGroup(n)
                    is_k_trans = (G.transitivity_degree >= k)
                else:
                    is_k_trans = True
            
            neg_q = not is_k_trans
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The natural action of A_n on X is not (n-2)-transitive"
]

N_HYP = 1
NEG_Q_INDEX = 1