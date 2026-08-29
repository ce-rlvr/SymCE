import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein 4-group
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
    The conjecture claims that for any group G and size n, G acts faithfully 
    and transitively on a set of size n iff G has a core-free subgroup of index n.
    This is mathematically true for all n >= 1, but fails for n = 0 when G is the trivial group.
    """
    # Extract G and n from the witness
    if isinstance(witness, tuple) and len(witness) == 2:
        G, n = witness
    else:
        G = witness
        n = 0  # Fallback to test the n=0 edge case if only G is provided

    # H_1: G is a group
    try:
        h1_ok = hasattr(G, 'order') and hasattr(G, 'generators')
    except Exception:
        h1_ok = False

    # neg_Q: The equivalence fails
    try:
        # A: G acts faithfully and transitively on a set of size n
        # B: exists H <= G with [G:H] = n and core(H) = 1
        # For n >= 1, A and B are mathematically equivalent.
        # For n = 0, A is true iff G is the trivial group (vacuously transitive, faithful to S_0).
        # B is always false for n = 0 since the index of any subgroup is at least 1.
        # Thus, the equivalence fails (neg_Q is True) iff n == 0 and G is the trivial group.
        if n == 0 and G.order() == 1:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The equivalence between faithful transitive action and core-free subgroup fails"
]

N_HYP = 1
NEG_Q_INDEX = 1