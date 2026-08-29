import sympy as sp
from sympy import Poly
from sympy.abc import x
import functools

# Top-level setup for potential witness expressions
S3 = sp.combinatorics.SymmetricGroup(3)
S4 = sp.combinatorics.SymmetricGroup(4)
A4 = sp.combinatorics.AlternatingGroup(4)
D4 = sp.combinatorics.DihedralGroup(4)
C4 = sp.combinatorics.CyclicGroup(4)
V4 = sp.combinatorics.AlternatingGroup(4)
Z2 = sp.combinatorics.CyclicGroup(2)
Z3 = sp.combinatorics.CyclicGroup(3)
Z4 = sp.combinatorics.CyclicGroup(4)
Z6 = sp.combinatorics.CyclicGroup(6)
trivial = sp.combinatorics.CyclicGroup(1)

I2 = sp.matrices.eye(2)
I3 = sp.matrices.eye(3)
O2 = sp.matrices.zeros(2, 2)
O3 = sp.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "If R is an integral domain, P is a prime ideal, f(x) is primitive, and a_n not in P,
    then f(x) is irreducible in R[x]."
    
    Expected witness format:
    (R_str, P_gen, f_expr)  e.g., ("ZZ", 3, x**2 - 1)
    or just (P_gen, f_expr) which defaults to R = "ZZ".
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R_str, P_gen, f_expr = witness
            elif len(witness) == 2:
                R_str = "ZZ"
                P_gen, f_expr = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5
        
    try:
        f_expr = sp.sympify(f_expr, locals={'x': x})
    except Exception:
        return [False] * 5

    # H_1: R is an integral domain
    try:
        h1 = (R_str in ["ZZ", "QQ", "Z"])
    except Exception:
        h1 = False
        
    # H_2: P is a prime ideal of R
    try:
        if R_str in ["ZZ", "Z"]:
            p_val = abs(int(P_gen))
            h2 = (p_val == 0) or sp.isprime(p_val)
        elif R_str == "QQ":
            p_val = abs(int(P_gen))
            h2 = (p_val == 0)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: f(x) is a primitive polynomial
    try:
        if not f_expr.free_symbols.issubset({x}):
            h3 = False
        else:
            f_poly = Poly(f_expr, x)
            coeffs = f_poly.all_coeffs()
            if R_str in ["ZZ", "Z"]:
                h3 = (abs(functools.reduce(sp.gcd, coeffs)) == 1)
            elif R_str == "QQ":
                h3 = not f_poly.is_zero
            else:
                h3 = False
    except Exception:
        h3 = False
        
    # H_4: a_n not in P
    try:
        if not f_expr.free_symbols.issubset({x}):
            h4 = False
        else:
            f_poly = Poly(f_expr, x)
            a_n = f_poly.LC()
            if R_str in ["ZZ", "Z"]:
                if p_val == 0:
                    h4 = (a_n != 0)
                else:
                    h4 = (a_n % p_val != 0)
            elif R_str == "QQ":
                if p_val == 0:
                    h4 = (a_n != 0)
                else:
                    h4 = False
            else:
                h4 = False
    except Exception:
        h4 = False
        
    # ¬Q: f(x) is reducible
    try:
        if not f_expr.free_symbols.issubset({x}):
            neg_q = False
        else:
            if R_str in ["ZZ", "Z"]:
                domain = sp.ZZ
            else:
                domain = sp.QQ
                
            factors = sp.factor_list(f_expr, domain=domain)
            # A primitive polynomial is reducible if it factors into more than one non-unit (degree > 0)
            num_non_constant_factors = sum(mult for fac, mult in factors[1] if Poly(fac, x).degree() > 0)
            neg_q = (num_non_constant_factors > 1)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: P is a prime ideal of R",
    "H_3: f(x) is a primitive polynomial",
    "H_4: a_n not in P",
    "¬Q: f(x) is reducible"
]

N_HYP = 4
NEG_Q_INDEX = 4