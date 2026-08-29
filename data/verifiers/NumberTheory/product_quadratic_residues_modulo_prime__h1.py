import math

# No special top-level bindings needed for this number theory conjecture;
# witnesses are expected to be integers.

def conditions(witness):
    try:
        p = int(witness)
        # Restrict to reasonable positive integers to ensure fast execution
        if p <= 1 or p > 100000:
            return [False]
            
        # Find all quadratic residues modulo p that are coprime to p
        residues = set()
        for x in range(1, p):
            val = (x * x) % p
            if math.gcd(val, p) == 1:
                residues.add(val)
                
        # Compute the product of all such quadratic residues modulo p
        product = 1
        for r in residues:
            product = (product * r) % p
            
        # Check the conclusion
        if p % 4 == 3:
            q_holds = (product == 1)
        elif p % 4 == 1:
            q_holds = (product == p - 1)
        else:
            # The conclusion is an implication that only restricts p = 1 or 3 mod 4.
            # If p is even, the implication is vacuously true.
            q_holds = True
            
        neg_q = not q_holds
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The product of quadratic residues modulo p fails to match the specified congruence"
]

N_HYP = 0
NEG_Q_INDEX = 0