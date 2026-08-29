import itertools
import math
import functools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# (No specific named objects are required for this domain)

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with:
      - 'ring': list of elements in the ring R
      - 'add': callable for addition in R
      - 'mul': callable for multiplication in R
      - 'I': list of elements in ideal I
      - 'J': list of elements in ideal J
    """
    try:
        R = witness['ring']
        add = witness['add']
        mul = witness['mul']
        I = witness['I']
        J = witness['J']
    except Exception:
        return [False, False, False]

    def check_H1():
        try:
            if not isinstance(R, list) or not R: return False
            if len(R) > 12: return False # Prevent timeout for power set operations
            if len(set(R)) != len(R): return False
            
            # check closure
            for a in R:
                for b in R:
                    if add(a, b) not in R: return False
                    if mul(a, b) not in R: return False
            # check add commutativity and associativity
            for a in R:
                for b in R:
                    if add(a, b) != add(b, a): return False
                    if mul(a, b) != mul(b, a): return False
                    for c in R:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
            # check zero
            zeros = [z_elem for z_elem in R if all(add(a, z_elem) == a for a in R)]
            if len(zeros) != 1: return False
            zero = zeros[0]
            # check inverses
            for a in R:
                if not any(add(a, b) == zero for b in R): return False
            return True
        except Exception:
            return False

    def is_ideal(S):
        try:
            if not isinstance(S, list) or not S: return False
            if any(val not in R for val in S): return False
            zeros = [z_elem for z_elem in R if all(add(a, z_elem) == a for a in R)]
            if not zeros: return False
            zero = zeros[0]
            if zero not in S: return False
            for val in S:
                inv_val = [y_val for y_val in R if add(val, y_val) == zero]
                if not any(y_val in S for y_val in inv_val): return False
                for y_val in S:
                    if add(val, y_val) not in S: return False
            for r in R:
                for val in S:
                    if mul(r, val) not in S: return False
            return True
        except Exception:
            return False

    def check_H2():
        try:
            return is_ideal(I) and is_ideal(J)
        except Exception:
            return False

    def check_neg_Q():
        try:
            ideals = []
            for r in range(1, len(R) + 1):
                for subset in itertools.combinations(R, r):
                    if is_ideal(list(subset)):
                        ideals.append(set(subset))
            
            prime_ideals = []
            for P in ideals:
                if len(P) == len(R): continue # proper ideal
                is_prime = True
                for a in R:
                    for b in R:
                        if mul(a, b) in P:
                            if a not in P and b not in P:
                                is_prime = False
                                break
                    if not is_prime: break
                if is_prime:
                    prime_ideals.append(P)
            
            V_I = [P for P in prime_ideals if all(val in P for val in I)]
            V_J = [P for P in prime_ideals if all(val in P for val in J)]
            
            V_I_cap_V_J = [P for P in V_I if P in V_J]
            is_empty = (len(V_I_cap_V_J) == 0)
            
            I_plus_J = set()
            for val_i in I:
                for val_j in J:
                    I_plus_J.add(add(val_i, val_j))
                    
            is_comaximal = (len(I_plus_J) == len(R) and all(val in R for val in I_plus_J))
            
            # The conclusion states: comaximal iff V(I) \cap V(J) is empty.
            # We want the negation of this conclusion.
            return is_comaximal != is_empty
        except Exception:
            return False

    h1 = check_H1()
    h2 = check_H2() if h1 else False
    nq = check_neg_Q() if h1 and h2 else False

    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "¬Q: I and J are comaximal iff V(I) \\cap V(J) is empty is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2