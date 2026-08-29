import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
from sympy import S, ImageSet, Lambda
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1_ok = False
    neg_q = False
    
    # Extract R and a from the witness
    R = None
    a = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, a = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'a'):
            R = witness.R
            a = witness.a
        elif isinstance(witness, dict) and 'R' in witness and 'a' in witness:
            R = witness['R']
            a = witness['a']
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # Check H1: a is an element of R
    try:
        if hasattr(R, 'contains'):
            res = R.contains(a)
            if res is not None:
                h1_ok = bool(res)
        elif hasattr(R, '__contains__'):
            h1_ok = a in R
        elif isinstance(R, (list, set, tuple)):
            h1_ok = a in R
    except Exception:
        h1_ok = False

    # Check neg_Q: The conclusion fails.
    # The conclusion states that the principal left ideals Ra and R(1-a) are comaximal.
    # This requires 1-a to be a well-defined element of R, which implies R must have
    # a multiplicative identity. If R does not have an identity, the conclusion fails.
    try:
        has_id = False
        identity = None
        
        # 1. Try standard 1
        try:
            if hasattr(R, 'contains'):
                if R.contains(1) == True:
                    has_id = True
                    identity = 1
            elif 1 in R:
                has_id = True
                identity = 1
        except Exception:
            pass
            
        # 2. Try matrix identity
        if not has_id:
            try:
                if hasattr(a, 'shape') and len(a.shape) == 2 and a.shape[0] == a.shape[1]:
                    I = eye(a.shape[0])
                    if hasattr(R, 'contains'):
                        if R.contains(I) == True:
                            has_id = True
                            identity = I
                    elif I in R:
                        has_id = True
                        identity = I
            except Exception:
                pass
                
        # 3. Try finding identity by iteration
        if not has_id:
            try:
                is_finite = True
                if hasattr(R, 'is_finite') and R.is_finite == False:
                    is_finite = False
                    
                if is_finite:
                    elements = []
                    iterator = iter(R)
                    for _ in range(200):
                        try:
                            elements.append(next(iterator))
                        except StopIteration:
                            break
                    
                    if len(elements) > 0:
                        for e in elements:
                            is_id = True
                            for elem in elements:
                                try:
                                    if e * elem != elem or elem * e != elem:
                                        is_id = False
                                        break
                                except Exception:
                                    is_id = False
                                    break
                            if is_id:
                                has_id = True
                                identity = e
                                break
            except Exception:
                pass
                
        if not has_id:
            neg_q = True
        else:
            neg_q = False
            # If it has an identity, verify Ra + R(1-a) == R for finite sets
            try:
                is_finite = True
                if hasattr(R, 'is_finite') and R.is_finite == False:
                    is_finite = False
                    
                if is_finite:
                    elements = list(R)
                    if len(elements) <= 100:
                        e_minus_a = identity - a
                        
                        Ra = [r * a for r in elements]
                        R_ema = [r * e_minus_a for r in elements]
                        
                        sum_set = []
                        for x_elem in Ra:
                            for y_elem in R_ema:
                                sum_set.append(x_elem + y_elem)
                                
                        for r in elements:
                            if r not in sum_set:
                                neg_q = True
                                break
                                
                        if not neg_q:
                            for s in sum_set:
                                if s not in elements:
                                    neg_q = True
                                    break
            except Exception:
                pass
                
    except Exception:
        neg_q = True

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of R",
    "¬Q: The principal left ideals Ra and R(1-a) are not comaximal (e.g., R has no identity)"
]

N_HYP = 1
NEG_Q_INDEX = 1