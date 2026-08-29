import sympy

def conditions(witness):
    """
    Given a witness integer n, checks if it is a counterexample to the conjecture:
    "sigma(n) >= psi(n), with equality if and only if n is a square-free integer"
    """
    try:
        # The witness must be an integer
        if int(witness) != witness:
            return [False]
        n = int(witness)
        
        # The functions are generally undefined or singular at n = 0
        if n == 0:
            return [False]
            
        # Compute sum of divisors. For negative n, we use the divisors of |n|.
        sig = sympy.divisor_sigma(abs(n))
        
        # Compute Dedekind psi function: psi(n) = n * product_{p|n} (1 + 1/p)
        # We preserve the sign of n in the initial value, which is the key to the counterexample
        # when the hypothesis "n is a positive integer" is dropped.
        psi = n
        for p in sympy.primefactors(abs(n)):
            psi = psi * (p + 1) // p
            
        # Check if n is square-free. A negative integer is square-free if its absolute value is.
        sqf = sympy.is_squarefree(abs(n))
        
        # Evaluate the conclusion
        part1 = (sig >= psi)
        part2 = ((sig == psi) == sqf)
        conclusion = part1 and part2
        
        # The conjecture is false if the conclusion fails
        neg_q = not conclusion
        
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: sigma(n) >= psi(n) with equality iff n is square-free fails"
]

N_HYP = 0
NEG_Q_INDEX = 0