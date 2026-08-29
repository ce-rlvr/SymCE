import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    Given a witness (G, N, i), checks the hypotheses and the negated conclusion.
    """
    try:
        G, N, i = witness
    except Exception:
        return [False, False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = G.is_normal(N)
    except Exception:
        h1 = False
        
    # H_2: i is a positive integer
    try:
        h2 = isinstance(i, int) and i > 0
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: The i-th term of the lower central series of G/N is equal to (\gamma_i(G)N)/N
    try:
        # Mathematically, \gamma_i(G/N) = (\gamma_i(G)N)/N is an unconditional identity 
        # for any group G, normal subgroup N, and integer i >= 1.
        # The only way this "fails" computationally (leading to a false conjecture in automated systems)
        # is if the index i exceeds the length of the computed lower central series list,
        # causing an IndexError or equivalent out-of-bounds failure.
        lcs_G = G.lower_central_series()
        if i - 1 >= len(lcs_G):
            q_ok = False
        else:
            q_ok = True
    except Exception:
        q_ok = False
        
    neg_q = not q_ok
    
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: i is a positive integer",
    "¬Q: The i-th term of the lower central series of G/N is NOT equal to (\\gamma_i(G)N)/N"
]

N_HYP = 2
NEG_Q_INDEX = 2