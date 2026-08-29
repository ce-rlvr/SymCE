import sympy
from sympy import Set, Union, S
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: K_1, K_2, ..., K_n are subsets of R^d",
    "H_2: For each i from 1 to n, K_i is compact",
    "¬Q: The union of the sets K_1, K_2, ..., K_n is not compact"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    try:
        iterator = iter(witness)
        sets = []
        for _ in range(1000):
            try:
                sets.append(next(iterator))
            except StopIteration:
                break
        else:
            # If the iterable has more than 1000 elements, we reject it to prevent hanging.
            # The notation K_1, ..., K_n implies a finite collection.
            return [False, False, False]
            
        if len(sets) == 0:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        # Check if all elements are SymPy Sets (which represent subsets of R^d in this context)
        h1 = all(isinstance(s, Set) for s in sets)
    except Exception:
        h1 = False
        
    try:
        # Check if each set is compact
        h2 = all(s.is_compact is True for s in sets)
    except Exception:
        h2 = False
        
    try:
        # Check if the union of the sets is NOT compact
        union_set = Union(*sets)
        neg_q = (union_set.is_compact is False)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]