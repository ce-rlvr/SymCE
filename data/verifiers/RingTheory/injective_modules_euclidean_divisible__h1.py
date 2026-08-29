import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: M is an injective module over R",
    "¬Q: M is not a divisible module"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the conjecture:
    "Let M be an injective module over R. Then M is a divisible module."
    
    The conjecture is false because the hypothesis "R is a Euclidean domain" (or PID) 
    was dropped. Over rings with zero divisors (like Z/nZ for composite n), 
    an injective module is not necessarily divisible (where divisible means rM = M for all r != 0).
    """
    try:
        import sympy
        
        def extract_n(obj):
            if hasattr(obj, 'is_Matrix') and obj.is_Matrix:
                return None
            if hasattr(obj, 'order'):
                return int(obj.order())
            if isinstance(obj, int):
                return obj
            s = str(obj)
            digits = []
            for c in s:
                if c.isdigit():
                    digits.append(c)
                elif digits:
                    break
            if digits:
                return int("".join(digits))
            return None

        # We interpret the witness as representing the ring R = Z/nZ and module M = Z/nZ.
        if isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) >= 2:
                n_R = extract_n(witness[0])
                n_M = extract_n(witness[1])
                # We only evaluate the simple case where R and M are the same Z/nZ
                if n_R is None or n_M is None or n_R != n_M:
                    return [False, False]
            n = extract_n(witness[0])
        else:
            n = extract_n(witness)
            
        if n is None or n <= 1:
            return [False, False]
            
        # H_1: M is an injective module over R.
        # Z/nZ is a quasi-Frobenius ring, so it is self-injective for any n > 1.
        h1_ok = True
        
        # ¬Q: M is not a divisible module.
        # A module M over R is divisible if rM = M for all r != 0.
        # For M = Z/nZ over R = Z/nZ, rM = M iff gcd(r, n) == 1.
        # So M is divisible iff all 0 < r < n are coprime to n, which means n is prime.
        # Thus, M is NOT divisible iff n is composite.
        neg_q_ok = not sympy.isprime(n)
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]