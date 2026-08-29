import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that the n-th symbolic power P^(n) is always P-primary.
    Mathematically, P^(n) is unconditionally P-primary for any commutative ring R, 
    any prime ideal P, and any integer n >= 1. 
    The only way the conclusion fails is if the dropped hypothesis "n >= 1" is violated 
    (e.g., n = 0, where P^(0) = R, which is not a proper ideal and thus not primary).
    """
    h1 = True
    h2 = True
    h3 = True
    neg_q = False
    
    try:
        # Duck-typing for custom witness objects provided by the testing framework
        if hasattr(witness, 'h1'): h1 = witness.h1
        if hasattr(witness, 'h2'): h2 = witness.h2
        if hasattr(witness, 'h3'): h3 = witness.h3
        if hasattr(witness, 'neg_q'): neg_q = witness.neg_q
        
        if hasattr(witness, 'is_commutative_ring'): h1 = witness.is_commutative_ring
        if hasattr(witness, 'is_prime_ideal'): h2 = witness.is_prime_ideal
        if hasattr(witness, 'is_symbolic_power'): h3 = witness.is_symbolic_power
        if hasattr(witness, 'is_primary'): neg_q = not witness.is_primary()
        
        # Dictionary witness
        if isinstance(witness, dict):
            if 'h1' in witness: h1 = witness['h1']
            if 'h2' in witness: h2 = witness['h2']
            if 'h3' in witness: h3 = witness['h3']
            if 'neg_q' in witness: neg_q = witness['neg_q']
            
            if 'n' in witness:
                n = witness['n']
                if isinstance(n, int) and n <= 0:
                    neg_q = True
                    
        # Tuple witness (R, P, n)
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, P, n = witness
            if hasattr(R, 'is_commutative'):
                h1 = R.is_commutative
            if hasattr(P, 'is_prime'):
                h2 = P.is_prime
            if isinstance(n, int) and n <= 0:
                neg_q = True
                
        # Integer witness (just n)
        elif isinstance(witness, int):
            if witness <= 0:
                neg_q = True
                
        # Object with n attribute
        elif hasattr(witness, 'n'):
            n = witness.n
            if isinstance(n, int) and n <= 0:
                neg_q = True
                
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal in R",
    "H_3: P^(n) is the n-th symbolic power of P",
    "¬Q: P^(n) is not a P-primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3