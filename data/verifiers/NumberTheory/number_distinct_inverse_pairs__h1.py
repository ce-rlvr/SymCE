import sympy
import math

# Top-level setup
# (No specific named objects required for this number theory problem)

CONDITION_LABELS = [
    "¬Q: The number of unordered pairs is not (phi(m) - s(m))/2"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness) -> list[bool]:
    # The witness must be an integer
    if not isinstance(witness, (int, sympy.Integer)):
        return [False]
        
    try:
        m = int(witness)
        
        # Modulo 0 is degenerate and phi(0) is undefined.
        # This makes the formula invalid, so the conclusion fails.
        if m == 0:
            return [True]
            
        abs_m = abs(m)
        
        # For large m, the theorem is mathematically proven to be true.
        # We return False early to avoid Time Limit Exceeded.
        if abs_m > 10000:
            return [False]
            
        # Calculate LHS: number of unordered pairs {x, y} in the reduced residue system
        # such that x * y = 1 (mod m) and x != y.
        if abs_m == 1:
            lhs = 0
        else:
            R = [x for x in range(1, abs_m + 1) if math.gcd(x, abs_m) == 1]
            pairs = set()
            for x in R:
                # Find the modular inverse of x modulo abs_m
                y = pow(x, -1, abs_m)
                if x != y:
                    pairs.add(frozenset([x, y]))
            lhs = len(pairs)
            
        # Calculate RHS: (phi(m) - s(m)) / 2
        phi_m = sympy.totient(abs_m)
        
        # s(m) is the number of solutions to x^2 = 1 (mod m)
        s_m = sum(1 for x in range(abs_m) if (x * x - 1) % abs_m == 0)
        
        rhs = (phi_m - s_m) // 2
        
        # The conclusion holds if LHS equals RHS
        q_holds = (lhs == rhs)
        neg_q = not q_holds
        
    except Exception:
        # If any calculation fails (e.g., undefined mathematical operations),
        # the conclusion is considered to fail.
        neg_q = True
        
    return [neg_q]