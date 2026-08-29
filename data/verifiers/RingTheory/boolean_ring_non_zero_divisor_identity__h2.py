import itertools
import sympy
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    Expected witness format: (n, add_table, mul_table, a)
      - n: int, size of the ring
      - add_table: n x n list of lists for addition
      - mul_table: n x n list of lists for multiplication
      - a: int, the element 'a' in the ring (0 <= a < n)
    """
    try:
        n, add_table, mul_table, a = witness
        
        if not isinstance(n, int) or n <= 0:
            return [False, False]
        if not isinstance(a, int) or not (0 <= a < n):
            return [False, False]
        if len(add_table) != n or any(len(row) != n for row in add_table):
            return [False, False]
        if len(mul_table) != n or any(len(row) != n for row in mul_table):
            return [False, False]
            
        # H1: R is a Boolean ring
        h1 = True
        
        # Addition commutative
        for i, j in itertools.product(range(n), repeat=2):
            if add_table[i][j] != add_table[j][i]:
                h1 = False
                break
                
        # Addition associative
        if h1:
            for i, j, k in itertools.product(range(n), repeat=3):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                    h1 = False
                    break
                    
        # Addition identity
        zero = -1
        if h1:
            for i in range(n):
                if all(add_table[i][j] == j for j in range(n)):
                    zero = i
                    break
            if zero == -1:
                h1 = False
                
        # Addition inverses
        if h1:
            for i in range(n):
                if not any(add_table[i][j] == zero for j in range(n)):
                    h1 = False
                    break
                    
        # Multiplication associative
        if h1:
            for i, j, k in itertools.product(range(n), repeat=3):
                if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                    h1 = False
                    break
                    
        # Distributive
        if h1:
            for i, j, k in itertools.product(range(n), repeat=3):
                if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                    h1 = False
                    break
                if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                    h1 = False
                    break
                    
        # Boolean (x^2 = x for all x)
        if h1:
            for i in range(n):
                if mul_table[i][i] != i:
                    h1 = False
                    break
                    
        # neg_Q: a is NOT the multiplicative identity
        # The conclusion states R has a multiplicative identity and a is that identity.
        # This fails if there is any element x such that a*x != x or x*a != x.
        neg_q = False
        for i in range(n):
            if mul_table[a][i] != i or mul_table[i][a] != i:
                neg_q = True
                break
                
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: a is not the multiplicative identity of R"
]

N_HYP = 1
NEG_Q_INDEX = 1