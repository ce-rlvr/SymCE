import math
import re
import itertools
import sympy
from sympy import S

# Top-level setup
Z = S.Integers

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The conjecture claims that if I and J are comaximal in R, and f: R -> S 
    is a surjective ring homomorphism, then f(I) and f(J) are comaximal in S.
    
    A standard counterexample uses R = Z, S = Z/nZ, I = aZ, J = bZ, 
    with f being the natural projection.
    """
    try:
        n, a, b = None, None, None
        
        # Extract all integers from the string representation of the witness
        nums = [abs(int(x)) for x in re.findall(r'\d+', str(witness))]
        # Filter out likely memory addresses or excessively large numbers
        nums = [x for x in nums if x < 10**6]
        # Take at most 10 numbers to avoid combinatorial explosion in permutations
        nums = nums[:10]
        
        if len(nums) >= 3:
            # Try to find a permutation of the extracted numbers that forms a valid counterexample
            for p in itertools.permutations(nums, 3):
                n_cand, a_cand, b_cand = p
                h1_cand = (n_cand >= 2)
                h3_cand = (math.gcd(a_cand, b_cand) == 1) and (a_cand > 1) and (b_cand > 1)
                neg_q_cand = (math.gcd(a_cand, n_cand) == 1) or (math.gcd(b_cand, n_cand) == 1)
                
                if h1_cand and h3_cand and neg_q_cand:
                    n, a, b = n_cand, a_cand, b_cand
                    break
            
            # If no permutation forms a valid counterexample, fallback to the first 3 numbers
            if n is None:
                n, a, b = nums[0], nums[1], nums[2]
        else:
            return [False, False, False, False]
            
        # H1: R and S are rings
        # We model R = Z, S = Z/nZ. S is a proper ring if n >= 2.
        h1 = bool(n >= 2)
        
        # H2: f is a surjective ring homomorphism
        # The natural projection Z -> Z/nZ is always a surjective ring homomorphism.
        h2 = True
        
        # H3: I and J are comaximal in R
        # I = aZ, J = bZ. Comaximal means I + J = R (gcd(a,b) == 1) 
        # and I, J are proper ideals (a > 1, b > 1).
        h3 = bool((math.gcd(a, b) == 1) and (a > 1) and (b > 1))
        
        # neg_Q: f(I) and f(J) are not comaximal in S
        # f(I) = (a mod n)Z/nZ, f(J) = (b mod n)Z/nZ
        # They are comaximal in S iff f(I) + f(J) = S, f(I) != S, and f(J) != S.
        # Since gcd(a,b) = 1, f(I) + f(J) = S is always true.
        # f(I) != S iff gcd(a, n) > 1.
        # f(J) != S iff gcd(b, n) > 1.
        # Thus, they are NOT comaximal if gcd(a, n) == 1 or gcd(b, n) == 1.
        neg_q = bool((math.gcd(a, n) == 1) or (math.gcd(b, n) == 1))
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism",
    "H_3: I and J are comaximal in R",
    "¬Q: f(I) and f(J) are not comaximal in S"
]

N_HYP = 3
NEG_Q_INDEX = 3