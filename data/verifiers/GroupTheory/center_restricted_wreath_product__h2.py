import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def regular_representation(B):
    """Returns the regular permutation representation of a permutation group B."""
    elements = list(B.generate())
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    gens = []
    for gen in B.generators:
        p = [0] * len(elements)
        for i, e in enumerate(elements):
            # Left-to-right multiplication matches SymPy's permutation application
            p[i] = elem_to_idx[e * gen]
        gens.append(Permutation(p))
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def wreath_product(A, B):
    """Constructs the wreath product of permutation groups A and B."""
    deg_a = getattr(A, 'degree', 1)
    deg_b = getattr(B, 'degree', 1)
    if deg_a == 0: deg_a = 1
    if deg_b == 0: deg_b = 1
    
    gens = []
    # Generators for the base group A^B
    for gen_a in A.generators:
        for j in range(deg_b):
            p = list(range(deg_a * deg_b))
            for i in range(deg_a):
                p[i + j * deg_a] = gen_a(i) + j * deg_a
            gens.append(Permutation(p))
            
    # Generators for the acting group B
    for gen_b in B.generators:
        p = list(range(deg_a * deg_b))
        for j in range(deg_b):
            for i in range(deg_a):
                p[i + j * deg_a] = i + gen_b(j) * deg_a
        gens.append(Permutation(p))
        
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        A, B, W = witness
    except Exception:
        return [False, False, False]
        
    # H_1: A is a non-trivial group
    try:
        h1_ok = A.order() > 1
    except Exception:
        h1_ok = False
        
    # H_2: W is the restricted wreath product of A by B
    try:
        # Check against both the permutation wreath product and the regular wreath product
        # to robustly handle different interpretations of "wreath product of A by B".
        WP_perm = wreath_product(A, B)
        try:
            B_reg = regular_representation(B)
            WP_reg = wreath_product(A, B_reg)
        except Exception:
            WP_reg = None
            
        h2_ok = False
        if W == WP_perm or (W.order() == WP_perm.order() and W.is_isomorphic(WP_perm)):
            h2_ok = True
        elif WP_reg is not None and (W == WP_reg or (W.order() == WP_reg.order() and W.is_isomorphic(WP_reg))):
            h2_ok = True
    except Exception:
        h2_ok = False
        
    # ¬Q: The center of W is NOT the trivial subgroup
    try:
        neg_q_ok = W.center().order() > 1
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a non-trivial group",
    "H_2: W is the restricted wreath product of A by B",
    "¬Q: The center of W is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2