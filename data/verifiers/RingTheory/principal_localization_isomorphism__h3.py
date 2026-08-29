import sympy
import math
import itertools
import functools

class FiniteRing:
    """
    Helper class to represent a finite ring.
    n: number of elements (0 to n-1)
    add: n x n list of lists for addition table
    mul: n x n list of lists for multiplication table
    f: an element of the ring (int)
    """
    def __init__(self, n, add, mul, f=0):
        self.n = n
        self.add = add
        self.mul = mul
        self.f = f

def is_commutative_ring(n, add, mul):
    if not isinstance(n, int) or n <= 0 or n > 50:
        return False
    if not isinstance(add, list) or len(add) != n:
        return False
    if not isinstance(mul, list) or len(mul) != n:
        return False
    for row in add:
        if not isinstance(row, list) or len(row) != n: return False
    for row in mul:
        if not isinstance(row, list) or len(row) != n: return False

    for i in range(n):
        for j in range(n):
            if not isinstance(add[i][j], int) or not (0 <= add[i][j] < n):
                return False
            if not isinstance(mul[i][j], int) or not (0 <= mul[i][j] < n):
                return False

    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]:
                return False
            if mul[i][j] != mul[j][i]:
                return False

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]:
                    return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]:
                    return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]:
                    return False

    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1:
        return False

    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)):
            return False

    return True

def has_identity(n, mul):
    for i in range(n):
        if all(mul[i][j] == j for j in range(n)):
            return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            n, add, mul, f = witness
        else:
            n = witness.n
            add = witness.add
            mul = witness.mul
            f = witness.f
            
        h1 = is_commutative_ring(n, add, mul)
        h2 = isinstance(f, int) and 0 <= f < n
        
        # The conclusion "S^{-1}R is isomorphic to R[x]/(xf - 1)" holds for any commutative ring with identity.
        # If R lacks an identity, the quotient ring R[x]/(xf - 1) is undefined (since 1 is not in R),
        # making the conclusion false.
        neg_q = not has_identity(n, mul)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ["H_1: R is a commutative ring", "H_2: f is an element of R", "¬Q: The localized ring is not isomorphic to the quotient ring"]

N_HYP = 2
NEG_Q_INDEX = 2