import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard groups
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # V4 is often represented as a subgroup of A4, but we'll leave it as A4 here
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, N, g), checks if it is a valid counterexample to the conjecture.
    The conjecture states that the size of the conjugacy class of gN in G/N divides
    the size of the conjugacy class of g in G.
    """
    try:
        G, N, g = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup) and G.is_finite
    except Exception:
        h1_ok = False

    # H_2: g is an element of G
    try:
        h2_ok = g in G
    except Exception:
        h2_ok = False

    # neg_Q: The size of the conjugacy class of gN in G/N DOES NOT divide the size of the conjugacy class of g in G.
    # We evaluate the sizes by computing the conjugacy classes directly.
    try:
        # Size of conjugacy class of g in G
        cl_g = set()
        for x in G.elements:
            cl_g.add(x**-1 * g * x)
        size_cl_g = len(cl_g)

        # Size of conjugacy class of gN in G/N
        # We define the conjugacy class of gN as the set of cosets { x^-1 g x N | x \in G }
        # This definition works even if N is not a normal subgroup (which is the dropped hypothesis).
        cl_gN = set()
        for x in G.elements:
            # Compute the coset x^-1 g x N
            conj_g = x**-1 * g * x
            # Represent the coset by its canonical representative or as a frozenset
            coset = frozenset([conj_g * n for n in N.elements])
            cl_gN.add(coset)
        size_cl_gN = len(cl_gN)

        # The conclusion fails if size_cl_gN does not divide size_cl_g
        neg_q_ok = (size_cl_g % size_cl_gN != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: g is an element of G",
    "¬Q: The size of the conjugacy class of gN in G/N does not divide the size of the conjugacy class of g in G"
]

N_HYP = 2
NEG_Q_INDEX = 2