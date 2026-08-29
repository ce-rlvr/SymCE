import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: x is an element of X, and G_x is the stabilizer of x in G",
    "¬Q: The equivalence (H acts transitively on the G-orbit of x iff G = H G_x) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Parse witness
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            x = witness['x']
            X = witness.get('X', set(range(G.degree)))
            G_x_witness = witness.get('G_x', None)
        else:
            if len(witness) == 3:
                G, H, x = witness
                X = set(range(G.degree))
                G_x_witness = None
            elif len(witness) == 4:
                G, H, X, x = witness
                G_x_witness = None
            elif len(witness) == 5:
                G, H, X, x, G_x_witness = witness
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: H is a subgroup of G
    try:
        h1 = all(g in G for g in H.generators)
    except Exception:
        h1 = False

    # H_2: x is an element of X, and G_x is the stabilizer of x in G
    try:
        h2 = x in X
        G_elements = set(G.elements)
        actual_G_x_elements = {g for g in G_elements if g(x) == x}
        
        if G_x_witness is not None:
            if hasattr(G_x_witness, 'elements'):
                G_x_w_elems = set(G_x_witness.elements)
            else:
                G_x_w_elems = set(G_x_witness)
            h2 = h2 and (G_x_w_elems == actual_G_x_elements)
    except Exception:
        h2 = False

    # Conclusion: H acts transitively on the G-orbit of x if and only if G = H G_x
    try:
        H_elements = set(H.elements)
        
        # Compute orbits
        G_orbit = {g(x) for g in G_elements}
        H_orbit = {h(x) for h in H_elements}
        
        # H acts transitively on the G-orbit of x iff its orbit covers the G-orbit
        is_transitive = (H_orbit == G_orbit)
        
        # Determine G_x elements to use
        if G_x_witness is not None:
            if hasattr(G_x_witness, 'elements'):
                G_x_elements = set(G_x_witness.elements)
            else:
                G_x_elements = set(G_x_witness)
        else:
            G_x_elements = actual_G_x_elements
            
        # Compute the set product H G_x
        # In SymPy, (k * h)(x) = h(k(x)). To match standard math notation h(k(x)), we use k * h.
        # We check both left and right multiplication conventions to be absolutely robust.
        HG_x_elements_math = {k * h for h in H_elements for k in G_x_elements}
        HG_x_elements_sympy = {h * k for h in H_elements for k in G_x_elements}
        
        is_eq = (HG_x_elements_math == G_elements) or (HG_x_elements_sympy == G_elements)
        
        # The conclusion is: is_transitive <==> is_eq
        # We want the negated conclusion (i.e., the equivalence fails)
        neg_q = (is_transitive != is_eq)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]