import sympy
import math

# Top-level setup: named object bindings that the witness expression may reference.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture:
    "R is a principal ideal domain if and only if there exists a Dedekind-Hasse norm on R."
    """
    n = None
    try:
        if isinstance(witness, int):
            n = witness
        elif hasattr(witness, 'is_Integer') and witness.is_Integer:
            n = int(witness)
        elif isinstance(witness, str):
            # Parse strings like "Z/6Z" or "Z6" or "6"
            s = witness.replace(' ', '').replace('Z/', '').replace('Z', '')
            try:
                n = int(s)
            except Exception:
                pass
    except Exception:
        pass

    if n is not None:
        try:
            if n <= 1:
                return [False]
            
            # In Z/nZ, every ideal is principal. 
            # Thus, Z/nZ is a PID iff it is an integral domain, which happens iff n is prime.
            is_pid = sympy.isprime(n)
            
            # Every finite principal ideal ring (like Z/nZ) has a Dedekind-Hasse norm.
            # For example, N(x) = (number of prime factors of gcd(x, n)) + 1 is a valid norm.
            has_norm = True
            
            # The conjecture states: R is a PID iff R has a Dedekind-Hasse norm.
            # We want the conjecture to FAIL at the witness.
            neg_q = (is_pid != has_norm)
            return [neg_q]
        except Exception:
            return [False]
    
    # Fallback for sympy rings or other objects
    try:
        if hasattr(witness, 'is_PID') and hasattr(witness, 'is_IntegralDomain'):
            is_pid = bool(witness.is_PID)
            # For integral domains, it has a Dedekind-Hasse norm iff it is a PID (by the true theorem).
            if witness.is_IntegralDomain:
                has_norm = is_pid
                neg_q = (is_pid != has_norm)
                return [neg_q]
    except Exception:
        pass

    return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence (R is a PID iff R has a Dedekind-Hasse norm) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0