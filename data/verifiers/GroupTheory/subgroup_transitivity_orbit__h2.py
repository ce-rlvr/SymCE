import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, H, x) where G and H are PermutationGroups and x is an integer.
    """
    try:
        G, H, x = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: x is an element of X, and G_x is the stabilizer of x in G
    # We also verify H is a PermutationGroup so the conclusion can be evaluated.
    try:
        h2 = isinstance(H, PermutationGroup) and isinstance(x, int) and x >= 0
    except Exception:
        h2 = False
        
    # ¬Q: It is NOT the case that (H acts transitively on the G-orbit of x iff G = H G_x)
    try:
        # Normalize permutations to the same degree to ensure safe equality checks
        max_degree = max(G.degree, H.degree, x + 1)
        
        def norm(p):
            return Permutation(p.array_form, size=max_degree)
            
        G_elements = {norm(g) for g in G.generate()}
        H_elements = {norm(h) for h in H.generate()}
        
        # Calculate orbits
        G_orbit = set(G.orbit(x))
        H_orbit = set(H.orbit(x))
        
        # H acts transitively on the G-orbit of x if and only if the H-orbit of x equals the G-orbit of x
        P = (H_orbit == G_orbit)
        
        # Calculate stabilizer G_x
        G_x = G.stabilizer(x)
        G_x_elements = {norm(k) for k in G_x.generate()}
        
        # Calculate the set H G_x
        HG_x_elements = {norm(h * k) for h in H_elements for k in G_x_elements}
        
        # G = H G_x
        Q = (G_elements == HG_x_elements)
        
        # The conclusion is P <==> Q. The negated conclusion is P != Q.
        neg_q = (P != Q)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x is an element of X, and G_x is the stabilizer of x in G",
    "¬Q: It is not the case that (H acts transitively on the G-orbit of x iff G = H G_x)"
]

N_HYP = 2
NEG_Q_INDEX = 2