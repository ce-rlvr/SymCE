import math

def conditions(witness):
    try:
        # The witness should be an integer
        n = int(witness)
        if n != witness:
            return [False]
        
        # Factorial is only defined for non-negative integers
        if n < 0:
            return [False]
            
        n_fact = math.factorial(n)
        
        # Calculate sigma(n!), the sum of divisors of n!
        if n == 0 or n == 1:
            sigma_n_fact = 1
        else:
            # Use Legendre's formula to find the prime factorization of n!
            # and compute the sum of divisors directly to ensure high performance.
            sieve = [True] * (n + 1)
            sigma_n_fact = 1
            for p in range(2, n + 1):
                if sieve[p]:
                    # Mark multiples of p as composite
                    for i in range(p * p, n + 1, p):
                        sieve[i] = False
                    
                    # Count the exponent of p in n!
                    count = 0
                    k = p
                    while k <= n:
                        count += n // k
                        k *= p
                    
                    # Multiply the sum of divisors contribution for prime p
                    sigma_n_fact *= (p**(count + 1) - 1) // (p - 1)
                    
        # Calculate n! * sum(1/k for k in 1..n)
        # Since k <= n, k always divides n!, so n! / k is an integer.
        rhs = sum(n_fact // k for k in range(1, n + 1))
        
        # The negated conclusion is that sigma(n!) < n! * sum(1/k)
        neg_q = bool(sigma_n_fact < rhs)
        
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: \\sigma(n!) < n! \\sum_{k=1}^n \\frac{1}{k}"
]

N_HYP = 0
NEG_Q_INDEX = 0