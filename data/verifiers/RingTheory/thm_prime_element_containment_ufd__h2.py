import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.abc import x, y, z

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

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: P is not the zero ideal",
    "¬Q: P does not contain a prime element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, (list, tuple, set)):
            if len(witness) == 0:
                g = 0
            else:
                g = list(witness)[0]
                for x_gen in list(witness)[1:]:
                    g = sympy.gcd(g, x_gen)
        else:
            g = witness

        if isinstance(g, (int, sympy.Integer)):
            h1 = True
            h2 = (g != 0)
            val = abs(int(g))
            # In ZZ, an ideal (g) contains a prime iff g divides a prime.
            # This happens iff |g| == 1 (divides all primes) or |g| is prime.
            contains_prime = (val == 1) or sympy.isprime(val)
            neg_q = not contains_prime
            return [h1, h2, neg_q]
            
        elif isinstance(g, sympy.Expr):
            free_symbols = g.free_symbols
            if len(free_symbols) > 1:
                return [False, False, False]
                
            h1 = True
            h2 = (g != 0)
            
            poly_g = sympy.Poly(g)
            deg = poly_g.degree()
            
            # In QQ[x], an ideal (g) contains a prime (irreducible) iff g divides an irreducible.
            # This happens iff g is a unit (degree 0) or g is irreducible itself.
            if deg == 0 and g != 0:
                contains_prime = True
            elif deg > 0:
                factors = sympy.factor_list(g)[1]
                if len(factors) == 1 and factors[0][1] == 1:
                    contains_prime = True
                else:
                    contains_prime = False
            else:
                contains_prime = False
                
            neg_q = not contains_prime
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [False, False, False]