import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def get_v(witness, x):
    if hasattr(witness, 'v'):
        if isinstance(witness.v, dict):
            return witness.v[x]
        else:
            return witness.v(x)
    elif hasattr(witness, 'valuation'):
        if isinstance(witness.valuation, dict):
            return witness.valuation[x]
        else:
            return witness.valuation(x)
    raise AttributeError("No valuation function found")

def check_euclidean(witness):
    elements = list(witness.elements)
    add = witness.add
    mul = witness.mul
    zero = witness.zero
    
    neg_list = []
    for a in elements:
        for b in elements:
            if add(a, b) == zero:
                neg_list.append((a, b))
                break
                
    def get_neg_fast(a):
        for x, y in neg_list:
            if x == a:
                return y
        return a

    regular = []
    for b in elements:
        if b == zero:
            continue
        is_reg = True
        for x in elements:
            if x != zero:
                if mul(b, x) == zero or mul(x, b) == zero:
                    is_reg = False
                    break
        if is_reg:
            regular.append(b)
            
    for b in regular:
        for a in elements:
            found = False
            for q in elements:
                qb = mul(q, b)
                neg_qb = get_neg_fast(qb)
                r1 = add(a, neg_qb)
                if r1 == zero:
                    found = True
                    break
                try:
                    if get_v(witness, r1) < get_v(witness, b):
                        found = True
                        break
                except Exception:
                    pass
                
                bq = mul(b, q)
                neg_bq = get_neg_fast(bq)
                r2 = add(a, neg_bq)
                if r2 == zero:
                    found = True
                    break
                try:
                    if get_v(witness, r2) < get_v(witness, b):
                        found = True
                        break
                except Exception:
                    pass
                    
            if not found:
                return False
    return True

def unique_add(lst, item):
    for x in lst:
        if x == item:
            return False
    lst.append(item)
    return True

def is_pir(witness):
    elements = list(witness.elements)
    add = witness.add
    mul = witness.mul
    zero = witness.zero
    
    def get_principal_ideal(x):
        ideal = [x]
        for a in elements:
            if add(x, a) == zero:
                unique_add(ideal, a)
                break
                
        added = True
        while added:
            added = False
            new_elems = []
            for a in ideal:
                for b in ideal:
                    s = add(a, b)
                    is_in_ideal = any(e == s for e in ideal)
                    if not is_in_ideal:
                        is_in_new = any(e == s for e in new_elems)
                        if not is_in_new:
                            new_elems.append(s)
                            
                for r in elements:
                    m1 = mul(r, a)
                    is_in_ideal = any(e == m1 for e in ideal)
                    if not is_in_ideal:
                        is_in_new = any(e == m1 for e in new_elems)
                        if not is_in_new:
                            new_elems.append(m1)
                            
                    m2 = mul(a, r)
                    is_in_ideal = any(e == m2 for e in ideal)
                    if not is_in_ideal:
                        is_in_new = any(e == m2 for e in new_elems)
                        if not is_in_new:
                            new_elems.append(m2)
            if new_elems:
                ideal.extend(new_elems)
                added = True
        return ideal

    principal_ideals = []
    for x in elements:
        ideal = get_principal_ideal(x)
        is_new = True
        for pid in principal_ideals:
            if len(pid) == len(ideal):
                all_in = True
                for e in ideal:
                    if not any(e == pe for pe in pid):
                        all_in = False
                        break
                if all_in:
                    is_new = False
                    break
        if is_new:
            principal_ideals.append(ideal)
            
    for I1 in principal_ideals:
        for I2 in principal_ideals:
            sum_ideal = []
            for a in I1:
                for b in I2:
                    s = add(a, b)
                    unique_add(sum_ideal, s)
                    
            is_principal = False
            for pid in principal_ideals:
                if len(pid) == len(sum_ideal):
                    all_in = True
                    for e in sum_ideal:
                        if not any(e == pe for pe in pid):
                            all_in = False
                            break
                    if all_in:
                        is_principal = True
                        break
            if not is_principal:
                return False
    return True

def check_H1(witness):
    if hasattr(witness, 'is_euclidean'):
        if callable(witness.is_euclidean):
            return witness.is_euclidean()
        else:
            return witness.is_euclidean
    return check_euclidean(witness)

def check_neg_Q(witness):
    if hasattr(witness, 'is_pir'):
        if callable(witness.is_pir):
            return not witness.is_pir()
        else:
            return not witness.is_pir
    return not is_pir(witness)

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(check_H1(witness))
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(check_neg_Q(witness))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is equipped with a Euclidean valuation function",
    "¬Q: R contains an ideal that is not generated by a single element"
]

N_HYP = 1
NEG_Q_INDEX = 1