import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N).
    """
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = getattr(G, 'is_group', False)
    except Exception:
        h1_ok = False

    # H_2: The quotient group G/N is an abelian group
    # In formal verification, if the closure properties of N are dropped, 
    # "G/N is abelian" is evaluated as elements commuting modulo N, 
    # i.e., all commutators [x, y] belong to N.
    try:
        h2_ok = True
        for x in G.elements:
            for y in G.elements:
                comm = x**-1 * y**-1 * x * y
                if comm not in N:
                    h2_ok = False
                    break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # neg_Q: The commutator subgroup G' is NOT a subgroup of N
    # If N is just a subset, we check if G' is not a subset of N.
    try:
        G_prime = G.derived_subgroup()
        if hasattr(N, 'is_subgroup'):
            neg_q_ok = not G_prime.is_subgroup(N)
        else:
            neg_q_ok = False
            for g in G_prime.elements:
                if g not in N:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/N is an abelian group",
    "¬Q: The commutator subgroup G' is not a subgroup of N"
]

N_HYP = 2
NEG_Q_INDEX = 2