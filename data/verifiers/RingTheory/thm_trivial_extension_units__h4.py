import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def get_callable(witness, name):
    try:
        val = witness[name]
    except (TypeError, KeyError, AttributeError):
        val = getattr(witness, name)
    if isinstance(val, dict):
        return lambda a, b, v=val: v[(a, b)]
    elif isinstance(val, list):
        return lambda a, b, v=val: v[a][b]
    return val

def get_list(witness, name):
    try:
        return witness[name]
    except (TypeError, KeyError, AttributeError):
        return getattr(witness, name)

def get_val(witness, name):
    try:
        return witness[name]
    except (TypeError, KeyError, AttributeError):
        return getattr(witness, name)

def check_H1(witness):
    try:
        R = get_list(witness, 'R')
        R_add = get_callable(witness, 'R_add')
        R_mul = get_callable(witness, 'R_mul')
        
        # Check closure
        for a in R:
            for b in R:
                if R_add(a, b) not in R: return False
                if R_mul(a, b) not in R: return False
                
        # Commutativity of addition
        for a in R:
            for b in R:
                if R_add(a, b) != R_add(b, a): return False
                
        # Associativity and Distributivity
        for a in R:
            for b in R:
                ab_add = R_add(a, b)
                ab_mul = R_mul(a, b)
                for c in R:
                    if R_add(ab_add, c) != R_add(a, R_add(b, c)): return False
                    if R_mul(ab_mul, c) != R_mul(a, R_mul(b, c)): return False
                    if R_mul(a, R_add(b, c)) != R_add(ab_mul, R_mul(a, c)): return False
                    if R_mul(ab_add, c) != R_add(R_mul(a, c), R_mul(b, c)): return False
                    
        zero = None
        for e in R:
            if all(R_add(e, a) == a for a in R):
                zero = e
                break
        if zero is None: return False
        
        for a in R:
            if not any(R_add(a, b) == zero for b in R): return False
            
        one = None
        for e in R:
            if all(R_mul(e, a) == a and R_mul(a, e) == a for a in R):
                one = e
                break
        if one is None: return False
        
        return True
    except Exception:
        return False

def check_H2(witness):
    try:
        R = get_list(witness, 'R')
        M = get_list(witness, 'M')
        R_add = get_callable(witness, 'R_add')
        R_mul = get_callable(witness, 'R_mul')
        M_add = get_callable(witness, 'M_add')
        rmul = get_callable(witness, 'rmul')
        mrul = get_callable(witness, 'mrul')
        
        for x in M:
            for y in M:
                if M_add(x, y) not in M: return False
        for a in R:
            for x in M:
                if rmul(a, x) not in M: return False
                if mrul(x, a) not in M: return False
                
        for x in M:
            for y in M:
                if M_add(x, y) != M_add(y, x): return False
                xy_add = M_add(x, y)
                for z in M:
                    if M_add(xy_add, z) != M_add(x, M_add(y, z)): return False
                    
        zero_M = None
        for e in M:
            if all(M_add(e, x) == x for x in M):
                zero_M = e
                break
        if zero_M is None: return False
        
        for x in M:
            if not any(M_add(x, y) == zero_M for y in M): return False
            
        for a in R:
            for b in R:
                ab_mul = R_mul(a, b)
                ab_add = R_add(a, b)
                for x in M:
                    if rmul(ab_mul, x) != rmul(a, rmul(b, x)): return False
                    if mrul(x, ab_mul) != mrul(mrul(x, a), b): return False
                    if rmul(ab_add, x) != M_add(rmul(a, x), rmul(b, x)): return False
                    if mrul(x, ab_add) != M_add(mrul(x, a), mrul(x, b)): return False
                    if rmul(a, mrul(x, b)) != mrul(rmul(a, x), b): return False
                    
        for a in R:
            for x in M:
                for y in M:
                    if rmul(a, M_add(x, y)) != M_add(rmul(a, x), rmul(a, y)): return False
                    if mrul(M_add(x, y), a) != M_add(mrul(x, a), mrul(y, a)): return False
                    
        return True
    except Exception:
        return False

def check_H3(witness):
    try:
        R = get_list(witness, 'R')
        M = get_list(witness, 'M')
        r = get_val(witness, 'r')
        m = get_val(witness, 'm')
        return r in R and m in M
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        R = get_list(witness, 'R')
        M = get_list(witness, 'M')
        R_add = get_callable(witness, 'R_add')
        R_mul = get_callable(witness, 'R_mul')
        M_add = get_callable(witness, 'M_add')
        rmul = get_callable(witness, 'rmul')
        mrul = get_callable(witness, 'mrul')
        r = get_val(witness, 'r')
        m = get_val(witness, 'm')
        
        id_R = None
        for e in R:
            if all(R_mul(e, a) == a and R_mul(a, e) == a for a in R):
                id_R = e
                break
                
        r_is_unit = False
        if id_R is not None:
            for s in R:
                if R_mul(r, s) == id_R and R_mul(s, r) == id_R:
                    r_is_unit = True
                    break
                    
        id_RM = None
        for e_r in R:
            for e_m in M:
                is_id = True
                for a in R:
                    for x in M:
                        p1_r = R_mul(e_r, a)
                        p1_m = M_add(rmul(e_r, x), mrul(e_m, a))
                        if p1_r != a or p1_m != x:
                            is_id = False
                            break
                        p2_r = R_mul(a, e_r)
                        p2_m = M_add(rmul(a, e_m), mrul(x, e_r))
                        if p2_r != a or p2_m != x:
                            is_id = False
                            break
                    if not is_id:
                        break
                if is_id:
                    id_RM = (e_r, e_m)
                    break
            if id_RM is not None:
                break
                
        rm_is_unit = False
        if id_RM is not None:
            for s in R:
                for n in M:
                    p1_r = R_mul(r, s)
                    p1_m = M_add(rmul(r, n), mrul(m, s))
                    p2_r = R_mul(s, r)
                    p2_m = M_add(rmul(s, m), mrul(n, r))
                    if (p1_r, p1_m) == id_RM and (p2_r, p2_m) == id_RM:
                        rm_is_unit = True
                        break
                if rm_is_unit:
                    break
                    
        return rm_is_unit != r_is_unit
    except Exception:
        return False

def conditions(witness):
    return [
        check_H1(witness),
        check_H2(witness),
        check_H3(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: R is a unital ring",
    "H_2: M is an R-bimodule",
    "H_3: R \\ltimes M is the trivial extension ring",
    "¬Q: (r, m) is a unit in R \\ltimes M iff r is a unit in R is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3