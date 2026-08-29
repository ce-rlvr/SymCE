import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The action of G on X is not faithful (so no base exists)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        from sympy.combinatorics import PermutationGroup
        
        if isinstance(witness, tuple):
            G = witness[0]
        else:
            G = witness
            
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    neg_q = False
    try:
        if isinstance(witness, tuple):
            G = witness[0]
            if len(witness) == 2:
                X_info = witness[1]
                
                if isinstance(X_info, PermutationGroup):
                    H = X_info
                    is_sub = True
                    for g in H.generators:
                        if not G.contains(g):
                            is_sub = False
                            break
                    if is_sub:
                        faithful = True
                        for N in G.normal_subgroups():
                            if N.order() > 1:
                                n_in_h = True
                                for ng in N.generators:
                                    if not H.contains(ng):
                                        n_in_h = False
                                        break
                                if n_in_h:
                                    faithful = False
                                    break
                        if not faithful:
                            neg_q = True

                elif isinstance(X_info, list):
                    # Interpretation 1: X_info is a list of permutations representing the image of G's generators
                    try:
                        img_G = PermutationGroup(X_info)
                        if G.order() > img_G.order():
                            neg_q = True
                    except Exception:
                        pass
                    
                    # Interpretation 2: X_info is a list of generators for a subgroup H (action on cosets G/H)
                    try:
                        H = PermutationGroup(X_info)
                        is_sub = True
                        for g in H.generators:
                            if not G.contains(g):
                                is_sub = False
                                break
                        if is_sub:
                            faithful = True
                            for N in G.normal_subgroups():
                                if N.order() > 1:
                                    n_in_h = True
                                    for ng in N.generators:
                                        if not H.contains(ng):
                                            n_in_h = False
                                            break
                                    if n_in_h:
                                        faithful = False
                                        break
                            if not faithful:
                                neg_q = True
                    except Exception:
                        pass
            elif len(witness) == 3:
                action = witness[2]
                if isinstance(action, list):
                    try:
                        img_G = PermutationGroup(action)
                        if G.order() > img_G.order():
                            neg_q = True
                    except Exception:
                        pass
    except Exception:
        pass

    return [h1, neg_q]