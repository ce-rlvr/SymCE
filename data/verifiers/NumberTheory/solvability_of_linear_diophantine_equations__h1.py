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
# No specific named bindings needed for Number Theory; use integers or sympy expressions directly.

def conditions(witness) -> list[bool]:
    """
    Given a witness (a, b, c), checks if it satisfies the remaining hypotheses
    and if the conclusion FAILS.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            if a is None or b is None or c is None:
                return [False, False]
        else:
            if len(witness) != 3:
                return [False, False]
            a, b, c = witness
    except Exception:
        return [False, False]
        
    # H1: at least one of a or b is non-zero
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        h1_ok = not (sympy.simplify(a_sym) == 0 and sympy.simplify(b_sym) == 0)
    except Exception:
        h1_ok = False
        
    # neg_Q: conclusion fails
    try:
        c_sym = sympy.sympify(c)
        
        def check_has_sols(a_val, b_val, c_val):
            # Try exact rational arithmetic first
            try:
                a_rat = sympy.nsimplify(a_val, rational=True)
                b_rat = sympy.nsimplify(b_val, rational=True)
                c_rat = sympy.nsimplify(c_val, rational=True)
                
                if a_rat.is_Rational and b_rat.is_Rational and c_rat.is_Rational:
                    da, db, dc = a_rat.q, b_rat.q, c_rat.q
                    M = da * db * dc
                    A, B, C = a_rat*M, b_rat*M, c_rat*M
                    g = math.gcd(int(A), int(B))
                    if g == 0:
                        return int(C) == 0
                    return int(C) % g == 0
            except Exception:
                pass
                
            # Fallback for irrationals/algebraics: check a small grid
            try:
                if a_val != 0:
                    for y_val in range(-100, 101):
                        x_val = sympy.simplify((c_val - b_val*y_val) / a_val)
                        if x_val.is_integer == True:
                            if sympy.simplify(a_val*x_val + b_val*y_val - c_val) == 0:
                                return True
                        elif x_val.is_real:
                            try:
                                if abs(float(x_val) - round(float(x_val))) < 1e-9:
                                    x_int = int(round(float(x_val)))
                                    if sympy.simplify(a_val*x_int + b_val*y_val - c_val) == 0:
                                        return True
                            except Exception:
                                pass
                elif b_val != 0:
                    for x_val in range(-100, 101):
                        y_val = sympy.simplify((c_val - a_val*x_val) / b_val)
                        if y_val.is_integer == True:
                            if sympy.simplify(a_val*x_val + b_val*y_val - c_val) == 0:
                                return True
                        elif y_val.is_real:
                            try:
                                if abs(float(y_val) - round(float(y_val))) < 1e-9:
                                    y_int = int(round(float(y_val)))
                                    if sympy.simplify(a_val*x_val + b_val*y_int - c_val) == 0:
                                        return True
                            except Exception:
                                pass
                else:
                    return sympy.simplify(c_val) == 0
            except Exception:
                pass
            return False

        has_sols = check_has_sols(a_sym, b_sym, c_sym)
        
        def check_gcd_divides(a_val, b_val, c_val):
            try:
                g = sympy.gcd(a_val, b_val)
            except Exception:
                return False
            try:
                if g == 0:
                    return sympy.simplify(c_val) == 0
                val = sympy.simplify(c_val / g)
                if val.is_integer == True:
                    return True
                if val.is_real:
                    try:
                        if abs(float(val) - round(float(val))) < 1e-9:
                            v_int = int(round(float(val)))
                            if sympy.simplify(c_val - g * v_int) == 0:
                                return True
                    except Exception:
                        pass
            except Exception:
                pass
            return False
            
        gcd_div = check_gcd_divides(a_sym, b_sym, c_sym)
        
        # The conclusion is an iff statement. It fails if the two sides have different truth values.
        neg_q_ok = bool(has_sols != gcd_div)
        
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: at least one of a or b is non-zero",
    "¬Q: The conclusion fails (ax + by = c has integer solutions iff gcd(a,b) divides c is FALSE)"
]

N_HYP = 1
NEG_Q_INDEX = 1