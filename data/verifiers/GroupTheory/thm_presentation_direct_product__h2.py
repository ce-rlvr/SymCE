import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G = witness["G"]
        H = witness["H"]
        F_X = witness["F_X"]
        R = witness["R"]
        F_Y = witness["F_Y"]
        S = witness["S"]
    except KeyError:
        return [False, False, False]
        
    try:
        G_fp = FpGroup(F_X, R)
        h1 = bool(G.order() == G_fp.order())
    except Exception:
        h1 = False
        
    try:
        X_names = set(str(g) for g in F_X.generators)
        Y_names = set(str(g) for g in F_Y.generators)
        h2 = bool(X_names.isdisjoint(Y_names))
    except Exception:
        h2 = False
        
    try:
        XY_names = sorted(list(X_names)) + sorted(list(Y_names))
        res = free_group(" ".join(XY_names))
        F_XY_group = res[0]
        
        gen_map = {}
        for g in F_X.generators:
            for g_new in F_XY_group.generators:
                if str(g_new) == str(g):
                    gen_map[g] = g_new
                    break
        for g in F_Y.generators:
            for g_new in F_XY_group.generators:
                if str(g_new) == str(g):
                    gen_map[g] = g_new
                    break
                    
        def map_word(word, g_map, target_group):
            new_word = target_group.identity
            for gen, exp in word.array_form:
                new_word = new_word * (g_map[gen] ** exp)
            return new_word
            
        R_new = [map_word(w, gen_map, F_XY_group) for w in R]
        S_new = [map_word(w, gen_map, F_XY_group) for w in S]
        
        commutators = []
        for x in F_X.generators:
            for y in F_Y.generators:
                x_new = gen_map[x]
                y_new = gen_map[y]
                comm = (x_new**-1) * (y_new**-1) * x_new * y_new
                commutators.append(comm)
                
        K_fp = FpGroup(F_XY_group, R_new + S_new + commutators)
        
        G_H_order = G.order() * H.order()
        K_order = K_fp.order()
        
        neg_q = bool(G_H_order != K_order)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a group with presentation <X | R>", "H_2: The generating sets X and Y are disjoint", "¬Q: G x H is not isomorphic to the combined presentation"]
N_HYP = 2
NEG_Q_INDEX = 2