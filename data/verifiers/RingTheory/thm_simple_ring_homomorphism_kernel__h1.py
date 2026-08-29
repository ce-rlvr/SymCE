import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    # Extract R, add, mul, zero, f, S_add, S_mul, S_zero
    R = None
    try:
        if isinstance(witness, int):
            if witness == 0:
                R = [0]
                zero = 0
                S_zero = 0
                add = lambda x, y: 0
                mul = lambda x, y: 0
                f = lambda x: 0
                S_add = lambda x, y: 0
                S_mul = lambda x, y: 0
            elif witness > 0:
                n = witness
                R = list(range(n))
                zero = 0
                S_zero = 0
                add = lambda x, y: (x + y) % n
                mul = lambda x, y: (x * y) % n
                f = lambda x: 0
                S_add = lambda x, y: 0
                S_mul = lambda x, y: 0
        elif hasattr(witness, 'is_zero') and witness.is_zero:
            R = [0]
            zero = 0
            S_zero = 0
            add = lambda x, y: 0
            mul = lambda x, y: 0
            f = lambda x: 0
            S_add = lambda x, y: 0
            S_mul = lambda x, y: 0
        elif isinstance(witness, tuple) and len(witness) == 8:
            R, add, mul, zero, f, S_add, S_mul, S_zero = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'add'):
            R = witness.R
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            f = witness.f
            S_add = witness.S_add
            S_mul = witness.S_mul
            S_zero = witness.S_zero
        elif isinstance(witness, dict) and 'R' in witness:
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            f = witness['f']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            S_zero = witness['S_zero']
        elif isinstance(witness, (list, set, tuple)) and len(witness) == 1:
            R = list(witness)
            zero = R[0]
            S_zero = R[0]
            add = lambda x, y: zero
            mul = lambda x, y: zero
            f = lambda x: zero
            S_add = lambda x, y: zero
            S_mul = lambda x, y: zero
        elif isinstance(witness, str) and "zero" in witness.lower():
            R = [0]
            zero = 0
            S_zero = 0
            add = lambda x, y: 0
            mul = lambda x, y: 0
            f = lambda x: 0
            S_add = lambda x, y: 0
            S_mul = lambda x, y: 0
    except Exception:
        pass

    if R is None:
        return [False, False, False]

    try:
        unique_R = []
        for x in R:
            if x not in unique_R:
                unique_R.append(x)
        R_list = unique_R
        if len(R_list) == 0 or len(R_list) > 30:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a simple ring (containing no non-trivial two-sided ideals)
    h1_ok = False
    try:
        is_ring = True
        # Check abelian group under addition
        for a in R_list:
            if add(a, zero) != a or add(zero, a) != a: 
                is_ring = False; break
            for b in R_list:
                if add(a, b) != add(b, a): 
                    is_ring = False; break
                for c in R_list:
                    if add(a, add(b, c)) != add(add(a, b), c): 
                        is_ring = False; break
            if not is_ring: break
        
        if is_ring:
            # Check existence of additive inverses
            for a in R_list:
                has_inv = False
                for b in R_list:
                    if add(a, b) == zero:
                        has_inv = True
                        break
                if not has_inv: 
                    is_ring = False; break
                    
        if is_ring:
            # Check multiplication associativity and distributivity
            for a in R_list:
                for b in R_list:
                    for c in R_list:
                        if mul(a, mul(b, c)) != mul(mul(a, b), c): 
                            is_ring = False; break
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): 
                            is_ring = False; break
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): 
                            is_ring = False; break
                    if not is_ring: break
                if not is_ring: break

        if is_ring:
            # Check simplicity (no non-trivial two-sided ideals)
            is_simple = True
            for x in R_list:
                if x == zero: continue
                # Generate the two-sided ideal from x
                ideal = [x, zero] if x != zero else [zero]
                changed = True
                while changed:
                    changed = False
                    new_elems = []
                    for a in ideal:
                        for b in ideal:
                            s = add(a, b)
                            if s not in ideal and s not in new_elems:
                                new_elems.append(s)
                        for r in R_list:
                            m1 = mul(a, r)
                            if m1 not in ideal and m1 not in new_elems:
                                new_elems.append(m1)
                            m2 = mul(r, a)
                            if m2 not in ideal and m2 not in new_elems:
                                new_elems.append(m2)
                    if new_elems:
                        ideal.extend(new_elems)
                        changed = True
                if len(ideal) != len(R_list):
                    is_simple = False
                    break
            h1_ok = is_simple
    except Exception:
        h1_ok = False

    # H2: f is a ring homomorphism
    h2_ok = False
    try:
        is_hom = True
        if f(zero) != S_zero:
            is_hom = False
        else:
            for a in R_list:
                for b in R_list:
                    if f(add(a, b)) != S_add(f(a), f(b)): 
                        is_hom = False; break
                    if f(mul(a, b)) != S_mul(f(a), f(b)): 
                        is_hom = False; break
                if not is_hom: break
        h2_ok = is_hom
    except Exception:
        h2_ok = False

    # ¬Q: f is not exclusively injective or the zero homomorphism (it is both or neither)
    neg_q_ok = False
    try:
        is_inj = True
        f_values = []
        for a in R_list:
            v = f(a)
            if v in f_values:
                is_inj = False
                break
            f_values.append(v)
            
        is_zero_hom = True
        for a in R_list:
            if f(a) != S_zero:
                is_zero_hom = False
                break
                
        # The conclusion is an exclusive OR. It fails if both are true or both are false.
        q = (is_inj and not is_zero_hom) or (not is_inj and is_zero_hom)
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a simple ring (containing no non-trivial two-sided ideals)",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: f is not exclusively injective or the zero homomorphism (it is both or neither)"
]
N_HYP = 2
NEG_Q_INDEX = 2