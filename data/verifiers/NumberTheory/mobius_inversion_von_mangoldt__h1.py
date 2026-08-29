import sympy
import sympy.ntheory
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        n = sympy.sympify(witness)
        n_int = int(n)
        if n_int != n:
            Q_holds = False
        elif n_int < 1:
            Q_holds = False
        else:
            if n_int == 1:
                L = sympy.Integer(0)
            else:
                factors = sympy.ntheory.primefactors(n_int)
                if len(factors) == 1:
                    L = sympy.log(factors[0])
                else:
                    L = sympy.Integer(0)
            
            R = -sum(sympy.ntheory.mobius(d) * sympy.log(d) for d in sympy.ntheory.divisors(n_int))
            Q_holds = sympy.simplify(L - R) == 0
    except Exception:
        Q_holds = False

    return [not Q_holds]

CONDITION_LABELS = [
    "¬Q: \\Lambda(n) != -\\sum_{d|n} \\mu(d) \\log d"
]

N_HYP = 0
NEG_Q_INDEX = 0