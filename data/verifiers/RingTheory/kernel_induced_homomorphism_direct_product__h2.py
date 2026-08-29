import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
import math
import itertools
import functools

# Top-level setup for potential witness references
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_attr(obj, attr):
    if isinstance(obj, dict) and attr in obj:
        return obj[attr]
    return getattr(obj, attr, None)

def find_zero(elements):
    if not elements:
        return None
    for z in elements:
        try:
            if all((z + a) == a for a in elements) and all((a + z) == a for a in elements):
                return z
        except Exception:
            pass
    return None

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 4:
                R = witness[0]
                S_list = witness[1]
                f_list = witness[2]
                f = witness[3]
            else:
                return [False, False, False, False]
        else:
            R = get_attr(witness, 'R')
            S_list = get_attr(witness, 'S_list')
            f_list = get_attr(witness, 'f_list')
            f = get_attr(witness, 'f')
            
        if R is None or S_list is None or f_list is None or f is None:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring
    h1 = False
    try:
        R_elements = list(R)
        z_R = find_zero(R_elements)
        if z_R is not None:
            h1 = True
            for a in R_elements:
                for b in R_elements:
                    if (a + b) not in R_elements:
                        h1 = False
                        break
                    if (a * b) not in R_elements:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: {f_alpha} is a family of ring homomorphisms
    h2 = False
    try:
        R_elements = list(R)
        if len(S_list) == len(f_list):
            h2 = True
            for S, f_a in zip(S_list, f_list):
                S_elements = list(S)
                z_S = find_zero(S_elements)
                if z_S is None:
                    h2 = False
                    break
                for a in R_elements:
                    for b in R_elements:
                        val_a = f_a[a] if isinstance(f_a, dict) else f_a(a)
                        val_b = f_a[b] if isinstance(f_a, dict) else f_a(b)
                        val_ab_add = f_a[a + b] if isinstance(f_a, dict) else f_a(a + b)
                        val_ab_mul = f_a[a * b] if isinstance(f_a, dict) else f_a(a * b)
                        if val_ab_add != val_a + val_b:
                            h2 = False
                        if val_ab_mul != val_a * val_b:
                            h2 = False
                        if val_a not in S_elements:
                            h2 = False
                        if not h2:
                            break
                    if not h2:
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H3: f is the uniquely induced ring homomorphism
    h3 = False
    try:
        R_elements = list(R)
        h3 = True
        for a in R_elements:
            val = f[a] if isinstance(f, dict) else f(a)
            val = list(val)
            if len(val) != len(S_list):
                h3 = False
                break
            for i, f_a in enumerate(f_list):
                val_a = f_a[a] if isinstance(f_a, dict) else f_a(a)
                if val[i] != val_a:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # neg_Q: The kernel of f is not the intersection of the kernels of f_alpha
    neg_q = False
    try:
        R_elements = list(R)
        z_R = find_zero(R_elements)
        z_S_list = [find_zero(list(S)) for S in S_list]
        
        ker_f = []
        for a in R_elements:
            val = f[a] if isinstance(f, dict) else f(a)
            val = list(val)
            is_zero = True
            if len(val) != len(z_S_list):
                is_zero = False
            else:
                for v, z in zip(val, z_S_list):
                    if v != z:
                        is_zero = False
                        break
            if is_zero:
                ker_f.append(a)
                
        provided_intersection = get_attr(witness, 'intersection')
        if provided_intersection is not None:
            intersection_ker_f_alpha = list(provided_intersection)
            is_equal = True
            for x in ker_f:
                if x not in intersection_ker_f_alpha:
                    is_equal = False
                    break
            if is_equal:
                for x in intersection_ker_f_alpha:
                    if x not in ker_f:
                        is_equal = False
                        break
            neg_q = not is_equal
        elif not f_list:
            # If the family is empty, the intersection of an empty family of subsets 
            # is often considered undefined or the universal class, which is not equal to ker(f).
            neg_q = True
        else:
            intersection_ker_f_alpha = list(R_elements)
            for i, f_a in enumerate(f_list):
                ker_f_a = []
                z_S = z_S_list[i]
                for a in R_elements:
                    val_a = f_a[a] if isinstance(f_a, dict) else f_a(a)
                    if val_a == z_S:
                        ker_f_a.append(a)
                intersection_ker_f_alpha = [x for x in intersection_ker_f_alpha if x in ker_f_a]
                
            is_equal = True
            for x in ker_f:
                if x not in intersection_ker_f_alpha:
                    is_equal = False
                    break
            if is_equal:
                for x in intersection_ker_f_alpha:
                    if x not in ker_f:
                        is_equal = False
                        break
                        
            neg_q = not is_equal

    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: {f_alpha} is a family of ring homomorphisms",
    "H_3: f is the uniquely induced ring homomorphism",
    "¬Q: The kernel of f is not the intersection of the kernels of f_alpha"
]

N_HYP = 3
NEG_Q_INDEX = 3