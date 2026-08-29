import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy import isprime

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

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a tuple (F, p) where F is the field size (a prime n)
        # and p is the exponent in the map phi(x) = x^p.
        if hasattr(witness, '__iter__') and not isinstance(witness, str):
            witness_list = list(witness)
            if len(witness_list) != 2:
                return [False, False]
            n_obj, p_obj = witness_list
        else:
            return [False, False]
            
        # Extract the integer size of the field
        if hasattr(n_obj, 'order'):
            n = int(n_obj.order)
        elif hasattr(n_obj, 'mod'):
            n = int(n_obj.mod)
        else:
            n = int(n_obj)
            
        p = int(p_obj)
        
        # Limit size to prevent timeout during evaluation
        if n > 2000 or n < 2:
            return [False, False]
            
    except Exception:
        return [False, False]
        
    # H_1: F is a finite field
    # We restrict to prime fields Z/nZ for simplicity, which are fields iff n is prime.
    try:
        h1 = isprime(n)
    except Exception:
        h1 = False
        
    # neg_Q: The map phi(x) = x^p is NOT a field automorphism of F
    try:
        is_auto = True
        if p < 0:
            is_auto = False
        else:
            # Check bijection
            mapped = set(pow(x, p, n) for x in range(n))
            if len(mapped) != n:
                is_auto = False
            
            # Check addition preservation: phi(x + y) == phi(x) + phi(y)
            if is_auto:
                for x in range(n):
                    for y in range(n):
                        if pow(x + y, p, n) != (pow(x, p, n) + pow(y, p, n)) % n:
                            is_auto = False
                            break
                    if not is_auto:
                        break
            
            # Check multiplication preservation: phi(x * y) == phi(x) * phi(y)
            if is_auto:
                for x in range(n):
                    for y in range(n):
                        if pow(x * y, p, n) != (pow(x, p, n) * pow(y, p, n)) % n:
                            is_auto = False
                            break
                    if not is_auto:
                        break
                        
        neg_q = not is_auto
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "¬Q: The map phi(x) = x^p is not a field automorphism of F"
]

N_HYP = 1
NEG_Q_INDEX = 1