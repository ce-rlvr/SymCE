import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.abc import x
from sympy.ntheory import legendre_symbol, isprime

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            p = witness.get('p')
        else:
            a, p = witness
    except Exception:
        return [False, False]
        
    try:
        a_val = int(a)
        p_val = int(p)
        h1 = (a_val == a) and (p_val == p) and (p_val > 1) and (a_val % p_val != 0)
    except Exception:
        h1 = False
        
    try:
        if not isprime(p_val):
            # If p is not prime, F_p is not a field, so the conclusion is ill-typed and fails.
            neg_q = True
        else:
            # LHS: x^2 - a is irreducible over F_p
            # factor_list returns (coeff, [(factor1, exp1), ...])
            factors = sympy.factor_list(x**2 - a_val, modulus=p_val)[1]
            # It is irreducible if there is exactly one factor and its exponent is 1
            lhs = (len(factors) == 1 and factors[0][1] == 1)
            
            # RHS: (a/p) = -1
            if p_val == 2:
                # Legendre symbol is undefined for p=2.
                # We treat the condition (a/p) = -1 as False.
                rhs = False
            else:
                rhs = (legendre_symbol(a_val, p_val) == -1)
            
            # The conclusion is the biconditional: LHS iff RHS
            # neg_q is True when the conclusion fails
            neg_q = not (lhs == rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer not divisible by p",
    "¬Q: The polynomial x^2 - a is irreducible over F_p iff (a/p) = -1 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1