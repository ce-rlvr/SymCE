import sympy
import math
import itertools
import functools
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

Z = sympy.S.Integers
Q = sympy.S.Rationals
R = sympy.S.Reals

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: sqrt(I) is the set of all x in R such that x^n in I for some positive integer n",
    "¬Q: sqrt(I) is not an ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        mod = 0
        # Witness can be just I (subset of Z) or a tuple (R, I)
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R_ring, I_set = witness
                if isinstance(R_ring, int) and R_ring > 1:
                    mod = R_ring
                elif hasattr(R_ring, 'characteristic') and callable(R_ring.characteristic):
                    c = R_ring.characteristic()
                    if c > 0:
                        mod = int(c)
                elif hasattr(R_ring, 'mod'):
                    mod = int(R_ring.mod)
            else:
                I_set = witness
        else:
            I_set = witness
            
        if not isinstance(I_set, (list, tuple, set)):
            return [False, False, False]
            
        if len(I_set) > 1000:
            return [False, False, False]
            
        if mod > 1000:
            return [False, False, False]
            
        I_ints = []
        for elem in I_set:
            val = int(elem)
            I_ints.append(val)
            
        if mod > 0:
            I_ints = [v % mod for v in I_ints]
            
        # H1 and H2 are trivially satisfied by our evaluation domain (Z or Z_m)
        H1 = True
        H2 = True
        
        sqrt_I = set()
        if mod == 0:
            # Evaluate in Z
            for y_val in I_ints:
                if abs(y_val) > 1000:
                    return [False, False, False]
                if y_val == 0:
                    sqrt_I.add(0)
                elif y_val == 1:
                    sqrt_I.update([1, -1])
                elif y_val == -1:
                    sqrt_I.add(-1)
                else:
                    for x_val in range(-abs(y_val), abs(y_val) + 1):
                        if x_val in (0, 1, -1):
                            continue
                        curr = x_val
                        while abs(curr) <= abs(y_val):
                            if curr == y_val:
                                sqrt_I.add(x_val)
                                break
                            curr *= x_val
            # A finite subset of Z is an ideal iff it is exactly {0}
            is_ideal = (sqrt_I == {0})
        else:
            # Evaluate in Z_mod
            for x_val in range(mod):
                curr = x_val
                # The sequence x^n mod m is eventually periodic with pre-period + period <= m
                for n in range(1, mod + 2):
                    if curr in I_ints:
                        sqrt_I.add(x_val)
                        break
                    curr = (curr * x_val) % mod
                    
            if not sqrt_I:
                is_ideal = False
            elif 0 not in sqrt_I:
                is_ideal = False
            else:
                is_ideal = True
                # Check closure under addition/subtraction
                for a in sqrt_I:
                    for b in sqrt_I:
                        if (a - b) % mod not in sqrt_I:
                            is_ideal = False
                            break
                    if not is_ideal:
                        break
                # Check closure under scalar multiplication
                if is_ideal:
                    for a in sqrt_I:
                        for r in range(mod):
                            if (r * a) % mod not in sqrt_I:
                                is_ideal = False
                                break
                        if not is_ideal:
                            break
                            
        neg_Q = not is_ideal
        return [H1, H2, neg_Q]
    except Exception:
        return [False, False, False]