import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
from sympy import isprime, Rational

# Top-level setup
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
    "H_1: p is a prime number",
    "H_2: x is an element of Z_p with valid p-adic digits",
    "¬Q: x is a unit in Z_p iff a_0 != 0 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def p_adic_valuation(x, p):
    if x == 0:
        return float('inf')
    x_rat = Rational(x)
    return sympy.ntheory.multiplicity(p, x_rat.p) - sympy.ntheory.multiplicity(p, x_rat.q)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            if 'a' in witness:
                a = witness['a']
                x = sum(c * (p**i) for i, c in enumerate(a))
                explicit_a = True
            elif 'x' in witness:
                x = witness['x']
                explicit_a = False
            else:
                return [False, False, False]
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 2:
                p = witness[0]
                second = witness[1]
                if isinstance(second, list):
                    a = second
                    x = sum(c * (p**i) for i, c in enumerate(a))
                    explicit_a = True
                else:
                    x = second
                    explicit_a = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: p is prime
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H2: x in Z_p
    try:
        if not h1:
            h2 = False
        else:
            if x == 0:
                h2 = True
            else:
                val = p_adic_valuation(x, p)
                h2 = bool(val >= 0)
            
            if h2 and explicit_a:
                if not all(0 <= c < p for c in a):
                    h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: x is unit iff a_0 != 0
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            if x == 0:
                is_unit = False
            else:
                val = p_adic_valuation(x, p)
                is_unit = (val == 0)
            
            x_rat = Rational(x)
            u = x_rat.p
            v = x_rat.q
            
            u_int = int(u)
            v_int = int(v)
            p_int = int(p)
            
            # a_0 is the first p-adic digit, which is (u * v^-1) mod p
            a_0 = (u_int * pow(v_int, -1, p_int)) % p_int
            
            a_0_not_zero = (a_0 != 0)
            
            neg_q = bool(is_unit != a_0_not_zero)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]