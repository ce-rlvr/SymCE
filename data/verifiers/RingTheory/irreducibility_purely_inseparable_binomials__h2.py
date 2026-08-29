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

# Top-level setup
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

def conditions(witness):
    try:
        K = witness.get('K')
        p = witness.get('p')
        a = witness.get('a')
    except Exception:
        return [False, False, False]
        
    # H1: K is a field of prime characteristic p
    try:
        if hasattr(K, 'characteristic'):
            char_K = K.characteristic()
        elif hasattr(K, 'char'):
            char_K = K.char
        else:
            char_K = None
            
        h1 = K.is_Field and char_K == p and sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H2: a is not a p-th power of any element in K
    try:
        is_pth_power = False
        if hasattr(K, 'is_FiniteField') and K.is_FiniteField:
            try:
                a_K = K(a)
                for i in range(K.order):
                    c = K(i)
                    if c**p == a_K:
                        is_pth_power = True
                        break
            except Exception:
                # If a cannot be converted to an element of K, it is not in K.
                # Thus it cannot be a p-th power of any element in K.
                is_pth_power = False
        else:
            try:
                K(a)
                # If a is in K, we conservatively assume it might be a p-th power
                # to avoid false positives in H2 for infinite fields.
                # (Any valid counterexample must have a not in K anyway).
                is_pth_power = True
            except Exception:
                is_pth_power = False
                
        h2 = not is_pth_power
    except Exception:
        h2 = False
        
    # neg_Q: x^p - a is NOT irreducible over K
    try:
        x_var = sympy.Symbol('x')
        a_expr = a.to_sympy() if hasattr(a, 'to_sympy') else sympy.sympify(a)
        poly_expr = x_var**p - a_expr
        poly = sympy.Poly(poly_expr, x_var, domain=K)
        neg_q = not poly.is_irreducible
    except Exception:
        # If Poly construction fails (e.g., a is not in K and doesn't form a valid poly),
        # then x^p - a is not a polynomial over K, hence not irreducible over K.
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field of prime characteristic p",
    "H_2: a is not a p-th power of any element in K",
    "¬Q: The polynomial x^p - a is not irreducible over K"
]

N_HYP = 2
NEG_Q_INDEX = 2