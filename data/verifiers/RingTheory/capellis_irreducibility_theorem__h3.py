import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
from sympy import QQ, ZZ
from sympy.abc import x, y, z, t
import math
from functools import reduce

# Top-level setup
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

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def check_H1(F):
    try:
        return hasattr(F, 'is_Field') and F.is_Field
    except Exception:
        return False

def check_H2(F, a):
    try:
        if a == 0:
            return False
        if F == QQ:
            sympy.Rational(a)
            return True
        elif hasattr(F, 'characteristic'):
            F(a)
            return True
        return False
    except Exception:
        return False

def check_H3(F, a, n):
    try:
        if not isinstance(n, (int, sympy.Integer)):
            return False
        if a == 0:
            return False
        if n == 0:
            if F == QQ:
                num, den = sympy.Rational(a).as_numer_denom()
                factors = sympy.factorint(abs(num))
                factors.update(sympy.factorint(abs(den)))
                if not factors:
                    return False
                g = reduce(math.gcd, factors.values())
                if a < 0:
                    return (g & (g - 1)) == 0
                else:
                    return g == 1
            else:
                return False
        else:
            primes = sympy.primefactors(abs(n))
            for p in primes:
                if F == QQ:
                    num, den = sympy.Rational(a).as_numer_denom()
                    factors = sympy.factorint(abs(num))
                    factors.update(sympy.factorint(abs(den)))
                    if not factors:
                        if a == 1:
                            return False
                        if a == -1 and p != 2:
                            return False
                        continue
                    is_pth = True
                    for prime, exp in factors.items():
                        if exp % p != 0:
                            is_pth = False
                            break
                    if is_pth:
                        if a < 0 and p == 2:
                            is_pth = False
                    if is_pth:
                        return False
                elif hasattr(F, 'characteristic'):
                    char = F.characteristic()
                    if p == char:
                        return False
                    if hasattr(F, 'order') and F.order == char:
                        q = char
                        d = sympy.gcd(p, q - 1)
                        val = int(a) % q
                        if pow(val, (q - 1) // d, q) == 1:
                            return False
                    else:
                        return False
                else:
                    return False
            return True
    except Exception:
        return False

def check_H4(F, a, n):
    try:
        if not isinstance(n, (int, sympy.Integer)):
            return False
        if a == 0:
            return False
        if n % 4 != 0:
            return True
        if F == QQ:
            val = sympy.Rational(a) / -4
            if val < 0:
                return True
            if val == 0:
                return True
            num, den = val.as_numer_denom()
            factors = sympy.factorint(abs(num))
            factors.update(sympy.factorint(abs(den)))
            for prime, exp in factors.items():
                if exp % 4 != 0:
                    return True
            return False
        elif hasattr(F, 'characteristic'):
            char = F.characteristic()
            if char == 2:
                return True
            if hasattr(F, 'order') and F.order == char:
                q = char
                val = (int(a) * pow(-4, q - 2, q)) % q
                if val == 0:
                    return True
                d = sympy.gcd(4, q - 1)
                if pow(val, (q - 1) // d, q) == 1:
                    return False
                return True
            else:
                return False
        else:
            return False
    except Exception:
        return False

def check_neg_Q(F, a, n):
    try:
        if not isinstance(n, (int, sympy.Integer)):
            return False
        if n == 0:
            return True
        if n < 0:
            return True
        if n == 1:
            return False
        
        x_sym = sympy.Symbol('x')
        poly = x_sym**n - a
        
        if F == QQ:
            factors = sympy.factor_list(poly, domain='QQ')
            if len(factors[1]) == 1 and factors[1][0][1] == 1:
                return False
            else:
                return True
        elif hasattr(F, 'characteristic'):
            char = F.characteristic()
            factors = sympy.factor_list(poly, modulus=char)
            if len(factors[1]) == 1 and factors[1][0][1] == 1:
                return False
            else:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F', QQ)
            a = witness.get('a')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) == 3:
            F, a, n = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            a, n = witness
            F = QQ
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    h1 = check_H1(F)
    h2 = check_H2(F, a)
    h3 = check_H3(F, a, n)
    h4 = check_H4(F, a, n)
    neg_q = check_neg_Q(F, a, n)

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: a is a non-zero element of F",
    "H_3: For every prime number p dividing n, there is no element b in F such that b^p = a",
    "H_4: If 4 divides n, there is no element c in F such that a = -4c^4",
    "¬Q: The polynomial x^n - a is reducible over F"
]

N_HYP = 4
NEG_Q_INDEX = 4