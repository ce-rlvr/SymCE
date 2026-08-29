import itertools
import sympy
from sympy import symbols

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a commutative Artinian ring",
    "¬Q: The localization S^{-1}R is not isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to be a finite ring represented as a tuple:
    (n, add_table, mul_table)
    where n is the number of elements (0 to n-1),
    and add_table and mul_table are n x n lists representing the operations.
    """
    try:
        n, add_table, mul_table = witness
        
        if not isinstance(n, int) or n <= 0:
            return [False, False]
            
        if len(add_table) != n or any(len(row) != n for row in add_table):
            return [False, False]
        if len(mul_table) != n or any(len(row) != n for row in mul_table):
            return [False, False]
            
        # Check closure
        for i in range(n):
            for j in range(n):
                if not (0 <= add_table[i][j] < n): return [False, False]
                if not (0 <= mul_table[i][j] < n): return [False, False]
                
        # Check commutativity of addition
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]:
                    return [False, False]
                    
        # Check associativity of addition
        for i, j, k in itertools.product(range(n), repeat=3):
            if add_table[i][add_table[j][k]] != add_table[add_table[i][j]][k]:
                return [False, False]
                
        # Find additive identity
        zero = -1
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero == -1:
            return [False, False]
            
        # Check additive inverses
        for i in range(n):
            if not any(add_table[i][j] == zero for j in range(n)):
                return [False, False]
                
        # Check commutativity of multiplication
        for i in range(n):
            for j in range(n):
                if mul_table[i][j] != mul_table[j][i]:
                    return [False, False]
                    
        # Check associativity of multiplication
        for i, j, k in itertools.product(range(n), repeat=3):
            if mul_table[i][mul_table[j][k]] != mul_table[mul_table[i][j]][k]:
                return [False, False]
                
        # Check distributivity
        for i, j, k in itertools.product(range(n), repeat=3):
            if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                return [False, False]
                
        # If all checks pass, R is a finite commutative ring, hence Artinian.
        h1 = True
        
        # Find the set of non-zero-divisors S
        S = []
        for s in range(n):
            is_nzd = True
            for a in range(n):
                if mul_table[s][a] == zero and a != zero:
                    is_nzd = False
                    break
            if is_nzd:
                S.append(s)
                
        # The conclusion is that S^{-1}R is isomorphic to R.
        # For a finite commutative ring, if S is non-empty, then R has an identity,
        # S is exactly the set of units, and S^{-1}R is isomorphic to R.
        # If S is empty, the localization S^{-1}R is undefined (or empty), 
        # which is not isomorphic to R.
        # Thus, the conclusion fails if and only if S is empty.
        neg_q = (len(S) == 0)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]