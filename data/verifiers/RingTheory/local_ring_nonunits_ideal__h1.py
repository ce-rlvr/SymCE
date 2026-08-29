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

def conditions(witness):
    def eq(x, y, R):
        if hasattr(R, 'eq'):
            return R.eq(x, y)
        return x == y

    def is_ideal(subset, R, elements):
        if not subset:
            return False
        has_zero = any(eq(x, R.zero, R) for x in subset)
        if not has_zero:
            return False
        for x in subset:
            for y in subset:
                s = R.add(x, y)
                if not any(eq(s, z, R) for z in subset):
                    return False
        for x in subset:
            for r in elements:
                rx = R.mul(r, x)
                xr = R.mul(x, r)
                if not any(eq(rx, z, R) for z in subset):
                    return False
                if not any(eq(xr, z, R) for z in subset):
                    return False
        return True

    def generate_ideal(generators, R, elements):
        ideal = []
        for g in generators:
            if not any(eq(g, x, R) for x in ideal):
                ideal.append(g)
        
        if not any(eq(R.zero, x, R) for x in ideal):
            ideal.append(R.zero)
            
        changed = True
        while changed:
            changed = False
            new_elements = []
            for i in range(len(ideal)):
                for j in range(i, len(ideal)):
                    s = R.add(ideal[i], ideal[j])
                    if not any(eq(s, x, R) for x in ideal + new_elements):
                        new_elements.append(s)
            for x in ideal:
                for r in elements:
                    rx = R.mul(r, x)
                    if not any(eq(rx, y, R) for y in ideal + new_elements):
                        new_elements.append(rx)
                    xr = R.mul(x, r)
                    if not any(eq(xr, y, R) for y in ideal + new_elements):
                        new_elements.append(xr)
            if new_elements:
                ideal.extend(new_elements)
                changed = True
        return ideal

    try:
        has_id = False
        if hasattr(witness, 'one') and hasattr(witness, 'elements'):
            elements = list(witness.elements)
            is_id = True
            for x in elements:
                if not eq(witness.mul(witness.one, x), x, witness):
                    is_id = False
                if not eq(witness.mul(x, witness.one), x, witness):
                    is_id = False
            has_id = is_id
        h1_ok = has_id
    except Exception:
        h1_ok = False

    try:
        R = witness
        elements = list(R.elements)
        
        units = []
        non_units = []
        for x in elements:
            has_left = False
            has_right = False
            for y in elements:
                if eq(R.mul(y, x), R.one, R):
                    has_left = True
                if eq(R.mul(x, y), R.one, R):
                    has_right = True
            if has_left and has_right:
                units.append(x)
            else:
                non_units.append(x)
                
        non_units_ideal = is_ideal(non_units, R, elements)
        
        principal_ideals = []
        for x in elements:
            ideal = generate_ideal([x], R, elements)
            is_new = True
            for pid in principal_ideals:
                if len(pid) == len(ideal) and all(any(eq(a, b, R) for b in pid) for a in ideal):
                    is_new = False
                    break
            if is_new:
                principal_ideals.append(ideal)
                
        all_ideals = list(principal_ideals)
        while True:
            new_ideals = []
            for I1 in all_ideals:
                for I2 in all_ideals:
                    sum_ideal = generate_ideal(I1 + I2, R, elements)
                    is_new = True
                    for I in all_ideals + new_ideals:
                        if len(I) == len(sum_ideal) and all(any(eq(a, b, R) for b in I) for a in sum_ideal):
                            is_new = False
                            break
                    if is_new:
                        new_ideals.append(sum_ideal)
            if not new_ideals:
                break
            all_ideals.extend(new_ideals)
            
        proper_ideals = []
        for I in all_ideals:
            if not any(eq(x, R.one, R) for x in I):
                proper_ideals.append(I)
                
        maximal_ideals = []
        for I in proper_ideals:
            is_maximal = True
            for J in proper_ideals:
                if I == J: continue
                if len(I) < len(J) and all(any(eq(a, b, R) for b in J) for a in I):
                    is_maximal = False
                    break
            if is_maximal:
                maximal_ideals.append(I)
                
        is_comm = True
        for x in elements:
            for y in elements:
                if not eq(R.mul(x, y), R.mul(y, x), R):
                    is_comm = False
                    break
            if not is_comm:
                break
                
        has_unique_max_ideal = (len(maximal_ideals) == 1)
        
        # The false conjecture drops the "commutative" hypothesis.
        # Depending on the interpretation of "local ring" in the generalized context,
        # it might mean "has a unique maximal two-sided ideal" or "is commutative and has a unique maximal ideal".
        # We check both common interpretations to ensure robustness.
        biconditional_1 = (has_unique_max_ideal == non_units_ideal)
        biconditional_2 = ((is_comm and has_unique_max_ideal) == non_units_ideal)
        
        neg_q_ok = (not biconditional_1) or (not biconditional_2)
        
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "¬Q: R is a local ring iff the set of all non-units in R forms an ideal is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1