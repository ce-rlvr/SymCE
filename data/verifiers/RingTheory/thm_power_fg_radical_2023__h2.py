import math
import sympy
from sympy import Rational, Integer

# Top-level setup
# Expected witness: a dictionary representing a finite ring Z/nZ and a subset I.
# Example: witness = {'n': 6, 'I': [0, 4]}

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness['n']
            I_list = witness['I']
        else:
            n = witness.n
            I_list = witness.I
            
        n = int(n)
        if n < 2 or n > 1000:
            return [False, False, False]
            
        I_set = set(int(x) % n for x in I_list)
        
        # H1: R is a commutative ring
        # Z/nZ is always a commutative ring for n >= 2
        h1 = True
        
        # H2: \sqrt{I} is a finitely generated ideal
        # First, compute \sqrt{I} in Z/nZ
        radical = set()
        for x in range(n):
            curr = x % n
            in_radical = False
            # In a finite ring of size n, the sequence of powers is eventually periodic.
            # If x^m \in I for some m >= 1, it must occur for some m <= n.
            for _ in range(1, n + 1):
                if curr in I_set:
                    in_radical = True
                    break
                curr = (curr * x) % n
            if in_radical:
                radical.add(x)
                
        # Check if \sqrt{I} is an ideal
        is_ideal = (0 in radical)
        if is_ideal:
            # Closed under addition
            for a in radical:
                for b in radical:
                    if (a + b) % n not in radical:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
        if is_ideal:
            # Closed under multiplication by any element in R
            for a in radical:
                for r in range(n):
                    if (a * r) % n not in radical:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
                    
        # In Z/nZ, every ideal is finitely generated (principal).
        h2 = is_ideal
        
        # Conclusion: \exists m \ge 1 such that (\sqrt{I})^m \subseteq I
        # Find the generator of the principal ideal \sqrt{I}
        d = n
        for x in radical:
            d = math.gcd(d, x)
            
        conclusion_holds = False
        # The sequence of ideal powers (\sqrt{I})^m is decreasing and must stabilize within n steps.
        for m in range(1, n + 1):
            gen = pow(d, m, n)
            ideal_power = set((k * gen) % n for k in range(n))
            if ideal_power.issubset(I_set):
                conclusion_holds = True
                break
                
        neg_q = not conclusion_holds
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The radical \\sqrt{I} is a finitely generated ideal",
    "¬Q: For all positive integers n, (\\sqrt{I})^n \\not\\subseteq I"
]

N_HYP = 2
NEG_Q_INDEX = 2