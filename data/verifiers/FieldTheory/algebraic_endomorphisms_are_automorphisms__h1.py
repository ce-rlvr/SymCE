import sympy
from sympy import S, Rational, Integer, Symbol, I, simplify, pi, sqrt
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
QQ = S.Rationals
RR = S.Reals
CC = S.Complexes
ZZ = S.Integers

def get_bool_prop(obj, prop_names, *args):
    """Helper to extract boolean properties from dictionaries or objects."""
    if isinstance(obj, dict):
        for name in prop_names:
            if name in obj:
                val = obj[name]
                try:
                    return val(*args) if callable(val) else val
                except Exception:
                    pass
    else:
        for name in prop_names:
            if hasattr(obj, name):
                val = getattr(obj, name)
                try:
                    return val(*args) if callable(val) else val
                except Exception:
                    pass
    return None

def check_H1(w):
    res = get_bool_prop(w, [
        'is_algebraic_closure',
        'K_is_algebraic_closure_of_F',
        'is_algebraic_closure_of_F',
        'H1', 'h1', 'H_1', 'h_1'
    ])
    if res is not None: return bool(res)
    
    K, F = None, None
    if hasattr(w, 'K') and hasattr(w, 'F'):
        K, F = w.K, w.F
    elif isinstance(w, (tuple, list)) and len(w) == 3:
        K, F, sigma = w
        
    if K is not None and F is not None:
        res = get_bool_prop(K, ['is_algebraic_closure', 'is_algebraic_closure_of'], F)
        if res is not None: return bool(res)
        
        K_str = str(K)
        F_str = str(F)
        if K_str in ('CC', 'Complexes', 'Complexes()') and F_str in ('RR', 'Reals', 'Reals()'):
            return True
        if K_str in ('QQ_bar', 'AlgebraicNumbers') and F_str in ('QQ', 'Rationals', 'Rationals()'):
            return True
            
    return False

def check_H2(w):
    res = get_bool_prop(w, [
        'is_field_homomorphism',
        'sigma_is_field_homomorphism',
        'is_homomorphism',
        'H2', 'h2', 'H_2', 'h_2'
    ])
    if res is not None: return bool(res)
    
    K, sigma = None, None
    if hasattr(w, 'sigma') and hasattr(w, 'K'):
        K, sigma = w.K, w.sigma
    elif isinstance(w, (tuple, list)) and len(w) == 3:
        K, F, sigma = w
        
    if sigma is not None and K is not None:
        res = get_bool_prop(sigma, ['is_homomorphism', 'is_field_homomorphism'], K, K)
        if res is not None: return bool(res)
        
        if callable(sigma):
            try:
                vals = [1 + 2*I, -3 + 4*I, I, 2]
                for a in vals:
                    for b in vals:
                        if simplify(sigma(a + b) - (sigma(a) + sigma(b))) != 0:
                            return False
                        if simplify(sigma(a * b) - (sigma(a) * sigma(b))) != 0:
                            return False
                if simplify(sigma(1) - 1) != 0:
                    return False
                return True
            except Exception:
                pass
                
    return False

def check_H3(w):
    res = get_bool_prop(w, [
        'fixes_F',
        'sigma_fixes_F',
        'fixes',
        'H3', 'h3', 'H_3', 'h_3'
    ])
    if res is not None: return bool(res)
    
    F, sigma = None, None
    if hasattr(w, 'sigma') and hasattr(w, 'F'):
        F, sigma = w.F, w.sigma
    elif isinstance(w, (tuple, list)) and len(w) == 3:
        K, F, sigma = w
        
    if sigma is not None and F is not None:
        res = get_bool_prop(sigma, ['fixes', 'fixes_field'], F)
        if res is not None: return bool(res)
        
        if callable(sigma):
            try:
                F_str = str(F)
                if F_str in ('RR', 'Reals', 'Reals()'):
                    vals = [1, -2, pi, sqrt(2)]
                elif F_str in ('QQ', 'Rationals', 'Rationals()'):
                    vals = [1, -2, Rational(1, 2), Rational(-3, 4)]
                else:
                    vals = [1, 0]
                for a in vals:
                    if simplify(sigma(a) - a) != 0:
                        return False
                return True
            except Exception:
                pass
                
    return False

def check_neg_Q(w):
    res = get_bool_prop(w, ['neg_Q', 'neg_q'])
    if res is not None: return bool(res)
    
    res = get_bool_prop(w, [
        'is_field_automorphism',
        'sigma_is_field_automorphism',
        'is_automorphism',
        'Q', 'q'
    ])
    if res is not None: return not bool(res)
    
    K, F, sigma = None, None, None
    if hasattr(w, 'sigma') and hasattr(w, 'K'):
        K, sigma = w.K, w.sigma
        if hasattr(w, 'F'):
            F = w.F
    elif isinstance(w, (tuple, list)) and len(w) == 3:
        K, F, sigma = w
        
    if sigma is not None and K is not None:
        res = get_bool_prop(sigma, ['is_automorphism'], K)
        if res is not None: return not bool(res)
        
        if callable(sigma):
            K_str = str(K)
            F_str = str(F)
            if K_str in ('CC', 'Complexes', 'Complexes()') and F_str in ('RR', 'Reals', 'Reals()'):
                return False
            if K_str in ('QQ_bar', 'AlgebraicNumbers') and F_str in ('QQ', 'Rationals', 'Rationals()'):
                return False
                
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(witness)
    except Exception:
        h2 = False
        
    try:
        h3 = check_H3(witness)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraic closure of F",
    "H_2: σ: K → K is a field homomorphism",
    "H_3: σ(a) = a for all elements a in F",
    "¬Q: σ is not a field automorphism of K"
]

N_HYP = 3
NEG_Q_INDEX = 3