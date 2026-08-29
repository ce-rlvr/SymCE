import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
import math

# Top-level setup for potential witness expressions
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def check_rZ(r, m, n):
    """
    Evaluates the conditions for a ring without identity of the form R = rZ,
    with ideal M = mZ, and power n.
    """
    try:
        r = abs(int(r))
        m = abs(int(m))
        n = int(n)
        if r == 0 or n <= 0:
            return [False, False, False]
        
        # H1: rZ is always a commutative Noetherian ring
        h1 = True
        
        # H2: M is a maximal ideal of R
        # mZ is a maximal ideal in rZ iff m is a proper multiple of r and m/r is prime
        if m == 0 or m <= r or m % r != 0:
            h2 = False
        else:
            h2 = sympy.ntheory.isprime(m // r)
            
        # Conclusion: M^n is M-primary
        mn = m**n
        
        # Calculate the radical of M^n in R
        rad_m = 1
        for p in sympy.ntheory.primefactors(m):
            rad_m *= p
            
        radical_val = abs(r * rad_m) // math.gcd(r, rad_m)
        
        # An ideal is M-primary if its radical is M and it is primary
        if radical_val != m:
            is_M_primary = False
        else:
            # Check if mn Z is primary in rZ
            K = mn // math.gcd(mn, r**2)
            rad_a = radical_val // r
            target_b = mn // math.gcd(mn, r)
            is_M_primary = True
            
            # Iterate over divisors to check the primary condition efficiently
            for d in sympy.ntheory.divisors(K):
                if d % rad_a != 0:
                    b = K // d
                    if b % target_b != 0:
                        is_M_primary = False
                        break
                        
        return [h1, h2, not is_M_primary]
    except Exception:
        return [False, False, False]

def conditions(witness) -> list[bool]:
    # 1. Try integer tuple/list (r, m, n) representing R = rZ, M = mZ, power = n
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            r, m, n = witness
            if isinstance(r, int) and isinstance(m, int) and isinstance(n, int):
                return check_rZ(r, m, n)
    except Exception:
        pass

    # 2. Try object with attributes
    try:
        r = witness.R
        m = witness.M
        n = witness.n
        if isinstance(r, int) and isinstance(m, int) and isinstance(n, int):
            return check_rZ(r, m, n)
    except Exception:
        pass

    # 3. Try dictionary
    try:
        if isinstance(witness, dict):
            r = witness['R']
            m = witness['M']
            n = witness['n']
            if isinstance(r, int) and isinstance(m, int) and isinstance(n, int):
                return check_rZ(r, m, n)
    except Exception:
        pass

    # 4. Generic object with methods (duck typing for custom ring objects)
    h1 = False
    try:
        h1 = bool(witness.is_commutative() and witness.is_noetherian())
    except Exception:
        pass

    h2 = False
    try:
        h2 = bool(witness.is_maximal_ideal(witness.M))
    except Exception:
        pass

    neg_q = False
    try:
        Mn = witness.ideal_power(witness.M, witness.n)
        is_primary = witness.is_primary_ideal(Mn)
        radical_Mn = witness.radical(Mn)
        is_M_primary = is_primary and (radical_Mn == witness.M)
        neg_q = not is_M_primary
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is a maximal ideal of R",
    "¬Q: The ideal power M^n is not an M-primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2