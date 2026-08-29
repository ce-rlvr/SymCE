import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def check_eq(a, b):
    """Safely check equality between two elements, handling SymPy expressions."""
    if a == b:
        return True
    try:
        diff = a - b
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
        return sympy.simplify(diff) == 0
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks the hypotheses and the negated conclusion.
    Returns [H_1, H_2, H_3, neg_Q].
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            e = witness.get('e')
            f = witness.get('f')
        elif hasattr(witness, 'R') and hasattr(witness, 'e') and hasattr(witness, 'f'):
            R = witness.R
            e = witness.e
            f = witness.f
        else:
            R, e, f = witness
    except Exception:
        return [False, False, False, False]

    # Case 1: R is an integer n, representing the ring Z_n
    if isinstance(R, int) and R > 0:
        n = R
        try:
            e_val = int(e) % n
            f_val = int(f) % n
            
            h1 = True  # Z_n is always a commutative ring
            h2 = ((e_val * e_val) % n == e_val) and ((f_val * f_val) % n == f_val)
            h3 = ((e_val + f_val) % n == 1 % n)
            
            ann_e = [x for x in range(n) if (x * e_val) % n == 0]
            ann_f = [x for x in range(n) if (x * f_val) % n == 0]
            sum_ann = set(((x + y) % n) for x in ann_e for y in ann_f)
            
            neg_q = len(sum_ann) != n
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Case 1b: R is a SymPy Zmod domain
    if hasattr(R, 'mod') and isinstance(R.mod, int):
        n = R.mod
        try:
            e_val = int(e) % n
            f_val = int(f) % n
            
            h1 = True
            h2 = ((e_val * e_val) % n == e_val) and ((f_val * f_val) % n == f_val)
            h3 = ((e_val + f_val) % n == 1 % n)
            
            ann_e = [x for x in range(n) if (x * e_val) % n == 0]
            ann_f = [x for x in range(n) if (x * f_val) % n == 0]
            sum_ann = set(((x + y) % n) for x in ann_e for y in ann_f)
            
            neg_q = len(sum_ann) != n
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Case 2: R is an explicit collection of elements (e.g., custom objects)
    try:
        elements = list(R)
        
        # Identify additive identity (zero)
        zero = None
        for z in elements:
            if all(check_eq(z + x, x) for x in elements):
                zero = z
                break
                
        # Identify multiplicative identity (one)
        one = None
        for o in elements:
            if all(check_eq(o * x, x) for x in elements):
                one = o
                break
                
        if zero is not None and one is not None:
            is_comm = True
            for x in elements:
                for y in elements:
                    if not check_eq(x + y, y + x) or not check_eq(x * y, y * x):
                        is_comm = False
                        break
                if not is_comm:
                    break
            h1 = is_comm
            
            h2 = check_eq(e * e, e) and check_eq(f * f, f)
            h3 = check_eq(e + f, one)
            
            ann_e = [x for x in elements if check_eq(x * e, zero)]
            ann_f = [x for x in elements if check_eq(x * f, zero)]
            
            sum_ann = []
            for x in ann_e:
                for y in ann_f:
                    sum_ann.append(x + y)
                    
            missing = False
            for r in elements:
                if not any(check_eq(r, s) for s in sum_ann):
                    missing = True
                    break
            neg_q = missing
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Case 3: R is a SymPy domain or generic ring object
    try:
        h1 = getattr(R, 'is_commutative', True)
        h2 = check_eq(e * e, e) and check_eq(f * f, f)
        one = R.one if hasattr(R, 'one') else 1
        h3 = check_eq(e + f, one)
        
        # For infinite rings or abstract domains, if e+f=1 and e,f are idempotents,
        # it is a mathematical theorem that Ann(e) + Ann(f) = R.
        # Thus, the negated conclusion is False.
        neg_q = False
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: e and f are idempotent elements in R",
    "H_3: e + f = 1",
    "¬Q: Ann_R(e) + Ann_R(f) != R"
]

N_HYP = 3
NEG_Q_INDEX = 3