import sympy
from sympy import S
import sympy.abc
import itertools
import functools
import math

# Top-level setup for Ring/Field domain
ZZ = sympy.ZZ
QQ = sympy.QQ
Integers = sympy.S.Integers
Rationals = sympy.S.Rationals
Reals = sympy.S.Reals

def is_integral_domain_general(S_obj):
    """
    Checks if S_obj is an integral domain.
    Returns True for known sympy domains, otherwise attempts to verify
    the ring axioms and lack of zero divisors for a finite set.
    """
    if S_obj is ZZ or S_obj is QQ:
        return True
    if S_obj is Integers or S_obj is Rationals or S_obj is Reals:
        return True
    if hasattr(S_obj, 'is_IntegralDomain') and S_obj.is_IntegralDomain:
        return True
    
    try:
        S_list = []
        if hasattr(S_obj, '__iter__'):
            for i, x in enumerate(S_obj):
                if i > 1000:
                    return False  # Too large to exhaustively check here
                S_list.append(x)
        else:
            return False
            
        if not S_list: 
            return False
        
        # Find additive identity (zero)
        zeros = []
        for z in S_list:
            is_zero = True
            for a in S_list:
                try:
                    if (z + a) not in S_list or (z + a) != a:
                        is_zero = False
                        break
                except Exception:
                    is_zero = False
                    break
            if is_zero:
                zeros.append(z)
                
        if not zeros: 
            return False
        zero = zeros[0]
        
        # Find multiplicative identity (one)
        ones = []
        for u in S_list:
            is_one = True
            for a in S_list:
                try:
                    if (u * a) not in S_list or (u * a) != a:
                        is_one = False
                        break
                except Exception:
                    is_one = False
                    break
            if is_one:
                ones.append(u)
                
        if not ones: 
            return False
        one = ones[0]
        
        if zero == one: 
            return False
        
        # Check closure, commutativity, and no zero divisors
        for a in S_list:
            for b in S_list:
                try:
                    if (a + b) not in S_list: return False
                    if (a - b) not in S_list: return False
                    if (a * b) not in S_list: return False
                    if a * b != b * a: return False
                    if a + b != b + a: return False
                    if (a * b) == zero and a != zero and b != zero:
                        return False
                except Exception:
                    return False
        return True
    except Exception:
        return False

def get_mult_identity(R):
    """
    Attempts to find the multiplicative identity of R.
    """
    if R is ZZ or R is QQ or R is Integers or R is Rationals or R is Reals:
        return 1
    if hasattr(R, 'one'):
        return R.one
    
    try:
        R_list = []
        if hasattr(R, '__iter__'):
            for i, x in enumerate(R):
                if i > 1000:
                    break
                R_list.append(x)
                
        for u in R_list:
            is_one = True
            for a in R_list:
                try:
                    if (u * a) not in R_list or (u * a) != a:
                        is_one = False
                        break
                except Exception:
                    is_one = False
                    break
            if is_one:
                return u
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    The witness is expected to be a tuple (R, S) where R is the integral domain
    and S is the subset. If only S is provided, R defaults to ZZ.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S_set = witness
        else:
            R = ZZ
            S_set = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is an integral domain
    try:
        h1 = is_integral_domain_general(R)
    except Exception:
        h1 = False
        
    # H_2: S contains the multiplicative identity of R
    try:
        one_R = get_mult_identity(R)
        if one_R is None:
            h2 = False
        else:
            h2 = False
            try:
                if hasattr(S_set, '__contains__'):
                    if (one_R in S_set) is True:
                        h2 = True
            except Exception:
                pass
            
            if not h2 and hasattr(S_set, '__iter__'):
                try:
                    for x in S_set:
                        if x == one_R:
                            h2 = True
                            break
                except Exception:
                    pass
    except Exception:
        h2 = False
        
    # ¬Q: S is NOT an integral domain
    try:
        neg_q = not is_integral_domain_general(S_set)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: S contains the multiplicative identity of R",
    "¬Q: S is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2