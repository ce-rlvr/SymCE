import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools
import math

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def extract(witness):
    """Helper to extract ring components from the witness."""
    if isinstance(witness, dict):
        return witness['R'], witness['add'], witness['mult'], witness['S'], witness['I']
    else:
        return witness.R, witness.add, witness.mult, witness.S, witness.I

def cond1(witness):
    try:
        R, add, mult, S, I = extract(witness)
        if not S: 
            return False
        for a in S:
            if a not in R: 
                return False
            for b in S:
                if mult(a, b) not in S:
                    return False
        return True
    except Exception:
        return False

def cond2(witness):
    try:
        R, add, mult, S, I = extract(witness)
        
        if any(a not in R for a in I): return False
        if any(a in S for a in I): return False
        if not I: return False
        
        # Check closure under addition
        for a in I:
            for b in I:
                if add(a, b) not in I: return False
                
        # Check closure under multiplication by R (two-sided ideal)
        for a in I:
            for r in R:
                if mult(r, a) not in I: return False
                if mult(a, r) not in I: return False
                
        # Check for zero element
        zero = None
        for z_elem in R:
            if all(add(z_elem, a) == a and add(a, z_elem) == a for a in R):
                zero = z_elem
                break
        if zero not in I: return False
        
        # Check for additive inverses
        for a in I:
            neg_a = None
            for b in R:
                if add(a, b) == zero and add(b, a) == zero:
                    neg_a = b
                    break
            if neg_a not in I: return False
            
        return True
    except Exception:
        return False

def cond3(witness):
    try:
        R, add, mult, S, I = extract(witness)
        
        for elem in R:
            if elem in I: continue
            
            # Generate ideal J containing I and elem
            J = list(I)
            if elem not in J:
                J.append(elem)
                
            changed = True
            while changed:
                changed = False
                new_elements = []
                for a in J:
                    for b in J:
                        c = add(a, b)
                        if c not in J and c not in new_elements:
                            new_elements.append(c)
                for a in J:
                    for r in R:
                        c1 = mult(r, a)
                        if c1 not in J and c1 not in new_elements:
                            new_elements.append(c1)
                        c2 = mult(a, r)
                        if c2 not in J and c2 not in new_elements:
                            new_elements.append(c2)
                if new_elements:
                    J.extend(new_elements)
                    changed = True
                    
            # Check if J intersects S
            if not any(y in S for y in J):
                return False
                
        return True
    except Exception:
        return False

def get_all_ideals(R, add, mult):
    principal_ideals = []
    for x_elem in R:
        J = [x_elem]
        changed = True
        while changed:
            changed = False
            new_elements = []
            for a in J:
                for b in J:
                    c = add(a, b)
                    if c not in J and c not in new_elements:
                        new_elements.append(c)
            for a in J:
                for r in R:
                    c1 = mult(r, a)
                    if c1 not in J and c1 not in new_elements:
                        new_elements.append(c1)
                    c2 = mult(a, r)
                    if c2 not in J and c2 not in new_elements:
                        new_elements.append(c2)
            if new_elements:
                J.extend(new_elements)
                changed = True
                
        is_new = True
        for P in principal_ideals:
            if len(P) == len(J) and all(y in P for y in J):
                is_new = False
                break
        if is_new:
            principal_ideals.append(J)
            
    zero = None
    for z_elem in R:
        if all(add(z_elem, a) == a and add(a, z_elem) == a for a in R):
            zero = z_elem
            break
            
    ideals = []
    zero_ideal = [zero] if zero is not None else []
    ideals.append(zero_ideal)
    
    for P in principal_ideals:
        new_ideals = []
        for I_existing in ideals:
            sum_ideal = []
            if not I_existing:
                sum_ideal = list(P)
            else:
                for a in I_existing:
                    for b in P:
                        c = add(a, b)
                        if c not in sum_ideal:
                            sum_ideal.append(c)
            
            is_new = True
            for existing in ideals + new_ideals:
                if len(existing) == len(sum_ideal) and all(y in existing for y in sum_ideal):
                    is_new = False
                    break
            if is_new:
                new_ideals.append(sum_ideal)
        ideals.extend(new_ideals)
        
    return ideals

def cond4(witness):
    try:
        R, add, mult, S, I = extract(witness)
        
        # A prime ideal must be a proper ideal
        if all(a in I for a in R):
            return True
            
        ideals = get_all_ideals(R, add, mult)
        
        is_prime = True
        for A in ideals:
            for B in ideals:
                # Check if A * B is a subset of I
                ab_in_I = True
                for a in A:
                    for b in B:
                        if mult(a, b) not in I:
                            ab_in_I = False
                            break
                    if not ab_in_I:
                        break
                        
                if ab_in_I:
                    a_in_I = all(a in I for a in A)
                    b_in_I = all(b in I for b in B)
                    if not (a_in_I or b_in_I):
                        is_prime = False
                        break
            if not is_prime:
                break
                
        return not is_prime
    except Exception:
        return False

def conditions(witness):
    return [cond1(witness), cond2(witness), cond3(witness), cond4(witness)]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: I is an ideal of R such that the intersection of I and S is empty",
    "H_3: For any ideal J of R strictly containing I, the intersection of J and S is non-empty",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3