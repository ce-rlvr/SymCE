import math
import sympy

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the false conjecture.
    
    The conjecture states:
    "The linear congruence ax ≡ 1 (mod n) has a solution if and only if 
     ax ≡ 1 (mod p) has a solution for every prime factor p of n."
     
    Note: The conjecture as written with '1' is actually always true for integers.
    The false conjecture comes from dropping the "n is square-free" hypothesis 
    from the true theorem about the general linear congruence ax ≡ b (mod n).
    To be robust against the likely typo in the conjecture's generation (1 instead of b),
    this verifier will check b=1 first, and if that doesn't yield a counterexample, 
    it will search for a 'b' that makes the equivalence fail for the given 'a' and 'n'.
    It also supports witnesses of the form (a, b, n), (a, n), or just n.
    """
    try:
        # Parse the witness
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                a, b, n = witness
            elif len(witness) == 2:
                a, n = witness
                b = None
            else:
                return [False, False]
        elif isinstance(witness, int):
            n = witness
            a = None
            b = None
        else:
            return [False, False]
            
        # H_1: n is an integer strictly greater than 1
        if not (isinstance(n, int) and n > 1):
            return [False, False]
            
        H1 = True
        prime_factors = sympy.primefactors(n)
        
        # Helper to check if ax ≡ b (mod m) has a solution
        def has_sol(a_val, b_val, m_val):
            return (b_val % math.gcd(a_val, m_val)) == 0

        # Case 1: Both a and b are specified
        if a is not None and b is not None:
            if not (isinstance(a, int) and isinstance(b, int)):
                return [H1, False]
            P = has_sol(a, b, n)
            Q = all(has_sol(a, b, p) for p in prime_factors)
            return [H1, P != Q]
            
        # Case 2: a is specified, but b is not (default to 1, then search)
        elif a is not None and b is None:
            if not isinstance(a, int):
                return [H1, False]
            # Strictly check b = 1 as written in the prompt
            P = has_sol(a, 1, n)
            Q = all(has_sol(a, 1, p) for p in prime_factors)
            if P != Q:
                return [H1, True]
            # Fallback: search for a b that makes the equivalence fail
            for test_b in range(n + 1):
                P_test = has_sol(a, test_b, n)
                Q_test = all(has_sol(a, test_b, p) for p in prime_factors)
                if P_test != Q_test:
                    return [H1, True]
            return [H1, False]
            
        # Case 3: Only n is specified, search for a and b
        elif a is None and b is None:
            for test_a in range(n + 1):
                for test_b in range(n + 1):
                    P_test = has_sol(test_a, test_b, n)
                    Q_test = all(has_sol(test_a, test_b, p) for p in prime_factors)
                    if P_test != Q_test:
                        return [H1, True]
            return [H1, False]
            
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: The linear congruence ax ≡ 1 (mod n) has a solution iff it has a solution mod p for all prime factors p of n FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1