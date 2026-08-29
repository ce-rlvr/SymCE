import sympy
from sympy.combinatorics import PermutationGroup, Permutation

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # witness is expected to be a dictionary with keys 'G', 'H', 'A', 'B', 'C', 'D'
    try:
        G = witness['G']
        H = witness['H']
        A = witness['A']
        B = witness['B']
        C = witness['C']
        D = witness['D']
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: B and D are subgroups of H
    try:
        h2 = (isinstance(B, PermutationGroup) and isinstance(D, PermutationGroup) and 
              B.is_subgroup(H) and D.is_subgroup(H))
    except Exception:
        h2 = False

    # neg_Q: The commutator subgroup of A x B and C x D is NOT equal to commutator(A, C) x commutator(B, D)
    try:
        def get_elements(obj):
            if hasattr(obj, 'elements'):
                return list(obj.elements)
            elif hasattr(obj, 'generate'):
                return list(obj.generate())
            elif hasattr(obj, 'generate_dim'):
                return list(obj.generate_dim())
            else:
                return list(obj)

        A_elems = get_elements(A)
        C_elems = get_elements(C)
        B_elems = get_elements(B)
        D_elems = get_elements(D)
        
        deg_G = G.degree
        for p in A_elems + C_elems:
            if hasattr(p, 'size') and p.size > deg_G:
                deg_G = p.size
                
        deg_H = H.degree
        for p in B_elems + D_elems:
            if hasattr(p, 'size') and p.size > deg_H:
                deg_H = p.size
                
        def direct_prod(p1, p2):
            arr1 = p1.array_form if hasattr(p1, 'array_form') else []
            if len(arr1) < deg_G:
                arr1 = arr1 + list(range(len(arr1), deg_G))
            arr2 = p2.array_form if hasattr(p2, 'array_form') else []
            if len(arr2) < deg_H:
                arr2 = arr2 + list(range(len(arr2), deg_H))
            arr = arr1 + [x + deg_G for x in arr2]
            return Permutation(arr)
            
        # Compute LHS: commutator of A x B and C x D
        comms_LHS = []
        for a in A_elems:
            for c in C_elems:
                ac = (~a) * (~c) * a * c
                for b in B_elems:
                    for d in D_elems:
                        bd = (~b) * (~d) * b * d
                        comms_LHS.append(direct_prod(ac, bd))
                        
        if not comms_LHS:
            LHS = PermutationGroup([Permutation()])
        else:
            LHS = PermutationGroup(comms_LHS)
            
        # Compute RHS: commutator(A, C) x commutator(B, D)
        ac_comms = []
        for a in A_elems:
            for c in C_elems:
                ac_comms.append((~a) * (~c) * a * c)
                
        if not ac_comms:
            AC = PermutationGroup([Permutation()])
        else:
            AC = PermutationGroup(ac_comms)
            
        bd_comms = []
        for b in B_elems:
            for d in D_elems:
                bd_comms.append((~b) * (~d) * b * d)
                
        if not bd_comms:
            BD = PermutationGroup([Permutation()])
        else:
            BD = PermutationGroup(bd_comms)
        
        RHS_gens = []
        for g in AC.generators:
            if not g.is_Identity:
                RHS_gens.append(direct_prod(g, Permutation()))
        for g in BD.generators:
            if not g.is_Identity:
                RHS_gens.append(direct_prod(Permutation(), g))
                
        if not RHS_gens:
            RHS = PermutationGroup([Permutation()])
        else:
            RHS = PermutationGroup(RHS_gens)
            
        # Check if they are equal
        are_equal = LHS.is_subgroup(RHS) and RHS.is_subgroup(LHS)
        neg_q = not are_equal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: B and D are subgroups of H",
    "¬Q: The commutator subgroup of A x B and C x D is NOT equal to commutator(A, C) x commutator(B, D)"
]

N_HYP = 2
NEG_Q_INDEX = 2