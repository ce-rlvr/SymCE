import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_free_abelian(invs, rank):
    """
    Checks if a list of invariant factors represents a free abelian group of the given rank.
    In this representation, 0 denotes an infinite cyclic factor (Z), and k > 0 denotes Z_k.
    """
    return all(x == 0 for x in invs) and len(invs) == rank

def get_invs(G):
    """
    Extracts or approximates the abelian invariants of a group G.
    Returns a list of integers where 0 represents Z and k > 0 represents Z_k.
    """
    if hasattr(G, 'abelian_invariants'):
        return list(G.abelian_invariants())
    elif hasattr(G, 'is_group') and G.is_group:
        if hasattr(G, 'order'):
            try:
                o = G.order()
                if o == 1:
                    return []
                else:
                    # For finite groups, the exact invariants don't matter for freeness,
                    # any non-zero value correctly indicates the presence of torsion.
                    return [o]
            except Exception:
                pass
    elif isinstance(G, (list, tuple)):
        return list(G)
    elif isinstance(G, int):
        # An integer k represents the free abelian group Z^k
        return [0] * G
    raise ValueError("Cannot determine invariants for the given group representation")

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (A, B, m, n), checks if it is a valid counterexample.
    A and B can be represented as lists of invariant factors, integers (representing rank of Z^k),
    or SymPy groups.
    """
    try:
        A, B, m, n = witness
    except Exception:
        return [False, False]
        
    # H_1: B is a free abelian group of finite rank n
    try:
        invs_B = get_invs(B)
        h1_ok = is_free_abelian(invs_B, n)
    except Exception:
        h1_ok = False
        
    # ¬Q: The direct product A \times B is NOT a free abelian group of rank m + n
    try:
        invs_A = get_invs(A)
        invs_B = get_invs(B)
        # The invariants of the direct product is the concatenation of their cyclic factors
        prod_invs = invs_A + invs_B
        q_ok = is_free_abelian(prod_invs, m + n)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: B is a free abelian group of finite rank n",
    "¬Q: The direct product A x B is not a free abelian group of rank m + n"
]

N_HYP = 1
NEG_Q_INDEX = 1