import math
import itertools
import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        R_list = witness.get("R_list", [])
        S_list = witness.get("S_list", [])
        R = witness.get("R", None)
        S = witness.get("S", None)
    except AttributeError:
        return [False, False, False, False]
        
    try:
        is_ZZ = all(r == ZZ for r in R_list)
        is_finite = all(isinstance(r, int) and r >= 1 for r in R_list)
        
        if not (is_ZZ or is_finite):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: R_1, ..., R_n are commutative rings
    try:
        h1 = isinstance(R_list, list) and len(R_list) > 0 and (is_ZZ or is_finite)
    except Exception:
        h1 = False
        
    # H_2: R is the direct product R_1 \times ... \times R_n
    try:
        h2 = (R == tuple(R_list))
    except Exception:
        h2 = False
        
    # H_3: S is the direct product S_1 \times ... \times S_n
    try:
        expected_S = set(itertools.product(*S_list))
        h3 = isinstance(S, list) and set(tuple(s) for s in S) == expected_S
    except Exception:
        h3 = False
        
    # neg_Q: The localized ring S^{-1}R is not isomorphic to the direct product S_1^{-1}R_1 \times ... \times S_n^{-1}R_n
    neg_q = False
    try:
        if is_ZZ:
            # For ZZ, if S is empty (because some S_i is empty), S^{-1}R = R.
            # But if another S_j contains a non-unit, S_j^{-1}R_j is not isomorphic to R_j.
            # Thus the product of localizations has a different unit group than R.
            if not S:
                for s_set in S_list:
                    if any(abs(val) != 1 for val in s_set):
                        neg_q = True
                        break
        elif is_finite:
            # For finite rings Z/nZ, we can compute the exact size of the localized rings.
            # If the sizes differ, they are not isomorphic.
            def localization_size(R_tuple, S_set):
                closure = set(tuple(s) for s in S_set)
                identity = tuple(1 for _ in R_tuple)
                closure.add(identity)
                
                added = True
                while added:
                    added = False
                    new_elements = set()
                    for a in closure:
                        for b in closure:
                            ab = tuple((a[i] * b[i]) % R_tuple[i] for i in range(len(R_tuple)))
                            if ab not in closure:
                                new_elements.add(ab)
                    if new_elements:
                        closure.update(new_elements)
                        added = True
                        
                # In a finite commutative ring, the kernel of localization at S is Ann(s*) 
                # where s* is the product of all elements in the multiplicative closure of S.
                s_star = list(identity)
                for a in closure:
                    for i in range(len(R_tuple)):
                        s_star[i] = (s_star[i] * a[i]) % R_tuple[i]
                        
                size = 1
                for i in range(len(R_tuple)):
                    size *= R_tuple[i] // math.gcd(s_star[i], R_tuple[i])
                    
                return size

            size_S_inv_R = localization_size(tuple(R_list), S)
            
            size_prod = 1
            for i in range(len(R_list)):
                size_i = localization_size((R_list[i],), [(s,) for s in S_list[i]])
                size_prod *= size_i
                
            neg_q = (size_S_inv_R != size_prod)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R_1, ..., R_n are commutative rings",
    "H_2: R is the direct product R_1 \\times ... \\times R_n",
    "H_3: S is the direct product S_1 \\times ... \\times S_n",
    "¬Q: The localized ring S^{-1}R is not isomorphic to the direct product S_1^{-1}R_1 \\times ... \\times S_n^{-1}R_n"
]

N_HYP = 3
NEG_Q_INDEX = 3