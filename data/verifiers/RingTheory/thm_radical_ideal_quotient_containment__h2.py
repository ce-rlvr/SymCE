import sympy
from sympy import ZZ, QQ
from sympy import abc
import math
import itertools
import functools

# Top-level setup
Z = ZZ

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, I, x = witness
    except Exception:
        return [False, False, False]
    
    # H1: R is a commutative ring
    # We support R being sympy.ZZ (or 0) for the ring of integers,
    # or an integer n >= 2 for the ring Z/nZ.
    is_Z = False
    n = None
    try:
        if R == sympy.ZZ or R == 0 or str(R) == 'ZZ':
            is_Z = True
            H1 = True
        else:
            n = int(R)
            H1 = (n >= 2)
    except Exception:
        H1 = False

    # H2: x is an element of R
    try:
        if is_Z:
            x = int(x)
            H2 = True
        else:
            x = int(x)
            H2 = (0 <= x < n)
    except Exception:
        H2 = False

    # neg_Q: \sqrt{(I : x)} is not a subset of (\sqrt{I} : x)
    neg_Q = False
    try:
        if is_Z:
            I_set = set(int(i) for i in I)
            if x == 0:
                # If x == 0, (I : 0) is either empty or all of Z.
                # In either case, the subset relation holds, so neg_Q is False.
                neg_Q = False
            else:
                I_colon_x = { i // x for i in I_set if i % x == 0 }
                
                def get_roots(S):
                    roots = set()
                    for s in S:
                        if s == 0:
                            roots.add(0)
                        elif s == 1:
                            roots.add(1)
                            roots.add(-1)
                        elif s == -1:
                            roots.add(-1)
                        else:
                            for r in range(-abs(s), abs(s) + 1):
                                if r in (0, 1, -1):
                                    continue
                                curr = r
                                while abs(curr) <= abs(s):
                                    if curr == s:
                                        roots.add(r)
                                        break
                                    curr *= r
                            roots.add(s)
                    return roots

                rad_I_colon_x = get_roots(I_colon_x)
                rad_I = get_roots(I_set)
                
                rad_I_colon_x_2 = { i // x for i in rad_I if i % x == 0 }
                
                neg_Q = not rad_I_colon_x.issubset(rad_I_colon_x_2)
                
        else:
            I_set = {int(i) % n for i in I}
            
            def quotient(A, x_val, mod):
                return { r for r in range(mod) if (r * x_val) % mod in A }
            
            def radical(A, mod):
                rad = set()
                for r in range(mod):
                    curr = r
                    # In Z/nZ, the sequence r^k is eventually periodic.
                    # It must hit A within the first n steps if it ever does.
                    for _ in range(1, mod + 1):
                        if curr in A:
                            rad.add(r)
                            break
                        curr = (curr * r) % mod
                return rad
            
            I_colon_x = quotient(I_set, x, n)
            rad_I_colon_x = radical(I_colon_x, n)
            
            rad_I = radical(I_set, n)
            rad_I_colon_x_2 = quotient(rad_I, x, n)
            
            neg_Q = not rad_I_colon_x.issubset(rad_I_colon_x_2)
            
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x is an element of R",
    "¬Q: \\sqrt{(I : x)} is not a subset of (\\sqrt{I} : x)"
]

N_HYP = 2
NEG_Q_INDEX = 2