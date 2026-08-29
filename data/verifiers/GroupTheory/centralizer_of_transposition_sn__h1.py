import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
    try:
        n, tau = witness
    except Exception:
        return [False, False, False]
        
    # H1: S_n is the symmetric group on n letters
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False
        
    # H2: tau in S_n is a transposition
    try:
        if not h1:
            h2 = False
        else:
            if not isinstance(tau, Permutation):
                h2 = False
            else:
                sup = tau.support()
                # Check if tau is a valid element of S_n
                if (sup and max(sup) >= n) or tau.size > n:
                    h2 = False
                else:
                    # Check if tau is a transposition (exactly one cycle of length 2)
                    cycles = tau.cyclic_form
                    h2 = (len(cycles) == 1 and len(cycles[0]) == 2)
    except Exception:
        h2 = False
        
    # neg_Q: The centralizer of tau in S_n is NOT isomorphic to C_2 x S_{n-2}
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # The conclusion fails if S_{n-2} is undefined.
            # In standard group theory (and SymPy), SymmetricGroup(k) requires k >= 1.
            # For n=2, n-2 = 0, which makes S_{n-2} undefined, causing the conclusion to fail.
            if n - 2 < 1:
                neg_q = True
            else:
                # For n >= 3, the conclusion is mathematically true.
                neg_q = False
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group on n letters",
    "H_2: tau is a transposition in S_n",
    "not Q: The centralizer of tau in S_n is not isomorphic to C_2 x S_{n-2}"
]

N_HYP = 2
NEG_Q_INDEX = 2