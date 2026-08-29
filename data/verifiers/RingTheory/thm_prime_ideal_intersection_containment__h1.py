import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: I and J are ideals of R",
    "H_3: The intersection I \\cap J is contained in P",
    "¬Q: I is not contained in P and J is not contained in P"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # 1. Dictionary or Object with explicit finite ring structure
        if isinstance(witness, dict) and 'R' in witness:
            R = witness['R']
            P = witness['P']
            I = witness['I']
            J = witness['J']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
        elif hasattr(witness, 'R') and hasattr(witness, 'P') and hasattr(witness, 'add'):
            R = witness.R
            P = witness.P
            I = witness.I
            J = witness.J
            add = witness.add
            mul = witness.mul
            zero = witness.zero
        # 2. Tuple of 3 integers (representing ideals in Z)
        elif isinstance(witness, tuple) and len(witness) == 3 and all(isinstance(a, int) for a in witness):
            p, i, j = witness
            h1 = sympy.isprime(p) or p == 0
            h2 = True
            lcm_ij = abs(i * j) // math.gcd(i, j) if i and j else 0
            h3 = (lcm_ij % p == 0) if p != 0 else (lcm_ij == 0)
            i_in_p = (i % p == 0) if p != 0 else (i == 0)
            j_in_p = (j % p == 0) if p != 0 else (j == 0)
            neg_q = not (i_in_p or j_in_p)
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
        # 3. Tuple of 3 SymPy ideals
        elif isinstance(witness, tuple) and len(witness) == 3 and hasattr(witness[0], 'is_prime'):
            P, I, J = witness
            h1 = bool(P.is_prime)
            h2 = True
            I_int_J = I.intersect(J)
            h3 = all(P.contains(g) for g in I_int_J.gens)
            i_in_p = all(P.contains(g) for g in I.gens)
            j_in_p = all(P.contains(g) for g in J.gens)
            neg_q = not (i_in_p or j_in_p)
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
        # 4. Tuple of 4 SymPy ideals (R, P, I, J)
        elif isinstance(witness, tuple) and len(witness) == 4 and hasattr(witness[1], 'is_prime'):
            _, P, I, J = witness
            h1 = bool(P.is_prime)
            h2 = True
            I_int_J = I.intersect(J)
            h3 = all(P.contains(g) for g in I_int_J.gens)
            i_in_p = all(P.contains(g) for g in I.gens)
            j_in_p = all(P.contains(g) for g in J.gens)
            neg_q = not (i_in_p or j_in_p)
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
        else:
            return [False, False, False, False]

        # Evaluate for finite ring structure
        def is_ideal(S):
            if zero not in S:
                return False
            for a in S:
                for b in S:
                    if add(a, b) not in S:
                        return False
            for a in S:
                if not any(add(a, b) == zero for b in S):
                    return False
            for r in R:
                for a in S:
                    if mul(r, a) not in S:
                        return False
                    if mul(a, r) not in S:
                        return False
            return True

        def is_prime_ideal(S):
            if not is_ideal(S):
                return False
            if all(x in S for x in R):
                return False  # Prime ideals must be proper
            
            is_comm = all(mul(a, b) == mul(b, a) for a in R for b in R)
            
            if is_comm:
                for a in R:
                    for b in R:
                        if mul(a, b) in S:
                            if a not in S and b not in S:
                                return False
            else:
                for a in R:
                    for b in R:
                        if mul(a, b) in S and all(mul(a, mul(r, b)) in S for r in R):
                            if a not in S and b not in S:
                                return False
            return True

        h1 = is_prime_ideal(P)
        h2 = is_ideal(I) and is_ideal(J)
        
        h3 = all(x in P for x in I if x in J)
        
        i_in_p = all(x in P for x in I)
        j_in_p = all(x in P for x in J)
        neg_q = (not i_in_p) and (not j_in_p)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]