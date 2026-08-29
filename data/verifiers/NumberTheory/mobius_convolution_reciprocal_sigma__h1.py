import sympy
from sympy import divisors, primefactors, mobius, divisor_sigma, Rational

CONDITION_LABELS = [
    "¬Q: \\sum_{d|n} \\frac{\\mu(d)}{\\sigma(d)} \\neq \\prod_{p|n} \\frac{p}{p+1}"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        n = witness
        
        # Evaluate LHS: sum_{d|n} mu(d)/sigma(d)
        lhs_val = 0
        for d in divisors(n):
            lhs_val += Rational(mobius(d), divisor_sigma(d))
            
        # Evaluate RHS: prod_{p|n} p/(p+1)
        rhs_val = 1
        for p in primefactors(n):
            rhs_val *= Rational(p, p + 1)
            
        # The negated conclusion is True if LHS != RHS
        neg_q = bool(lhs_val != rhs_val)
    except Exception:
        neg_q = False
        
    return [neg_q]