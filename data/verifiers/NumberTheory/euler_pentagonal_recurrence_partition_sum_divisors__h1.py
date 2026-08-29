import sympy

# Top-level setup
# No special named objects needed for this number theory conjecture.

CONDITION_LABELS = [
    "H_1: p(n) denotes the partition function with p(0)=1",
    "H_2: sigma(n) denotes the sum of positive divisors function",
    "not Q: n p(n) != sum_{k=1}^n sigma(k) p(n-k)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n = witness
    
    # The remaining hypotheses are definitions, which hold vacuously 
    # in the context of evaluating the witness.
    h1 = True
    h2 = True
    
    try:
        # Check if n is a real number that can be compared to an integer
        try:
            is_int = (n == int(n))
        except Exception:
            # If we cannot even compare n to an int (e.g. symbolic, matrix, etc.),
            # we cannot evaluate the predicate.
            return [h1, h2, False]
            
        if not is_int:
            # If n is a non-integer (e.g., a float or rational), the partition function 
            # is undefined, meaning the conclusion equation fails to hold.
            return [h1, h2, True]
            
        n = int(n)
        
        def p(m):
            if m == 0:
                return 1
            if m < 0:
                return 0
            return sympy.ntheory.partitions(m)
            
        def sigma(m):
            return sympy.divisor_sigma(m)
            
        lhs = n * p(n)
        
        # Evaluate the sum on the right-hand side
        rhs = sum(sigma(k) * p(n - k) for k in range(1, n + 1))
        
        neg_q = (lhs != rhs)
        
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]