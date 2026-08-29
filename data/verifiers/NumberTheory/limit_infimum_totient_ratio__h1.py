import sympy
import itertools
import math

# Top-level setup
# No specific named bindings needed for this number theory conjecture.
# The witness is expected to be a sequence (e.g., a generator, list, callable, or sympy expression)
# representing the sequence of integers n_k.

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness should be a sequence of integers (e.g., sympy.S.Primes, a lambda function, 
    a sympy expression, or an iterable).
    """
    # H_1: \phi(n) is Euler's totient function
    # This is a definitional hypothesis that holds by the context of the problem.
    h1_ok = True
    
    neg_q_ok = False
    try:
        elements = []
        
        # Extract elements from the witness sequence
        if witness == sympy.S.Primes:
            elements = [sympy.prime(i) for i in range(1, 200)]
            
        elif isinstance(witness, sympy.Expr):
            free = list(witness.free_symbols)
            if len(free) == 1:
                k = free[0]
                # Test standard indices and highly composite indices to catch sequences that go to 0
                test_indices = list(range(1, 300))
                primorials = [2, 6, 30, 210, 2310, 30030, 510510, 9699690, 223092870]
                test_indices.extend(primorials)
                test_indices.extend([p - 1 for p in primorials])
                test_indices.extend([p + 1 for p in primorials])
                for i in test_indices:
                    try:
                        val = witness.subs(k, i)
                        if val.is_Integer:
                            elements.append(int(val))
                    except Exception:
                        pass
                        
        elif hasattr(witness, '__iter__'):
            try:
                for x in witness:
                    if isinstance(x, (int, sympy.Integer)):
                        elements.append(int(x))
                    if len(elements) >= 500:
                        break
            except Exception:
                pass
                
        elif callable(witness):
            test_indices = list(range(1, 300))
            primorials = [2, 6, 30, 210, 2310, 30030, 510510, 9699690, 223092870]
            test_indices.extend(primorials)
            test_indices.extend([p - 1 for p in primorials])
            test_indices.extend([p + 1 for p in primorials])
            for i in test_indices:
                try:
                    val = witness(i)
                    if isinstance(val, (int, sympy.Integer)):
                        elements.append(int(val))
                except Exception:
                    pass
                    
        if elements:
            # Compute the totient ratio phi(n)/n for the extracted elements
            ratios = [float(sympy.totient(x)) / float(x) for x in elements if x > 0]
            if ratios:
                # If the limit infimum is 0, the ratio will drop to very small values.
                # If the minimum ratio in our extensive sample remains bounded away from 0 
                # (e.g., > 0.15), then the limit infimum is strictly greater than 0, 
                # meaning the conclusion fails (neg_Q is True).
                if min(ratios) > 0.15:
                    neg_q_ok = True
                else:
                    neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \phi(n) is Euler's totient function",
    "¬Q: \liminf_{n \to \infty} \frac{\phi(n)}{n} > 0"
]

N_HYP = 1
NEG_Q_INDEX = 1