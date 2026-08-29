import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the Suborbit Rank Theorem conjecture.
    Witness is expected to be a tuple (G, x) where G is a PermutationGroup and x is an integer.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        G, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: Let G be a group acting on a set X.
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Let G act on X \times X diagonally via g * (y, z) = (g * y, g * z).
    try:
        # This is a definitional property of the diagonal action, which is always true 
        # given that G is a valid permutation group.
        h2 = h1
    except Exception:
        h2 = False

    # H_3: Let x be a fixed element of X, and let G_x be its stabilizer in G.
    try:
        h3 = h1 and isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h3 = False

    # ¬Q: The number of orbits of G on X \times X is NOT equal to the number of orbits of G_x on X.
    try:
        if not (h1 and h3):
            neg_q = False
        else:
            domain_size = G.degree
            
            def get_num_orbits(H, d_size):
                try:
                    h_deg = H.degree
                except Exception:
                    h_deg = 0
                try:
                    orb_len = len(H.orbits())
                except Exception:
                    orb_len = 0
                # Add fixed points that might not be covered by H.orbits() if H.degree < d_size
                return orb_len + max(0, d_size - h_deg)

            # Number of orbits of G on X \times X
            # By Burnside's Lemma / Mackey's formula, this equals the sum over all orbits O of G on X
            # of the number of orbits of the stabilizer G_y on X (where y is a representative of O).
            orbits_G = G.orbits()
            num_orbits_X_times_X = 0
            for O in orbits_G:
                rep = sorted(list(O))[0]
                stab = G.stabilizer(rep)
                num_orbits_X_times_X += get_num_orbits(stab, domain_size)
            
            # Number of orbits of G_x on X
            G_x = G.stabilizer(x)
            num_orbits_G_x = get_num_orbits(G_x, domain_size)
            
            neg_q = (num_orbits_X_times_X != num_orbits_G_x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: G acts on X \\times X diagonally via g * (y, z) = (g * y, g * z)",
    "H_3: x is a fixed element of X, and G_x is its stabilizer in G",
    "¬Q: The number of orbits of G on X \\times X is not equal to the number of orbits of G_x on X"
]

N_HYP = 3
NEG_Q_INDEX = 3