import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    "Coprimality of a Prime and a Non-Multiple in a UFD" (with UFD dropped).
    
    The counterexample is typically found in a ring with zero divisors, 
    such as Z x Z, where p = (0, 1) is prime, a = (2, 0), p does not divide a, 
    but their GCD is (2, 1) != (1, 1).
    """
    # 1. Duck typing for witness with attributes
    try:
        p = witness.p
        a = witness.a
        h1 = witness.is_prime(p)
        h2 = (a != witness.zero) and not witness.divides(p, a)
        
        try:
            if hasattr(witness, 'is_gcd_one'):
                neg_q = not witness.is_gcd_one(p, a)
            else:
                g = witness.gcd(p, a)
                neg_q = (g != witness.one)
        except Exception:
            # If gcd doesn't exist, then it is not 1.
            neg_q = True
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 2. Tuple (Ring, p, a)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, p, a = witness
            h1 = R.is_prime(p)
            h2 = (a != R.zero) and not R.divides(p, a)
            try:
                if hasattr(R, 'is_gcd_one'):
                    neg_q = not R.is_gcd_one(p, a)
                else:
                    g = R.gcd(p, a)
                    neg_q = (g != R.one)
            except Exception:
                neg_q = True
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 3. Z x Z representation: witness = ((p1, p2), (a1, a2))
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, a = witness
            if isinstance(p, tuple) and isinstance(a, tuple) and len(p) == 2 and len(a) == 2:
                p1, p2 = p
                a1, a2 = a
                
                # H1: p is a prime element
                is_zero = (p1 == 0 and p2 == 0)
                is_unit = (abs(p1) == 1 and abs(p2) == 1)
                
                def is_prime_ideal_gen(x):
                    return x == 0 or sympy.isprime(abs(x))
                    
                # In Z x Z, an element is prime iff one component generates a prime ideal 
                # and the other is a unit.
                h1_1 = is_prime_ideal_gen(p1) and abs(p2) == 1
                h1_2 = abs(p1) == 1 and is_prime_ideal_gen(p2)
                h1 = not is_zero and not is_unit and (h1_1 or h1_2)
                
                # H2: a != 0 and p does not divide a
                a_not_zero = (a1 != 0 or a2 != 0)
                p_div_a = (a1 % p1 == 0 if p1 != 0 else a1 == 0) and \
                          (a2 % p2 == 0 if p2 != 0 else a2 == 0)
                h2 = a_not_zero and not p_div_a
                
                # neg_Q: gcd(p, a) != 1
                # In Z x Z, 1 is (1, 1). The GCD is computed component-wise.
                g1 = math.gcd(p1, a1)
                g2 = math.gcd(p2, a2)
                neg_q = not (g1 == 1 and g2 == 1)
                
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 4. Z representation (integers): witness = (p, a)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, a = witness
            if isinstance(p, int) and isinstance(a, int):
                h1 = sympy.isprime(abs(p))
                h2 = (a != 0) and (a % p != 0 if p != 0 else a != 0)
                neg_q = math.gcd(p, a) != 1
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: p is a prime element",
    "H_2: a is non-zero and p does not divide a",
    "¬Q: The greatest common divisor of p and a is not 1"
]

N_HYP = 2
NEG_Q_INDEX = 2