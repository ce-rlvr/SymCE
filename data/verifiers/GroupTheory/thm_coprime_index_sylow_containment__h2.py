import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (G, H, p)
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, p = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # neg_Q: Conclusion fails
    try:
        index = G.order() // H.order()
        rhs = (index % p != 0)
        
        try:
            if not sympy.isprime(p):
                # If p is not prime, the concept of a Sylow p-subgroup is undefined.
                lhs = False
            else:
                P = G.sylow_subgroup(p)
                # H contains a Sylow p-subgroup of G iff the order of the Sylow p-subgroup divides the order of H.
                lhs = (H.order() % P.order() == 0)
        except Exception:
            lhs = False
            
        concl = (lhs == rhs)
        neg_q = not concl
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = ["H_1: G is a finite group", "H_2: H is a subgroup of G", "neg_Q: Conclusion fails"]

N_HYP = 2
NEG_Q_INDEX = 2