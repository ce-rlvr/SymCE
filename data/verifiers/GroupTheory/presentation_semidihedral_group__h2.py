import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def semidihedral_group(n):
    """
    Constructs the semidihedral group of order 2^{n+1} as a PermutationGroup.
    Presentation: < r, s | r^{2^n} = 1, s^2 = 1, s r s = r^{2^{n-1}-1} >
    """
    m = 2**n
    # r: x -> x + 1 mod m
    r_list = [(i + 1) % m for i in range(m)]
    # s: x -> (m//2 - 1)*x mod m
    s_list = [((m // 2 - 1) * i) % m for i in range(m)]
    
    r = Permutation(r_list)
    s = Permutation(s_list)
    return PermutationGroup(r, s)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (n, G).
    """
    try:
        n, G = witness
    except Exception:
        return [False, False]

    # H_1: Let n >= 3 be an integer.
    try:
        h1_ok = (int(n) == n) and (n >= 3)
    except Exception:
        h1_ok = False

    # neg_Q: G is NOT isomorphic to the semidihedral group of order 2^{n+1}.
    try:
        if not hasattr(G, 'order'):
            neg_q_ok = True
        elif G.order() != 2**(int(n) + 1):
            neg_q_ok = True
        else:
            # To prevent extremely slow isomorphism tests on unreasonably large groups
            if n > 10:
                neg_q_ok = False
            else:
                H = semidihedral_group(int(n))
                neg_q_ok = not G.is_isomorphic(H)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "¬Q: G is not isomorphic to the semidihedral group of order 2^{n+1}"
]

N_HYP = 1
NEG_Q_INDEX = 1