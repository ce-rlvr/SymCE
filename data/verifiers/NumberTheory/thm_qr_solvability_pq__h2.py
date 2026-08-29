import sympy

# Top-level setup
# (No specific bindings needed for this number theory problem)

def conditions(witness):
    """
    Given a witness (a, p, q), checks the hypotheses and the negated conclusion.
    Returns [H1_ok, H2_ok, neg_Q_ok].
    """
    try:
        a, p, q = witness
    except Exception:
        return [False, False, False]
        
    # H1: p and q are distinct odd primes
    try:
        h1 = sympy.isprime(p) and sympy.isprime(q) and (p != q) and (p % 2 != 0) and (q % 2 != 0)
    except Exception:
        h1 = False
        
    # H2: a is coprime to the product pq
    try:
        h2 = sympy.gcd(a, p * q) == 1
    except Exception:
        h2 = False
        
    # Conclusion: There exists an integer x such that x^2 = a mod pq iff (a/p) = 1 and (a/q) = 1
    # We want neg_Q to be True when this equivalence FAILS.
    try:
        m = abs(p * q)
        if m == 0:
            has_sol = False
        elif m < 100000:
            # For small moduli, brute-force to be absolutely independent of any theorems
            a_mod = a % m
            has_sol = False
            for x in range(m):
                if (x * x) % m == a_mod:
                    has_sol = True
                    break
        else:
            # For large moduli, try using sympy's nthroot_mod
            try:
                has_sol = sympy.ntheory.nthroot_mod(a, 2, m) is not None
            except Exception:
                # Fallback using CRT (valid since p and q are distinct primes if H1 holds)
                ans_p = (a % p == 0) or (sympy.jacobi_symbol(a, p) == 1)
                ans_q = (a % q == 0) or (sympy.jacobi_symbol(a, q) == 1)
                has_sol = ans_p and ans_q
                
        # Compute Legendre symbols (using jacobi_symbol which is equivalent for odd primes)
        leg_p = sympy.jacobi_symbol(a, p)
        leg_q = sympy.jacobi_symbol(a, q)
        
        rhs = (leg_p == 1) and (leg_q == 1)
        
        # The conclusion is the equivalence of has_sol and rhs
        conclusion = (has_sol == rhs)
        
        # We want the negation of the conclusion
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p and q are distinct odd primes",
    "H_2: a is coprime to the product pq",
    "¬Q: The equivalence (x^2 = a mod pq has a solution iff (a/p)=1 and (a/q)=1) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2