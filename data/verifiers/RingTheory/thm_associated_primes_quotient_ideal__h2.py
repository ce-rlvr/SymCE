import sympy
from sympy import S, FiniteSet, ImageSet, Lambda
from sympy.abc import x
from sympy.ntheory import primefactors

# Top-level setup
# Use these standard rings and modules for the witness
ZZ = S.Integers
QQ = S.Rationals

def Z_ideal(n):
    """Returns the ideal n*ZZ. Use this to construct ideals of ZZ."""
    if n == 0:
        return FiniteSet(0)
    if n == 1 or n == -1:
        return S.Integers
    return ImageSet(Lambda(x, n*x), S.Integers)

def get_n(S_obj):
    if S_obj == FiniteSet(0) or S_obj == 0 or S_obj == '0':
        return 0
    if S_obj == S.Integers or S_obj == 'ZZ':
        return 1
    if isinstance(S_obj, ImageSet):
        try:
            val = S_obj.lamda(1)
            if not val.is_Integer:
                return None
            return abs(int(val))
        except Exception:
            pass
    if isinstance(S_obj, int) or (hasattr(S_obj, 'is_Integer') and S_obj.is_Integer):
        return abs(int(S_obj))
    if isinstance(S_obj, str):
        try:
            return abs(int(S_obj))
        except ValueError:
            pass
    return None

def is_subset(I, J):
    if I == J:
        return True
        
    if J == S.Rationals or J == 'QQ':
        if I == S.Rationals or I == 'QQ': return True
        if get_n(I) is not None: return True
        return False
        
    n_I = get_n(I)
    n_J = get_n(J)
    
    if n_I is not None and n_J is not None:
        if n_J == 0:
            return n_I == 0
        if n_I == 0:
            return True
        return n_I % n_J == 0
        
    try:
        res = I.is_subset(J)
        if res is True: return True
        if res is False: return False
    except Exception:
        pass
        
    return False

def get_ass_primes_ZZ(M_num, M_den):
    if M_num == M_den:
        return set()
        
    if not is_subset(M_den, M_num):
        raise ValueError("Denominator is not a subset of numerator")
        
    n_num = get_n(M_num)
    n_den = get_n(M_den)
    
    if M_num == S.Rationals or M_num == 'QQ':
        if n_den == 0:
            return {0}
        if n_den is not None and n_den > 0:
            return 'ALL_PRIMES'
            
    if n_num is not None and n_den is not None:
        if n_den == 0:
            if n_num == 0:
                return set()
            else:
                return {0}
        else:
            val = n_den // n_num
            if val == 1:
                return set()
            return set(primefactors(val))
            
    raise ValueError("Unsupported module")

def normalize(obj):
    if obj == 'ZZ': return S.Integers
    if obj == 'QQ': return S.Rationals
    if obj == '0': return FiniteSet(0)
    return obj

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, I, J = witness
    except Exception:
        return [False, False, False]
        
    try:
        R = normalize(R)
        I = normalize(I)
        J = normalize(J)
    except Exception:
        pass
        
    # H1: R is a commutative Noetherian ring
    try:
        # We restrict the verifier to ZZ for simplicity and robustness
        h1 = (R == S.Integers)
    except Exception:
        h1 = False
        
    # H2: I is a subset of J
    try:
        h2 = is_subset(I, J)
    except Exception:
        h2 = False
        
    # neg_Q: Ass(J/I) is not a subset of Ass(R/I)
    try:
        ass_JI = get_ass_primes_ZZ(J, I)
        ass_RI = get_ass_primes_ZZ(R, I)
        
        if ass_JI == 'ALL_PRIMES':
            if ass_RI == 'ALL_PRIMES':
                neg_q = False
            else:
                neg_q = True
        else:
            if ass_RI == 'ALL_PRIMES':
                neg_q = False
            else:
                neg_q = not ass_JI.issubset(ass_RI)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: I is a subset of J",
    "¬Q: Ass(J/I) is not a subset of Ass(R/I)"
]

N_HYP = 2
NEG_Q_INDEX = 2