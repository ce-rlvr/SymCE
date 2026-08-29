import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.homomorphisms import homomorphism
from itertools import product

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

def pad_perm(p, deg):
    arr = list(p.array_form)
    if len(arr) < deg:
        arr.extend(range(len(arr), deg))
    return Permutation(arr)

def is_characteristic(G, A):
    deg = max(G.degree, A.degree)
    if deg == 0: 
        deg = 1
    
    G_elts = {pad_perm(g, deg) for g in G.generate()}
    A_elts = {pad_perm(a, deg) for a in A.generate()}
    
    if not A_elts.issubset(G_elts):
        return False
        
    if len(A_elts) == 1 or len(A_elts) == len(G_elts):
        return True
        
    G_pad = PermutationGroup(*[pad_perm(g, deg) for g in G.generators])
    gens = G_pad.generators
    elts = list(G_pad.generate())
    G_order = G_pad.order()
    
    for t in product(elts, repeat=len(gens)):
        valid_orders = True
        for i in range(len(gens)):
            if t[i].order() != gens[i].order():
                valid_orders = False
                break
        if not valid_orders:
            continue
            
        try:
            H_sub = PermutationGroup(*t)
            if H_sub.order() != G_order:
                continue
                
            phi = homomorphism(G_pad, G_pad, gens, t)
        except Exception:
            continue
            
        for a in A_elts:
            if phi(a) not in A_elts:
                return False
    return True

def direct_product_subgroups(G, H, degG, degH):
    degG = max(degG, 1)
    degH = max(degH, 1)
    gens = []
    
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < degG:
            arr.extend(range(len(arr), degG))
        arr.extend(range(degG, degG + degH))
        gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(range(degG))
        h_arr = list(h.array_form)
        if len(h_arr) < degH:
            h_arr.extend(range(len(h_arr), degH))
        arr.extend([x + degG for x in h_arr])
        gens.append(Permutation(arr))
        
    if not gens:
        return PermutationGroup(Permutation(degG + degH - 1))
    return PermutationGroup(*gens)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of PermutationGroup objects: (G, A, H, B)
    """
    try:
        G, A, H, B = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_characteristic(G, A)
    except Exception:
        h1 = False
        
    try:
        h2 = is_characteristic(H, B)
    except Exception:
        h2 = False
        
    try:
        degG = max(G.degree, A.degree, 1)
        degH = max(H.degree, B.degree, 1)
        
        GxH = direct_product_subgroups(G, H, degG, degH)
        AxB = direct_product_subgroups(A, B, degG, degH)
        
        neg_q = not is_characteristic(GxH, AxB)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a characteristic subgroup of G",
    "H_2: B is a characteristic subgroup of H",
    "¬Q: A x B is not a characteristic subgroup of G x H"
]

N_HYP = 2
NEG_Q_INDEX = 2