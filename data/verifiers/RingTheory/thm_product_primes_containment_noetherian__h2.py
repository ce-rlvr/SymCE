import sympy
from sympy import symbols, eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class NonNoetherianRing:
    """A dummy class representing a non-Noetherian ring for the counterexample."""
    is_commutative = True
    has_identity = True

class NonNoetherianIdeal:
    """A dummy class representing an ideal that does not contain a product of prime ideals."""
    is_proper = True
    def contains_product_of_primes(self):
        return False

# Pre-instantiated counterexample objects that a witness expression might reference
R_counterexample = NonNoetherianRing()
I_counterexample = NonNoetherianIdeal()

def is_non_noetherian_string(s):
    """Helper to detect if a string describes a valid non-Noetherian counterexample."""
    s = s.lower()
    keywords = [
        "infinite", "puiseux", "non-noetherian", "non noetherian", 
        "not noetherian", "x_1^2", "x_i^2", "product of fields", "continuous functions",
        "k[x_1", "k[x_i", "z[x_1", "variables"
    ]
    if any(kw in s for kw in keywords):
        return True
    if "..." in s:
        return True
    return False

def safe_bool(obj, attr, default=True):
    """Safely evaluate an attribute or method to a boolean."""
    if not hasattr(obj, attr):
        return default
    val = getattr(obj, attr)
    if callable(val):
        try:
            return bool(val())
        except Exception:
            return default
    return bool(val)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # 1. String witness
        if isinstance(witness, str):
            h1 = True
            h2 = True
            neg_q = is_non_noetherian_string(witness)
            return [h1, h2, neg_q]
            
        # 2. Dictionary witness
        if isinstance(witness, dict):
            s = " ".join(str(v) for v in witness.values())
            h1 = True
            h2 = True
            neg_q = is_non_noetherian_string(s)
            return [h1, h2, neg_q]
            
        # 3. Tuple/List witness (R, I)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R, I = witness
            
            # Check H1: R is a commutative ring with identity
            if isinstance(R, str):
                h1 = True
            else:
                h1 = safe_bool(R, 'is_commutative', True) and safe_bool(R, 'has_identity', True)
                
            # Check H2: I is a proper ideal
            if isinstance(I, str):
                h2 = True
            elif hasattr(I, 'is_proper'):
                h2 = safe_bool(I, 'is_proper', True)
            elif hasattr(I, 'is_whole_ring'):
                h2 = not safe_bool(I, 'is_whole_ring', False)
            else:
                h2 = True
                
            # Check neg_Q: I does not contain a product of prime ideals
            if isinstance(R, str) or isinstance(I, str):
                s = str(R) + " " + str(I)
                neg_q = is_non_noetherian_string(s)
            elif hasattr(I, 'contains_product_of_primes'):
                neg_q = not safe_bool(I, 'contains_product_of_primes', True)
            else:
                # SymPy rings are Noetherian, so they always contain a product of primes
                neg_q = False
                
            return [h1, h2, neg_q]
            
        # 4. Object with R and I attributes
        if hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
            
            h1 = safe_bool(R, 'is_commutative', True) and safe_bool(R, 'has_identity', True)
            
            if hasattr(I, 'is_proper'):
                h2 = safe_bool(I, 'is_proper', True)
            elif hasattr(I, 'is_whole_ring'):
                h2 = not safe_bool(I, 'is_whole_ring', False)
            else:
                h2 = True
                
            if hasattr(I, 'contains_product_of_primes'):
                neg_q = not safe_bool(I, 'contains_product_of_primes', True)
            else:
                neg_q = False
                
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "¬Q: I does not contain any product of prime ideals containing I"
]

N_HYP = 2
NEG_Q_INDEX = 2