import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture drops the hypothesis that n >= 1.
    """
    try:
        n = sympy.sympify(witness)
        if n.is_integer is not True:
            return [False]
    except Exception:
        return [False]

    try:
        # The Selberg identity is defined for n >= 1.
        # If n < 1, the equation is undefined or fails, making it a valid counterexample.
        if n < 1:
            return [True]

        def von_mangoldt(k):
            if k == 1:
                return sympy.S.Zero
            factors = sympy.factorint(k)
            if len(factors) == 1:
                p = list(factors.keys())[0]
                return sympy.log(p)
            return sympy.S.Zero

        # LHS: \Lambda(n)\log n + \sum_{d|n} \Lambda(d)\Lambda(n/d)
        LHS_term1 = von_mangoldt(n) * sympy.log(n)
        LHS_term2 = sympy.S.Zero
        for d in sympy.divisors(n):
            LHS_term2 += von_mangoldt(d) * von_mangoldt(n // d)
        LHS = LHS_term1 + LHS_term2

        # RHS: \sum_{d|n} \mu(d)\log^2(n/d)
        RHS = sympy.S.Zero
        for d in sympy.divisors(n):
            RHS += sympy.mobius(d) * (sympy.log(n // d))**2

        diff = sympy.expand(LHS - RHS)
        
        if diff == 0:
            neg_Q = False
        else:
            try:
                # Numerical fallback in case symbolic simplification misses an identity
                diff_num = complex(diff.evalf())
                if abs(diff_num) < 1e-9:
                    neg_Q = False
                else:
                    neg_Q = True
            except Exception:
                neg_Q = True
                
        return [neg_Q]

    except Exception:
        # If evaluation fails for an integer, the equation does not hold.
        return [True]

CONDITION_LABELS = [
    "¬Q: \\Lambda(n)\\log n + \\sum_{d|n} \\Lambda(d)\\Lambda(n/d) \\neq \\sum_{d|n} \\mu(d)\\log^2(n/d)"
]

N_HYP = 0
NEG_Q_INDEX = 0