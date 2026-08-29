import sympy
from sympy import I, pi, E, Rational
import math
import itertools
import functools

# Top-level setup
# No specific group theory bindings needed for this field theory conjecture.

def is_close(a, b):
    try:
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
        if isinstance(a, complex) and isinstance(b, complex):
            return math.isclose(a.real, b.real, rel_tol=1e-9, abs_tol=1e-9) and \
                   math.isclose(a.imag, b.imag, rel_tol=1e-9, abs_tol=1e-9)
    except Exception:
        pass
    return False

def is_field(F):
    try:
        if getattr(F, 'is_Field', False) or getattr(F, 'is_field', False):
            return True
        if F in [sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            return True
        if str(F) in ['RR', 'CC', 'QQ', 'Reals', 'Complexes', 'Rationals']:
            return True
        if hasattr(F, 'is_field') and F.is_field():
            return True
    except Exception:
        pass
    return False

def is_alg_closure(K, F):
    try:
        if hasattr(K, 'is_algebraic_closure_of'):
            return K.is_algebraic_closure_of(F)
        if (F == sympy.S.Reals or str(F) in ['RR', 'Reals']) and \
           (K == sympy.S.Complexes or str(K) in ['CC', 'Complexes']):
            return True
        if (F == sympy.S.Rationals or str(F) in ['QQ', 'Rationals']) and \
           (str(K) in ['QQbar', 'AlgebraicNumbers']):
            return True
    except Exception:
        pass
    return False

def check_sigma_fixes_F(sigma, F):
    test_elements = []
    if hasattr(F, 'test_elements'):
        test_elements = F.test_elements
    elif str(F) in ['RR', 'Reals', 'QQ', 'Rationals']:
        test_elements = [sympy.S(0), sympy.S(1), sympy.S(-1), sympy.S(2), sympy.Rational(1, 2)]
        if str(F) in ['RR', 'Reals']:
            test_elements.append(sympy.pi)
    else:
        test_elements = [0, 1, -1, 2]
        
    for a in test_elements:
        try:
            val = sigma(a)
            if val != a:
                if is_close(val, a):
                    continue
                if hasattr(val, 'equals') and val.equals(a):
                    continue
                if sympy.simplify(val - a) == 0:
                    continue
                return False
        except Exception:
            return False
    return True

def check_is_automorphism(sigma, K):
    test_elements = []
    if hasattr(K, 'test_elements'):
        test_elements = K.test_elements
    elif str(K) in ['CC', 'Complexes']:
        test_elements = [sympy.S(0), sympy.S(1), sympy.I, -sympy.I, 1+sympy.I, 2, sympy.pi]
    else:
        test_elements = [0, 1, -1, 2]
        
    for a in test_elements:
        for b in test_elements:
            # Addition
            try:
                sum_val = sigma(a + b)
                sum_sigma = sigma(a) + sigma(b)
                if sum_val != sum_sigma:
                    if is_close(sum_val, sum_sigma):
                        pass
                    elif hasattr(sum_val, 'equals') and sum_val.equals(sum_sigma):
                        pass
                    elif sympy.simplify(sum_val - sum_sigma) == 0:
                        pass
                    else:
                        return False
            except Exception:
                return False
                
            # Multiplication
            try:
                prod_val = sigma(a * b)
                prod_sigma = sigma(a) * sigma(b)
                if prod_val != prod_sigma:
                    if is_close(prod_val, prod_sigma):
                        pass
                    elif hasattr(prod_val, 'equals') and prod_val.equals(prod_sigma):
                        pass
                    elif sympy.simplify(prod_val - prod_sigma) == 0:
                        pass
                    else:
                        return False
            except Exception:
                return False
                
    # Check if sigma(1) == 1
    try:
        val = sigma(1)
        if val != 1:
            if is_close(val, 1):
                pass
            elif hasattr(val, 'equals') and val.equals(1):
                pass
            elif sympy.simplify(val - 1) == 0:
                pass
            else:
                return False
    except Exception:
        return False
        
    return True

def conditions(witness):
    if isinstance(witness, dict):
        F = witness.get('F')
        K = witness.get('K')
        sigma = witness.get('sigma')
    elif hasattr(witness, 'F') and hasattr(witness, 'K') and hasattr(witness, 'sigma'):
        F = witness.F
        K = witness.K
        sigma = witness.sigma
    else:
        try:
            F, K, sigma = witness
        except Exception:
            return [False, False, False, False]
            
    # H1: F is a field
    try:
        h1 = is_field(F)
    except Exception:
        h1 = False
        
    # H2: K is an algebraic closure of F
    try:
        h2 = is_alg_closure(K, F)
    except Exception:
        h2 = False
        
    # H3: sigma(a) = a for all a in F
    try:
        h3 = check_sigma_fixes_F(sigma, F)
    except Exception:
        h3 = False
        
    # neg_Q: sigma is NOT a field automorphism of K
    try:
        neg_q = not check_is_automorphism(sigma, K)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is an algebraic closure of F",
    "H_3: σ(a) = a for all elements a in F",
    "¬Q: σ is not a field automorphism of K"
]

N_HYP = 3
NEG_Q_INDEX = 3