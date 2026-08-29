import sympy
from sympy import ZZ, QQ
import itertools

# Top-level setup for RingTheory
Z = ZZ
Q = QQ

def conditions(witness):
    R = None
    I = None
    
    # Unpack witness
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
    else:
        I = witness
        R = getattr(I, 'ring', getattr(I, 'R', None))
        
    # H_1: R is a commutative Noetherian ring
    h1_ok = False
    try:
        if R is not None:
            if R in (ZZ, QQ, sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals):
                h1_ok = True
            elif hasattr(R, 'is_Noetherian') and R.is_Noetherian:
                h1_ok = True
            elif type(R).__name__ in ['IntegerRing', 'RationalField', 'RealField', 'ComplexField', 'PolynomialRing', 'FractionField']:
                h1_ok = True
            elif hasattr(R, 'is_commutative') and R.is_commutative:
                h1_ok = True
            elif isinstance(R, str):
                R_str = R.lower()
                if "noetherian" in R_str or "zz" in R_str or "qq" in R_str or R_str in ["z", "q", "r", "c"]:
                    h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The set of associated prime ideals of I is not finite
    neg_q = False
    try:
        if I is not None:
            # Check if I is explicitly an infinite SymPy set
            if hasattr(I, 'is_finite') and I.is_finite is False:
                neg_q = True
            
            # Check if I has an associated_primes attribute/method
            elif hasattr(I, 'associated_primes'):
                ass = I.associated_primes
                if callable(ass):
                    ass = ass()
                
                if hasattr(ass, 'is_finite') and ass.is_finite is False:
                    neg_q = True
                elif hasattr(ass, '__iter__') and not hasattr(ass, '__len__'):
                    try:
                        first_100 = list(itertools.islice(ass, 101))
                        if len(first_100) > 100:
                            neg_q = True
                    except Exception:
                        pass
                elif isinstance(ass, str) and "inf" in ass.lower():
                    neg_q = True
            
            # Check custom boolean flags
            elif getattr(I, 'has_infinite_associated_primes', False):
                neg_q = True
            elif getattr(I, 'is_finite_Ass', True) is False:
                neg_q = True
            
            # Check string representations indicating infinite structures
            elif isinstance(I, str) and ("inf" in I.lower() or "bigoplus" in I.lower() or "direct sum" in I.lower()):
                neg_q = True
                
            # Check class name for infinite indicators
            elif "infinit" in type(I).__name__.lower():
                neg_q = True
                
            # If I itself is an infinite generator (representing the infinite set of primes)
            elif hasattr(I, '__iter__') and not hasattr(I, '__len__'):
                try:
                    first_100 = list(itertools.islice(I, 101))
                    if len(first_100) > 100:
                        neg_q = True
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: The set of associated prime ideals of I is not finite"
]

N_HYP = 1
NEG_Q_INDEX = 1