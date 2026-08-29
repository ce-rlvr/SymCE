import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def direct_product_group(G, H):
    degG = G.degree
    degH = H.degree
    gens = []
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < degG:
            arr += list(range(len(arr), degG))
        arr += list(range(degG, degG + degH))
        gens.append(Permutation(arr))
    for h in H.generators:
        arr = list(h.array_form)
        if len(arr) < degH:
            arr += list(range(len(arr), degH))
        arr = list(range(degG)) + [x + degG for x in arr]
        gens.append(Permutation(arr))
    return PermutationGroup(gens)

def conditions(witness):
    try:
        G, H, A, B = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: B is a subgroup of H
    try:
        if isinstance(B, PermutationGroup):
            B_elems = set(B.generate())
            H_elems = set(H.generate())
            h2 = B_elems.issubset(H_elems)
        else:
            B_elems = set(B)
            H_elems = set(H.generate())
            h2 = len(B_elems) > 0 and B_elems.issubset(H_elems)
            if h2:
                for a in B_elems:
                    if ~a not in B_elems:
                        h2 = False
                        break
                    for b in B_elems:
                        if a * b not in B_elems:
                            h2 = False
                            break
    except Exception:
        h2 = False
        B_elems = set()

    # ¬Q: The normalizer of A x B in G x H is not equal to N_G(A) x N_H(B)
    try:
        if isinstance(A, PermutationGroup):
            A_elems = set(A.generate())
        else:
            A_elems = set(A)
            
        degG = G.degree
        degH = H.degree
        
        def pad(p, deg):
            arr = list(p.array_form)
            if len(arr) < deg:
                arr += list(range(len(arr), deg))
            return arr

        def dp_element(a, b):
            arr_a = pad(a, degG)
            arr_b = pad(b, degH)
            return Permutation(arr_a + [x + degG for x in arr_b])
            
        AxB = set()
        for a in A_elems:
            for b in B_elems:
                AxB.add(dp_element(a, b))
                
        GxH = direct_product_group(G, H)
        
        def normalizer(Grp, S_set):
            norm = set()
            for g in Grp.generate():
                if all(g * s * ~g in S_set for s in S_set):
                    norm.add(g)
            return norm
            
        N_GxH_AxB = normalizer(GxH, AxB)
        
        N_G_A = normalizer(G, A_elems)
        N_H_B = normalizer(H, B_elems)
        
        NG_x_NH = set()
        for g in N_G_A:
            for h in N_H_B:
                NG_x_NH.add(dp_element(g, h))
                
        neg_q = (N_GxH_AxB != NG_x_NH)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: B is a subgroup of H",
    "¬Q: The normalizer of A x B in G x H is not equal to N_G(A) x N_H(B)"
]

N_HYP = 2
NEG_Q_INDEX = 2