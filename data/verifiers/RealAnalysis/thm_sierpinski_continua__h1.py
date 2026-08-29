import sympy
from sympy import Set, Intersection, Union, EmptySet, Interval, FiniteSet, Reals

CONDITION_LABELS = [
    "H_1: {C_n} is a countable collection of pairwise disjoint closed subsets of X",
    "H_2: X = union(C_n)",
    "¬Q: At least two of the sets C_n are non-empty"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], Set) and isinstance(witness[1], (list, tuple, set)):
            X, C = witness
        elif isinstance(witness, (list, tuple, set)):
            C = witness
            is_collection = all(isinstance(c, Set) for c in C)
            if not is_collection:
                return [False, False, False]
            X = Union(*C) if C else EmptySet
        else:
            return [False, False, False]
            
        C_list = list(C)
        
        # H1: Countable collection of pairwise disjoint closed subsets of X
        is_collection = all(isinstance(c, Set) for c in C_list)
        if not is_collection:
            return [False, False, False]
            
        pairwise_disjoint = True
        for i in range(len(C_list)):
            for j in range(i + 1, len(C_list)):
                if not Intersection(C_list[i], C_list[j]).is_empty:
                    pairwise_disjoint = False
                    break
                    
        is_closed_in_X = True
        for c in C_list:
            try:
                closure_c = c.closure
                inter = Intersection(closure_c, X)
                if not (inter.is_subset(c) == True and c.is_subset(inter) == True):
                    is_closed_in_X = False
                    break
            except Exception:
                if c.is_closed is not True:
                    is_closed_in_X = False
                    break
                    
        h1 = pairwise_disjoint and is_closed_in_X
        
        # H2: X = Union(C_n)
        union_C = Union(*C_list) if C_list else EmptySet
        h2 = (union_C.is_subset(X) == True and X.is_subset(union_C) == True)
        
        # Negated Conclusion: At most one C_n is non-empty -> FAILS
        non_empty_count = sum(1 for c in C_list if c.is_empty is False or c != EmptySet)
        neg_q = non_empty_count >= 2
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]