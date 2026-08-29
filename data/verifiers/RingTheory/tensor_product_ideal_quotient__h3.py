import sympy
from sympy import Matrix
import itertools
import math

# Top-level setup: named object bindings that the witness expression may reference.
# We provide a FiniteRng class to allow the witness to easily construct finite rings (including rngs without identity).
class FiniteRng:
    def __init__(self, elements, add_table, mul_table):
        self.elements = list(elements)
        self.add_table = add_table
        self.mul_table = mul_table
        self.zero = self.elements[0]
        
    def add(self, a, b):
        i = self.elements.index(a)
        j = self.elements.index(b)
        return self.add_table[i][j]
        
    def mul(self, a, b):
        i = self.elements.index(a)
        j = self.elements.index(b)
        return self.mul_table[i][j]

def check_ideal(R, J):
    if not J: return False
    for a in J:
        if a not in R.elements: return False
        for b in J:
            ab = R.add(a, b)
            if ab not in J: return False
            inv_b = None
            for x in R.elements:
                if R.add(b, x) == R.zero:
                    inv_b = x
                    break
            if inv_b is None: return False
            a_inv_b = R.add(a, inv_b)
            if a_inv_b not in J: return False
        for r in R.elements:
            ar = R.mul(a, r)
            if ar not in J: return False
            ra = R.mul(r, a)
            if ra not in J: return False
    return True

def check_H1(witness):
    try:
        R = witness[0]
        elements = R.elements
        zero = R.zero
        if zero not in elements: return False
        for a in elements:
            if R.add(a, zero) != a: return False
            if R.add(zero, a) != a: return False
            has_inv = False
            for b in elements:
                if R.add(a, b) == zero and R.add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                ab_add = R.add(a, b)
                if ab_add not in elements: return False
                if ab_add != R.add(b, a): return False
                ab_mul = R.mul(a, b)
                if ab_mul not in elements: return False
                if ab_mul != R.mul(b, a): return False
                for c in elements:
                    if R.add(ab_add, c) != R.add(a, R.add(b, c)): return False
                    if R.mul(ab_mul, c) != R.mul(a, R.mul(b, c)): return False
                    if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                    if R.mul(ab_add, c) != R.add(R.mul(a, c), R.mul(b, c)): return False
        return True
    except Exception:
        return False

def check_H2(witness):
    try:
        R = witness[0]
        I = witness[1]
        return check_ideal(R, I)
    except Exception:
        return False

def get_tensor_product_factors(R, I, J):
    elements = R.elements
    cosets = []
    seen = [False] * len(elements)
    for idx, r in enumerate(elements):
        if seen[idx]: continue
        coset = set()
        for j in J:
            rj = R.add(r, j)
            rj_idx = elements.index(rj)
            coset.add(rj_idx)
            seen[rj_idx] = True
        cosets.append(frozenset(coset))
        
    elem_idx_to_coset = {}
    for c_idx, c in enumerate(cosets):
        for elem_idx in c:
            elem_idx_to_coset[elem_idx] = c_idx
            
    generators = []
    for i in I:
        i_idx = elements.index(i)
        for c_idx in range(len(cosets)):
            generators.append((i_idx, c_idx))
            
    gen_to_idx = {g: idx for idx, g in enumerate(generators)}
    N = len(generators)
    
    relations = []
    def add_rel(d):
        row = [0] * N
        for g, coeff in d.items():
            row[gen_to_idx[g]] += coeff
        relations.append(tuple(row))
        
    for i1 in I:
        i1_idx = elements.index(i1)
        for i2 in I:
            i2_idx = elements.index(i2)
            i12 = R.add(i1, i2)
            i12_idx = elements.index(i12)
            for c_idx in range(len(cosets)):
                add_rel({(i12_idx, c_idx): 1, (i1_idx, c_idx): -1, (i2_idx, c_idx): -1})
                
    for c1_idx, c1 in enumerate(cosets):
        for c2_idx, c2 in enumerate(cosets):
            rep1_idx = next(iter(c1))
            rep2_idx = next(iter(c2))
            rep1 = elements[rep1_idx]
            rep2 = elements[rep2_idx]
            rep12 = R.add(rep1, rep2)
            rep12_idx = elements.index(rep12)
            c12_idx = elem_idx_to_coset[rep12_idx]
            for i in I:
                i_idx = elements.index(i)
                add_rel({(i_idx, c12_idx): 1, (i_idx, c1_idx): -1, (i_idx, c2_idx): -1})
                
    for i in I:
        i_idx = elements.index(i)
        for x in elements:
            ix = R.mul(i, x)
            ix_idx = elements.index(ix)
            for c_idx, c in enumerate(cosets):
                rep_idx = next(iter(c))
                rep = elements[rep_idx]
                xc_rep = R.mul(x, rep)
                xc_rep_idx = elements.index(xc_rep)
                xc_idx = elem_idx_to_coset[xc_rep_idx]
                add_rel({(ix_idx, c_idx): 1, (i_idx, xc_idx): -1})
                
    if not relations:
        return [0] * N
        
    mat = Matrix(relations)
    try:
        snf = mat.smith_normal_form()
        r = min(snf.rows, snf.cols)
        factors = [snf[i, i] for i in range(r)]
    except Exception:
        return None
        
    factors.extend([0] * (N - r))
    factors = [abs(f) for f in factors if abs(f) != 1]
    factors.sort()
    return factors

