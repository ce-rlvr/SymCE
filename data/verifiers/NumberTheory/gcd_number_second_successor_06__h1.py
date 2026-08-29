import sympy

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a counterexample to the false conjecture.
    The conjecture claims: \gcd(n, n+2) = 1 if n is odd, and 2 if n is even.
    (The hypothesis that n is an integer was dropped).
    """
    try:
        n = sympy.sympify(witness)
        
        # Evaluate the conclusion:
        # It expects n to be either even or odd, and the corresponding GCD to match.
        if n % 2 == 0:
            q_holds = (sympy.gcd(n, n + 2) == 2)
        elif n % 2 == 1:
            q_holds = (sympy.gcd(n, n + 2) == 1)
        else:
            # If n is neither odd nor even (e.g., a fraction or symbol),
            # the conclusion's premise fails to apply properly, meaning the statement fails.
            q_holds = False
            
    except Exception:
        q_holds = False

    neg_q = not q_holds
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: \\gcd(n, n+2) != 1 if n is odd, or \\gcd(n, n+2) != 2 if n is even"
]

N_HYP = 0
NEG_Q_INDEX = 0