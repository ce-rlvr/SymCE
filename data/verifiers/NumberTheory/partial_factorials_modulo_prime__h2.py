import sympy

# Top-level setup
# No specific named bindings needed for this number theory problem.

def conditions(witness):
    try:
        p, k = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(0 <= k and k <= p - 1)
    except Exception:
        h2 = False
        
    try:
        # Evaluate the factorials and the right-hand side.
        # We use sympy.factorial to safely handle potential non-integer counterexamples
        # (since the dropped hypothesis is that k is an integer).
        lhs = sympy.factorial(k) * sympy.factorial(p - k - 1)
        rhs = (-1)**(k + 1)
        
        # Check congruence modulo p
        mod_lhs = sympy.Mod(lhs, p)
        mod_rhs = sympy.Mod(rhs, p)
        
        diff = sympy.simplify(mod_lhs - mod_rhs)
        
        # If diff is exactly 0, the congruence holds (conclusion is true, so neg_q is False).
        # Otherwise, the congruence fails (conclusion is false, so neg_q is True).
        neg_q = not (diff == 0)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: 0 <= k <= p - 1",
    "¬Q: k!(p-k-1)! is not congruent to (-1)^{k+1} mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2