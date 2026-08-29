import sympy
from sympy import divisor_sigma, S
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Extract n and factors
    try:
        if isinstance(witness, dict) and 'n' in witness:
            n = witness['n']
            if 'factors' in witness:
                factors = witness['factors']
            else:
                factors = list(factorint(n).items()) if isinstance(n, (int, sympy.Integer)) else []
            if isinstance(factors, dict):
                factors = list(factors.items())
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (int, sympy.Integer)):
            n, factors = witness
            if isinstance(factors, dict):
                factors = list(factors.items())
        else:
            n = witness
            factors = list(factorint(n).items()) if isinstance(n, (int, sympy.Integer)) else []
    except Exception:
        n = witness
        factors = []

    # H1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 1
    except Exception:
        h1 = False

    # Conclusion: sigma(n) == prod (p_i^{a_i+1}-1)/(p_i-1)
    try:
        if not isinstance(n, (int, sympy.Integer)):
            neg_q = False
        else:
            lhs = divisor_sigma(n)
            rhs = 1
            for p, a in factors:
                num = S(p)**(a+1) - 1
                den = S(p) - 1
                if den == 0:
                    raise ZeroDivisionError
                rhs *= num / den
            neg_q = bool(lhs != rhs)
    except ZeroDivisionError:
        neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: sigma(n) != prod_{i=1}^k (p_i^{a_i+1}-1)/(p_i-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1