def get_quotient_factors(R, I, J):
    elements = R.elements
    IJ_gens = []
    for i in I:
        for j in J:
            ij = R.mul(i, j)
            if ij not in IJ_gens:
                IJ_gens.append(ij)
                
    IJ = list(IJ_gens)
    added = True
    while added:
        added = False
        new_elems = []
        for x in IJ:
            for y in IJ:
                xy = R.add(x, y)
                if xy not in IJ and xy not in new_elems:
                    new_elems.append(xy)
        if new_elems:
            IJ.extend(new_elems)
            added = True
            
    cosets = []
    seen = [False] * len(elements)
    for i in I:
        i_idx = elements.index(i)
        if seen[i_idx]: continue
        coset = set()
        for ij in IJ:
            x = R.add(i, ij)
            x_idx = elements.index(x)
            coset.add(x_idx)
            seen[x_idx] = True
        cosets.append(frozenset(coset))
        
    N = len(cosets)
    elem_idx_to_coset = {}
    for c_idx, c in enumerate(cosets):
        for elem_idx in c:
            elem_idx_to_coset[elem_idx] = c_idx
            
    relations = []
    for c1_idx, c1 in enumerate(cosets):
        for c2_idx, c2 in enumerate(cosets):
            rep1_idx = next(iter(c1))
            rep2_idx = next(iter(c2))
            rep1 = elements[rep1_idx]
            rep2 = elements[rep2_idx]
            rep12 = R.add(rep1, rep2)
            rep12_idx = elements.index(rep12)
            c12_idx = elem_idx_to_coset[rep12_idx]
            row = [0] * N
            row[c1_idx] += 1
            row[c2_idx] += 1
            row[c12_idx] -= 1
            relations.append(tuple(row))
            
    if not relations:
        return [0] * N
        
    mat = Matrix(relations)
    try:
        snf = mat.smith_normal_form()
        r = min(snf.rows, snf.cols)
        factors = [snf[i, i] for i in range(r)]
    except Exception:
        return None
        
    factors.extend([0] * (N - r))
    factors = [abs(f) for f in factors if abs(f) != 1]
    factors.sort()
    return factors

def get_all_ideals(R):
    elements = R.elements
    ideals = []
    
    def get_closure(generators):
        closure = list(generators)
        added = True
        while added:
            added = False
            new_elems = []
            for x in closure:
                for y in closure:
                    xy = R.add(x, y)
                    if xy not in closure and xy not in new_elems:
                        new_elems.append(xy)
                for r in elements:
                    rx = R.mul(r, x)
                    if rx not in closure and rx not in new_elems:
                        new_elems.append(rx)
                    xr = R.mul(x, r)
                    if xr not in closure and xr not in new_elems:
                        new_elems.append(xr)
            if new_elems:
                closure.extend(new_elems)
                added = True
        closure_indices = sorted([elements.index(x) for x in closure])
        return closure_indices

    seen_closures = []
    for a in elements:
        closure_indices = get_closure([a])
        if closure_indices not in seen_closures:
            seen_closures.append(closure_indices)
            ideals.append([elements[i] for i in closure_indices])
            
    for a in elements:
        for b in elements:
            closure_indices = get_closure([a, b])
            if closure_indices not in seen_closures:
                seen_closures.append(closure_indices)
                ideals.append([elements[i] for i in closure_indices])
                
    return ideals

def check_neg_Q(witness):
    try:
        if len(witness) == 3:
            R, I, J = witness
            if not check_ideal(R, J):
                return False
            tp_factors = get_tensor_product_factors(R, I, J)
            q_factors = get_quotient_factors(R, I, J)
            if tp_factors is None or q_factors is None:
                return False
            return tp_factors != q_factors
        elif len(witness) == 2:
            R, I = witness
            ideals = get_all_ideals(R)
            for J in ideals:
                tp_factors = get_tensor_product_factors(R, I, J)
                q_factors = get_quotient_factors(R, I, J)
                if tp_factors is not None and q_factors is not None:
                    if tp_factors != q_factors:
                        return True
            return False
        else:
            return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False, False]
        if len(witness) not in [2, 3]:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    h1 = check_H1(witness)
    h2 = check_H2(witness)
    neg_q = check_neg_Q(witness)
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: I ⊗_R (R/J) is not isomorphic to I/IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2