import sympy
import itertools
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

CONDITION_LABELS = [
    "H_1: G is a group with presentation < X | R >",
    "H_2: H is a group with presentation < Y | S >",
    "¬Q: The free product G * H is NOT isomorphic to < X \\cup Y | R \\cup S >"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        X, R, Y, S = witness
    except Exception:
        return [False, False, False]
    
    def is_valid_presentation(gens, rels):
        if not isinstance(gens, (list, tuple)): return False
        if len(gens) > 5: return False
        if not all(isinstance(g, str) for g in gens): return False
        if len(set(gens)) != len(gens): return False
        if not isinstance(rels, (list, tuple)): return False
        if len(rels) > 5: return False
        for rel in rels:
            if not isinstance(rel, (list, tuple)): return False
            if len(rel) > 20: return False
            for term in rel:
                if not isinstance(term, (list, tuple)) or len(term) != 2: return False
                idx, power = term
                if not isinstance(idx, int) or not (0 <= idx < len(gens)): return False
                if not isinstance(power, int): return False
        return True

    try:
        h1 = is_valid_presentation(X, R)
    except Exception:
        h1 = False

    try:
        h2 = is_valid_presentation(Y, S)
    except Exception:
        h2 = False

    neg_q = False
    if h1 and h2:
        try:
            def get_abelian_invariants(gens, rels):
                if not gens:
                    return []
                rows = len(rels)
                cols = len(gens)
                if rows == 0:
                    return [0] * cols
                
                M = sympy.zeros(rows, cols)
                for i, rel in enumerate(rels):
                    for idx, power in rel:
                        M[i, idx] += power
                        
                D = []
                for k in range(1, min(rows, cols) + 1):
                    gcd_k = 0
                    for row_indices in itertools.combinations(range(rows), k):
                        for col_indices in itertools.combinations(range(cols), k):
                            sub_M = M[row_indices, col_indices]
                            det = sub_M.det()
                            gcd_k = sympy.gcd(gcd_k, det)
                            if gcd_k == 1:
                                break
                        if gcd_k == 1:
                            break
                    if gcd_k == 0:
                        break
                    D.append(gcd_k)
                    
                inv_factors = []
                prev = 1
                for d in D:
                    inv_factors.append(abs(d) // prev)
                    prev = abs(d)
                    
                inv_factors.extend([0] * (cols - len(D)))
                return sorted([int(f) for f in inv_factors if f != 1])

            # Abelianization of G * H
            # The generators are disjoint union of X and Y
            GH_gens = ['G_' + g for g in X] + ['H_' + g for g in Y]
            GH_rels = []
            for rel in R:
                GH_rels.append([(idx, power) for idx, power in rel])
            for rel in S:
                GH_rels.append([(len(X) + idx, power) for idx, power in rel])
                
            ab_GH = get_abelian_invariants(GH_gens, GH_rels)
            
            # Abelianization of U = < X \cup Y | R \cup S >
            XY = []
            for g in X:
                if g not in XY:
                    XY.append(g)
            for g in Y:
                if g not in XY:
                    XY.append(g)
                    
            U_rels = []
            for rel in R:
                new_rel = []
                for idx, power in rel:
                    gen_name = X[idx]
                    new_idx = XY.index(gen_name)
                    new_rel.append((new_idx, power))
                U_rels.append(new_rel)
            for rel in S:
                new_rel = []
                for idx, power in rel:
                    gen_name = Y[idx]
                    new_idx = XY.index(gen_name)
                    new_rel.append((new_idx, power))
                U_rels.append(new_rel)
                
            ab_U = get_abelian_invariants(XY, U_rels)
            
            # If abelian invariants differ, the groups are definitely not isomorphic
            if ab_GH != ab_U:
                neg_q = True
                
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]