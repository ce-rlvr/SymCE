import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
from sympy import ZZ, QQ, Rational, Integer
import math
import itertools
import functools

# Top-level setup for named objects that a witness expression might reference
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

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a and b are relatively prime",
    "H_3: n >= 2 is an integer",
    "H_4: ab = c^n",
    "¬Q: a and b are not both n-th powers up to a unit in R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    # Unpack witness. We support both (R, a, b, c, n) and (a, b, c, n) with implicit R=ZZ
    try:
        if len(witness) == 5:
            R, a, b, c, n = witness
        elif len(witness) == 4:
            a, b, c, n = witness
            R = ZZ
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: R is a unique factorization domain
    try:
        if R == ZZ or R == 'ZZ':
            h1 = True
        elif hasattr(R, 'is_UFD'):
            h1 = bool(R.is_UFD)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: a and b are relatively prime
    try:
        h2 = (sympy.gcd(a, b) == 1)
    except Exception:
        h2 = False

    # H_3: n >= 2 is an integer
    try:
        n_int = int(n)
        h3 = (n_int == n) and (n_int >= 2)
    except Exception:
        h3 = False

    # H_4: ab = c^n
    try:
        diff = sympy.simplify(a * b - c**n)
        if diff == 0:
            h4 = True
        else:
            try:
                h4 = abs(float(diff)) < 1e-9
            except Exception:
                h4 = False
    except Exception:
        h4 = False

    # ¬Q: a and b are not both n-th powers up to a unit in R
    try:
        def is_nth_power_up_to_unit(val, n_val):
            if R == ZZ or R == 'ZZ':
                try:
                    val_int = int(val)
                    # Ensure val is strictly an integer (rejects floats/expressions that aren't integers)
                    if val_int != val:
                        return False
                    n_int = int(n_val)
                except Exception:
                    return False
                
                if val_int == 0:
                    return True
                
                # In ZZ, units are 1 and -1
                for u in [1, -1]:
                    if val_int % u != 0:
                        continue
                    target = val_int // u
                    if n_int % 2 == 0 and target < 0:
                        continue
                    
                    # Check if target is a perfect n-th power
                    r = int(abs(target) ** (1 / n_int) + 0.5)
                    found = False
                    for guess in [r - 1, r, r + 1]:
                        if guess >= 0 and guess ** n_int == target:
                            found = True
                            break
                    if found:
                        return True
                return False
            else:
                # Fallback for other rings: assume it IS a power to avoid false positives on neg_Q
                return True

        a_is_power = is_nth_power_up_to_unit(a, n)
        b_is_power = is_nth_power_up_to_unit(b, n)
        
        neg_q = not (a_is_power and b_is_power)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]