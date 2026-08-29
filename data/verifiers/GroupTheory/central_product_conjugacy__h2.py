import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Given a witness tuple (G, z, x), checks if it is a valid counterexample to the conjecture.
    The dropped hypothesis is that x must be an element of G.
    """
    try:
        G, z, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
        # Prevent timeouts for excessively large groups
        if h1 and G.order() > 1000:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: z is an element in the center Z(G)
    try:
        if not h1:
            h2 = False
        else:
            if z not in G:
                h2 = False
            else:
                # Check if z commutes with all elements in G
                h2 = all(g * z == z * g for g in G.elements)
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails at the witness
    try:
        if not h1:
            neg_q = False
        else:
            # If x is not in G, zx is not in G, so its conjugacy class in G is undefined.
            # This makes the statement mathematically false/invalid.
            if x not in G:
                neg_q = True
            else:
                # If x is in G, we evaluate the sets to see if they differ.
                # (Mathematically, they will always be equal if x is in G and z is in Z(G)).
                C = {g * z * x * ~g for g in G.elements}
                S = {z * g * x * ~g for g in G.elements}
                neg_q = not (C == S)
    except Exception:
        # If any operation fails (e.g., multiplying incompatible types), the conclusion fails.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: z is an element in the center Z(G)",
    "¬Q: The conjugacy class of zx is NOT equal to {z y | y is conjugate to x in G}"
]

N_HYP = 2
NEG_Q_INDEX = 2