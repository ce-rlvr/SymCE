import sympy
from sympy import S, Set, Interval, Union, ProductSet

# Top-level setup
# (No specific named objects required for Real Analysis)

def conditions(witness) -> list[bool]:
    try:
        A, U = witness
    except Exception:
        return [False, False]
    
    # H1: A is an arbitrary subset of R^n
    h1 = False
    try:
        if isinstance(A, Set):
            if A.is_subset(S.Reals) == True:
                h1 = True
            elif isinstance(A, ProductSet):
                h1 = all(arg.is_subset(S.Reals) == True for arg in A.args)
        elif isinstance(A, (list, set, tuple)):
            h1 = True
            if len(A) > 0:
                first = list(A)[0]
                if isinstance(first, (int, float)):
                    for x in A:
                        if not isinstance(x, (int, float)): 
                            h1 = False
                            break
                elif isinstance(first, (list, tuple)):
                    n = len(first)
                    for pt in A:
                        if not isinstance(pt, (list, tuple)) or len(pt) != n: 
                            h1 = False
                            break
                        else:
                            for x in pt:
                                if not isinstance(x, (int, float)): 
                                    h1 = False
                                    break
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist a countable subcollection of U that covers A
    neg_q = False
    try:
        if U == "singletons":
            if isinstance(A, Set):
                def is_uncountable(s):
                    if s == S.Reals:
                        return True
                    if isinstance(s, Interval):
                        return s.start < s.end
                    if isinstance(s, Union):
                        return any(is_uncountable(arg) for arg in s.args)
                    if isinstance(s, ProductSet):
                        return any(is_uncountable(arg) for arg in s.args) and all(arg != S.EmptySet for arg in s.args)
                    return False
                if is_uncountable(A):
                    neg_q = True
        elif isinstance(U, (list, set, tuple)):
            if isinstance(A, Set):
                union_U = Union(*U) if U else S.EmptySet
                neg_q = (A.is_subset(union_U) == False)
            else:
                union_U = set()
                for subset in U:
                    for pt in subset:
                        union_U.add(pt)
                covers = True
                for pt in A:
                    if pt not in union_U:
                        covers = False
                        break
                neg_q = not covers
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an arbitrary subset of R^n",
    "¬Q: There does not exist a countable subcollection of U that covers A"
]

N_HYP = 1
NEG_Q_INDEX = 1