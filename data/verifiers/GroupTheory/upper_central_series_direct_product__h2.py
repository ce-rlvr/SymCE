import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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

def get_array(g, deg):
    """Returns the array form of a permutation padded to the specified degree."""
    arr = g.array_form
    if len(arr) < deg:
        arr = arr + list(range(len(arr), deg))
    return arr

def direct_product(G, H):
    """Constructs the direct product of two permutation groups."""
    deg_g = max(G.degree, 1)
    deg_h = max(H.degree, 1)
    gens = []
    
    for g in G.generators:
        arr = get_array(g, deg_g) + list(range(deg_g, deg_g + deg_h))
        gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(range(deg_g)) + [x + deg_g for x in get_array(h, deg_h)]
        gens.append(Permutation(arr))
        
    if not gens:
        gens.append(Permutation(list(range(deg_g + deg_h))))
        
    return PermutationGroup(gens), deg_g, deg_h

def combine(g, h, deg_g, deg_h):
    """Combines two permutations into a single permutation in the direct product."""
    arr_g = get_array(g, deg_g)
    arr_h = get_array(h, deg_h)
    arr_combined = arr_g + [x + deg_g for x in arr_h]
    return Permutation(arr_combined)

def upper_central_series_term(G, i):
    """Computes the i-th term of the upper central series of G."""
    elements = list(G.elements)
    gens = G.generators
    Z = {G.identity}
    
    for _ in range(i):
        next_Z = set()
        for x in elements:
            is_in_Z = True
            for y in gens:
                # Commutator [x, y] = x^-1 y^-1 x y
                comm = (~x) * (~y) * x * y
                if comm not in Z:
                    is_in_Z = False
                    break
            if is_in_Z:
                next_Z.add(x)
        if len(next_Z) == len(Z):
            break
        Z = next_Z
        
    return Z

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    The witness can be a tuple (G, H, i) or (G, H).
    """
    h1 = False
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, H, i_val = witness
                i_vals = [i_val]
            elif len(witness) == 2:
                G, H = witness
                max_i = int(max(G.order(), H.order())) + 1
                i_vals = range(1, max_i + 1)
            else:
                G, H = None, None
        else:
            G, H = None, None

        if G is not None and H is not None:
            h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1:
            GxH, deg_g, deg_h = direct_product(G, H)
            
            for i_raw in i_vals:
                try:
                    i = int(i_raw)
                except Exception:
                    continue
                
                Zi_GxH = upper_central_series_term(GxH, i)
                Zi_G = upper_central_series_term(G, i)
                Zi_H = upper_central_series_term(H, i)
                
                Zi_G_x_Zi_H = {combine(g, h, deg_g, deg_h) for g in Zi_G for h in Zi_H}
                
                if Zi_GxH != Zi_G_x_Zi_H:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: The i-th term of the upper central series of G x H is not Z_i(G) x Z_i(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1