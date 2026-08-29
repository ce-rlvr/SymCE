import sympy
from sympy import Matrix
import itertools
import functools
import math

# Top-level setup for the caller to easily construct finite rings of matrices over F_2
M2_F2 = [Matrix([[a, b], [c, d]]) for a in (0, 1) for b in (0, 1) for c in (0, 1) for d in (0, 1)]
UT2_F2 = [Matrix([[a, b], [0, d]]) for a in (0, 1) for b in (0, 1) for d in (0, 1)]

def add_mat_F2(A, B):
    return (A + B).applyfunc(lambda x: x % 2)

def mul_mat_F2(A, B):
    return (A * B).applyfunc(lambda x: x % 2)

zero_mat_F2 = Matrix([[0, 0], [0, 0]])
one_mat_F2 = Matrix([[1, 0], [0, 1]])

def conditions(witness) -> list[bool]:
    try:
        R_orig = witness['R']
        S_orig = witness['S']
        add_R_orig = witness['add_R']
        mul_R_orig = witness['mul_R']
        zero_R_orig = witness['zero_R']
        add_S_orig = witness['add_S']
        mul_S_orig = witness['mul_S']
        zero_S_orig = witness['zero_S']
        f_orig = witness['f']
        
        # Create index mappings to handle unhashable elements like mutable matrices
        try:
            R_inv = {r: i for i, r in enumerate(R_orig)}
            def get_R_idx(val): return R_inv[val]
        except TypeError:
            def get_R_idx(val):
                for i, v in enumerate(R_orig):
                    if v == val: return i
                raise ValueError("Value not found in R")
                
        try:
            S_inv = {s: i for i, s in enumerate(S_orig)}
            def get_S_idx(val): return S_inv[val]
        except TypeError:
            def get_S_idx(val):
                for i, v in enumerate(S_orig):
                    if v == val: return i
                raise ValueError("Value not found in S")
                
        R = list(range(len(R_orig)))
        S = list(range(len(S_orig)))
        
        zero_R = get_R_idx(zero_R_orig)
        zero_S = get_S_idx(zero_S_orig)
        
        def add_R(i, j): return get_R_idx(add_R_orig(R_orig[i], R_orig[j]))
        def mul_R(i, j): return get_R_idx(mul_R_orig(R_orig[i], R_orig[j]))
        def add_S(i, j): return get_S_idx(add_S_orig(S_orig[i], S_orig[j]))
        def mul_S(i, j): return get_S_idx(mul_S_orig(S_orig[i], S_orig[j]))
        def f(i): return get_S_idx(f_orig(R_orig[i]))
        
    except Exception:
        return [False, False]

    # H_1: f is a ring homomorphism from R to S
    h1_ok = True
    try:
        for x in R:
            for y in R:
                if f(add_R(x, y)) != add_S(f(x), f(y)):
                    h1_ok = False
                    break
            if not h1_ok: break
        if h1_ok:
            for x in R:
                for y in R:
                    if f(mul_R(x, y)) != mul_S(f(x), f(y)):
                        h1_ok = False
                        break
                if not h1_ok: break
        if h1_ok:
            if f(zero_R) != zero_S:
                h1_ok = False
                
        if h1_ok and 'one_R' in witness and 'one_S' in witness:
            one_R = get_R_idx(witness['one_R'])
            one_S = get_S_idx(witness['one_S'])
            if f(one_R) != one_S:
                h1_ok = False
    except Exception:
        h1_ok = False

    # Compute nilradical of S (largest nilpotent ideal)
    try:
        nilrad_S = set([zero_S])
        for x in S:
            I_x = set([x])
            changed = True
            while changed:
                changed = False
                new_elems = set()
                for a in I_x:
                    for b in I_x:
                        new_elems.add(add_S(a, b))
                    for r in S:
                        new_elems.add(mul_S(r, a))
                        new_elems.add(mul_S(a, r))
                if not new_elems.issubset(I_x):
                    I_x.update(new_elems)
                    changed = True
            
            curr = set(I_x)
            is_nilp = False
            for _ in range(len(S) + 1):
                if all(e == zero_S for e in curr):
                    is_nilp = True
                    break
                prods = set(mul_S(a, b) for a in I_x for b in curr)
                nxt = set(prods)
                changed = True
                while changed:
                    changed = False
                    new_sums = set(add_S(a, b) for a in nxt for b in nxt)
                    if not new_sums.issubset(nxt):
                        nxt.update(new_sums)
                        changed = True
                curr = nxt
                
            if is_nilp:
                nilrad_S.update(I_x)
                changed = True
                while changed:
                    changed = False
                    new_sums = set(add_S(a, b) for a in nilrad_S for b in nilrad_S)
                    if not new_sums.issubset(nilrad_S):
                        nilrad_S.update(new_sums)
                        changed = True
    except Exception:
        return [h1_ok, False]

    # Compute radical of ker f (intersection of prime ideals containing ker f)
    try:
        ker_f = set(r for r in R if f(r) == zero_S)
        
        rad_ker_f = set(ker_f)
        for x in R:
            if x in rad_ker_f:
                continue
            I_x = set([x])
            changed = True
            while changed:
                changed = False
                new_elems = set()
                for a in I_x:
                    for b in I_x:
                        new_elems.add(add_R(a, b))
                    for r in R:
                        new_elems.add(mul_R(r, a))
                        new_elems.add(mul_R(a, r))
                if not new_elems.issubset(I_x):
                    I_x.update(new_elems)
                    changed = True
            
            curr = set(I_x)
            is_in_rad = False
            for _ in range(len(R) + 1):
                if curr.issubset(ker_f):
                    is_in_rad = True
                    break
                prods = set(mul_R(a, b) for a in I_x for b in curr)
                nxt = set(prods)
                changed = True
                while changed:
                    changed = False
                    new_sums = set(add_R(a, b) for a in nxt for b in nxt)
                    if not new_sums.issubset(nxt):
                        nxt.update(new_sums)
                        changed = True
                curr = nxt
                
            if is_in_rad:
                rad_ker_f.add(x)
    except Exception:
        return [h1_ok, False]

    # Check if preimage of nilradical of S equals radical of ker f
    try:
        preimage_nilrad_S = set(r for r in R if f(r) in nilrad_S)
        neg_q = (preimage_nilrad_S != rad_ker_f)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "¬Q: The preimage of the nilradical of S under f is not equal to the radical of the kernel of f"
]

N_HYP = 1
NEG_Q_INDEX = 1