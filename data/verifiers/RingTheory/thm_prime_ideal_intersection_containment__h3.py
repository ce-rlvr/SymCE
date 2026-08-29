import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
import itertools
import math
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Expected witness formats:
      - (n, P, I, J) where n is an integer >= 2 (representing ring Z/nZ), and P, I, J are iterables of integers.
      - (R, P, I, J) where R is a finite collection, and P, I, J are iterables of integers.
      - (P, I, J) where P, I, J are iterables of integers (implicitly assumes R is the ring of integers ZZ).
    """
    try:
        if len(witness) == 4:
            R, P, I, J = witness
        elif len(witness) == 3:
            P, I, J = witness
            R = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # Attempt to interpret R as a finite ring Z/nZ
    n = None
    if isinstance(R, int):
        n = R
    elif hasattr(R, 'order') and callable(R.order):
        try:
            n = int(R.order())
        except Exception:
            pass
    elif isinstance(R, (set, list, tuple)):
        n = len(R)
    
    if n is not None:
        if n < 2:
            # Trivial ring has no prime ideals
            return [True, False, False, False]
        try:
            P_set = set(p % n for p in P)
            I_set = set(i % n for i in I)
            J_set = set(j % n for j in J)
            
            h1 = True  # Z/nZ is a commutative ring for n >= 2
            
            # Check if P is an ideal in Z/nZ
            is_ideal = True
            if not P_set:
                is_ideal = False
            else:
                for a in P_set:
                    for b in P_set:
                        if (a + b) % n not in P_set:
                            is_ideal = False
                            break
                    for r in range(n):
                        if (a * r) % n not in P_set:
                            is_ideal = False
                            break
                    if not is_ideal:
                        break
            
            # Check if P is a prime ideal in Z/nZ
            is_prime = True
            if len(P_set) == n:
                is_prime = False  # Prime ideal must be proper
            else:
                for a in range(n):
                    for b in range(n):
                        if (a * b) % n in P_set:
                            if a not in P_set and b not in P_set:
                                is_prime = False
                                break
                    if not is_prime:
                        break
            
            h2 = is_ideal and is_prime
            
            intersection = I_set.intersection(J_set)
            h3 = intersection.issubset(P_set)
            
            neg_q = not (I_set.issubset(P_set) or J_set.issubset(P_set))
            
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Fallback: Assume R is the ring of integers ZZ (or a similar integral domain)
    # In ZZ, the only finite prime ideal is {0}.
    try:
        P_set = set(P)
        I_set = set(I)
        J_set = set(J)
        
        h1 = True  # ZZ is a commutative ring
        
        if P_set == {0}:
            h2 = True
        else:
            h2 = False
            
        intersection = I_set.intersection(J_set)
        h3 = intersection.issubset(P_set)
        
        neg_q = not (I_set.issubset(P_set) or J_set.issubset(P_set))
        
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: The intersection I \\cap J is contained in P",
    "¬Q: I is not contained in P and J is not contained in P"
]

N_HYP = 3
NEG_Q_INDEX = 3