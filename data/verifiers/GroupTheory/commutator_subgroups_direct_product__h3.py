import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard groups
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def commutator_subgroup(U_elems, V_elems, degree):
    commutators = []
    for u in U_elems:
        for v in V_elems:
            c = (~u) * (~v) * u * v
            commutators.append(c)
    if not commutators:
        return PermutationGroup([Permutation([], size=degree)])
    return PermutationGroup(commutators)

def conditions(witness):
    try:
        G, H, A, B, C, D = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(A, PermutationGroup) and isinstance(C, PermutationGroup) and A.is_subgroup(G) and C.is_subgroup(G)
    except Exception:
        h2 = False
        
    try:
        G_deg = G.degree
        H_deg = H.degree
        
        def get_elems(X):
            if hasattr(X, 'elements'):
                return list(X.elements)
            return list(X)
            
        A_elems = get_elems(A)
        B_elems = get_elems(B)
        C_elems = get_elems(C)
        D_elems = get_elems(D)
        
        def dp_elem(g, h):
            g_arr = g.array_form
            g_arr = g_arr + list(range(len(g_arr), G_deg))
            h_arr = h.array_form
            h_arr = h_arr + list(range(len(h_arr), H_deg))
            return Permutation(g_arr + [x + G_deg for x in h_arr], size=G_deg + H_deg)
            
        AxB = [dp_elem(a, b) for a in A_elems for b in B_elems]
        CxD = [dp_elem(c, d) for c in C_elems for d in D_elems]
        
        LHS_group = commutator_subgroup(AxB, CxD, G_deg + H_deg)
        
        AC_group = commutator_subgroup(A_elems, C_elems, G_deg)
        BD_group = commutator_subgroup(B_elems, D_elems, H_deg)
        
        AC_elems = get_elems(AC_group)
        BD_elems = get_elems(BD_group)
        
        RHS_elems = [dp_elem(ac, bd) for ac in AC_elems for bd in BD_elems]
        RHS_group = PermutationGroup(RHS_elems) if RHS_elems else PermutationGroup([Permutation([], size=G_deg + H_deg)])
        
        neg_q = not (LHS_group.is_subgroup(RHS_group) and RHS_group.is_subgroup(LHS_group))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A and C are subgroups of G",
    "not Q: The commutator subgroup of A x B and C x D is not equal to the product of commutators"
]

N_HYP = 2
NEG_Q_INDEX = 2