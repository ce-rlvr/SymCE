import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks the remaining hypotheses and the negated conclusion for the conjecture.
    The witness is expected to provide G, N, H, n1, n2.
    """
    try:
        if isinstance(witness, dict):
            G = witness['G']
            N = witness['N']
            H = witness['H']
            n1 = witness['n1']
            n2 = witness['n2']
        else:
            G, N, H, n1, n2 = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: N is an abelian normal subgroup of G
    try:
        h2_ok = (isinstance(N, PermutationGroup) and 
                 N.is_subgroup(G) and 
                 N.is_abelian and 
                 N.is_normal(G))
    except Exception:
        h2_ok = False

    # H_3: n1 and n2 are elements of N
    try:
        h3_ok = n1 in N and n2 in N
    except Exception:
        h3_ok = False

    # ¬Q: The conclusion FAILS.
    # Conclusion: n1 and n2 are conjugate in G iff there exists h in H such that h * n1 * h^-1 == n2
    try:
        # P: n1 and n2 are conjugate in G
        P = any(g * n1 * ~g == n2 for g in G.elements)
        
        # Q: there exists h in H such that h * n1 * h^-1 == n2
        if hasattr(H, 'elements'):
            H_elements = H.elements
        else:
            H_elements = H
            
        Q = any(h * n1 * ~h == n2 for h in H_elements)
        
        # The conclusion is P == Q. The negated conclusion is P != Q.
        neg_q_ok = (P != Q)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is an abelian normal subgroup of G",
    "H_3: n1 and n2 are elements of N",
    "¬Q: Conjugacy in G is not equivalent to conjugacy by an element of H"
]

N_HYP = 3
NEG_Q_INDEX = 3