import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4) # V4 is often represented as a subgroup of A4, but we provide standard groups
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: K is a field (represented by a valid group theory context)",
    "H_2: L1 and L2 are finite Galois extensions of K",
    "¬Q: The Galois group of the compositum is NOT isomorphic to the fiber product"
]

N_HYP = 2
NEG_Q_INDEX = 2

def _is_normal(G, N):
    """Check if N is a normal subgroup of G."""
    if not N.is_subgroup(G):
        return False
    for g in G.generate_dimino():
        for n in N.generate_dimino():
            if (g**-1 * n * g) not in N:
                return False
    return True

def _intersect_subgroups(G, N1, N2):
    """Return the intersection of two subgroups N1 and N2."""
    elements = set(N1.generate_dimino()).intersection(set(N2.generate_dimino()))
    return PermutationGroup(list(elements))

def _product_subgroups(G, N1, N2):
    """Return the product N1*N2 of two normal subgroups."""
    elements = set()
    for n1 in N1.generate_dimino():
        for n2 in N2.generate_dimino():
            elements.add(n1 * n2)
    return PermutationGroup(list(elements))

def _quotient_group_order(G, N):
    """Return the order of the quotient group G/N."""
    return G.order() // N.order()

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture.
    The witness is expected to be a tuple (G, N1, N2) representing the absolute 
    Galois group G and the normal subgroups N1, N2 corresponding to L1 and L2.
    """
    # H_1: K is a field (context is valid)
    try:
        G, N1, N2 = witness
        h1_ok = isinstance(G, PermutationGroup) and isinstance(N1, PermutationGroup) and isinstance(N2, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: L1 and L2 are finite Galois extensions of K
    try:
        if h1_ok:
            h2_ok = _is_normal(G, N1) and _is_normal(G, N2)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion FAILS
    # Conclusion: Gal(L1 L2 / K) is isomorphic to the fiber product of Gal(L1/K) and Gal(L2/K) over Gal(L1 \cap L2 / K).
    # In Galois correspondence:
    # L1 <-> N1, L2 <-> N2
    # L1 L2 <-> N1 \cap N2
    # L1 \cap L2 <-> N1 N2
    # Gal(L1 L2 / K) = G / (N1 \cap N2)
    # Fiber product order = |G/N1| * |G/N2| / |G/(N1 N2)|
    try:
        if h1_ok and h2_ok:
            N_int = _intersect_subgroups(G, N1, N2)
            N_prod = _product_subgroups(G, N1, N2)
            
            gal_L1L2_order = _quotient_group_order(G, N_int)
            gal_L1_order = _quotient_group_order(G, N1)
            gal_L2_order = _quotient_group_order(G, N2)
            gal_L1_cap_L2_order = _quotient_group_order(G, N_prod)
            
            fiber_product_order = (gal_L1_order * gal_L2_order) // gal_L1_cap_L2_order
            
            # If the orders don't match, they cannot be isomorphic.
            # (By Goursat's Lemma, they are always isomorphic for subfields of a common field, 
            # so if a counterexample is provided where this fails, neg_Q becomes True).
            conclusion_holds = (gal_L1L2_order == fiber_product_order)
            neg_q = not conclusion_holds
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]