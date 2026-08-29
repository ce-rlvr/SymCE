import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def get_FpGroup():
    try:
        return type(SymmetricGroup(3).presentation())
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    FpGroup_class = get_FpGroup()
        
    # H1: G is a group with presentation <X | R>
    try:
        if hasattr(G, 'presentation'):
            G_fp = G.presentation()
            h1 = True
        elif hasattr(G, 'generators') and hasattr(G, 'relators') and hasattr(G, 'free_group'):
            G_fp = G
            h1 = True
        elif isinstance(G, tuple) and len(G) == 2 and hasattr(G[0], 'generators') and isinstance(G[1], list):
            if FpGroup_class is not None:
                G_fp = FpGroup_class(G[0], G[1])
                h1 = True
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: H is a group with presentation <Y | S>
    try:
        if hasattr(H, 'presentation'):
            H_fp = H.presentation()
            h2 = True
        elif hasattr(H, 'generators') and hasattr(H, 'relators') and hasattr(H, 'free_group'):
            H_fp = H
            h2 = True
        elif isinstance(H, tuple) and len(H) == 2 and hasattr(H[0], 'generators') and isinstance(H[1], list):
            if FpGroup_class is not None:
                H_fp = FpGroup_class(H[0], H[1])
                h2 = True
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: G x H is NOT isomorphic to the combined presentation
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            FpGroup = type(G_fp)
            F_G = G_fp.free_group
            F_H = H_fp.free_group
            
            X = [str(g) for g in F_G.generators]
            Y = [str(g) for g in F_H.generators]
            
            XY_names = list(set(X) | set(Y))
            XY_names.sort()
            
            try:
                order_G = G.order() if hasattr(G, 'order') else G_fp.order()
            except Exception:
                order_G = G_fp.order()
                
            try:
                order_H = H.order() if hasattr(H, 'order') else H_fp.order()
            except Exception:
                order_H = H_fp.order()
                
            order_GH = order_G * order_H
            
            if not XY_names:
                neg_q = bool(order_GH != 1)
            else:
                F_new = free_group(",".join(XY_names))[0]
                name_to_new_gen = {str(g): g for g in F_new.generators}
                
                def map_word(word):
                    new_word = F_new.identity
                    for gen, power in word.array_form:
                        new_gen = name_to_new_gen[str(gen)]
                        new_word = new_word * (new_gen ** power)
                    return new_word
                    
                R_new = [map_word(w) for w in G_fp.relators]
                S_new = [map_word(w) for w in H_fp.relators]
                
                commutators = []
                for x in X:
                    for y in Y:
                        gx = name_to_new_gen[x]
                        gy = name_to_new_gen[y]
                        commutators.append(gx * gy * gx**-1 * gy**-1)
                        
                all_rels = R_new + S_new + commutators
                new_G = FpGroup(F_new, all_rels)
                
                order_new = new_G.order()
                
                neg_q = bool(order_GH != order_new)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group with presentation <X | R>",
    "H_2: H is a group with presentation <Y | S>",
    "¬Q: G x H is not isomorphic to the combined presentation"
]

N_HYP = 2
NEG_Q_INDEX = 2