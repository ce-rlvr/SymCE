import sympy
from sympy import gcd, sympify, groebner, ZZ, QQ
from functools import reduce
from sympy.abc import x, y, z

def to_expr(k):
    if hasattr(k, 'as_expr'):
        return k.as_expr()
    return sympify(k)

def is_proper(K):
    if not K:
        return True
        
    try:
        exprs = [to_expr(k) for k in K]
    except Exception:
        return False
    
    # If all expressions are numbers (e.g., integers, rationals)
    if all(e.is_number for e in exprs):
        try:
            g = reduce(gcd, exprs)
            if g == 0:
                return True
            if g.is_Integer:
                return abs(g) != 1
            if g.is_Rational:
                return g == 0
            return g != 1 and g != -1
        except Exception:
            pass

    # For polynomials, use Groebner basis to check if ideal is proper
    try:
        gb = groebner(exprs)
        # If the Groebner basis contains exactly one element which is a unit, it's not proper.
        if len(gb) == 1:
            g = gb[0]
            if g.is_number:
                if g.is_Integer:
                    return abs(g) != 1
                if g.is_Rational:
                    return g == 0
                return g != 1 and g != -1
        return True
    except Exception:
        pass

    # Fallback to gcd if groebner fails
    try:
        g = reduce(gcd, exprs)
        if g == 0:
            return True
        if g.is_Integer:
            return abs(g) != 1
        if g.is_Rational:
            return g == 0
        if hasattr(g, 'as_poly'):
            p = g.as_poly()
            if p is not None:
                return p.degree() > 0
        return g != 1 and g != -1
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (I, J) or (R, I, J) where I and J are lists of generators for the ideals.
    """
    try:
        if len(witness) == 3:
            R, I, J = witness
        elif len(witness) == 2:
            I, J = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        if hasattr(I, 'gens'):
            I_list = list(I.gens)
        elif isinstance(I, (list, tuple, set)):
            I_list = list(I)
        else:
            I_list = [I]
            
        if hasattr(J, 'gens'):
            J_list = list(J.gens)
        elif isinstance(J, (list, tuple, set)):
            J_list = list(J)
        else:
            J_list = [J]
    except Exception:
        return [False, False]
        
    try:
        h1 = is_proper(I_list) and is_proper(J_list)
    except Exception:
        h1 = False
        
    try:
        I_plus_J = I_list + J_list
        # The conclusion is that I and J are NOT comaximal (i.e., I + J is a proper ideal).
        # The negation of the conclusion is that I and J ARE comaximal (i.e., I + J is NOT a proper ideal).
        neg_q = not is_proper(I_plus_J)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: I and J are proper ideals",
    "¬Q: I and J are comaximal (I + J = R)"
]

N_HYP = 1
NEG_Q_INDEX = 1