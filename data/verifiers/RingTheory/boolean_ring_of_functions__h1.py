import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_boolean_ring(elems, add, mul):
    n = len(elems)
    if n < 2:
        return False
    
    # Check closure
    for i in range(n):
        for j in range(n):
            if add[i][j] not in range(n) or mul[i][j] not in range(n):
                return False
                
    # Check abelian group for add
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]:
                return False
                
    # Check associativity for add
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]:
                    return False
                    
    # Check identity for add
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1:
        return False
        
    # Check inverses for add
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)):
            return False
            
    # Check associativity for mul
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]:
                    return False
                    
    # Check distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]:
                    return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]:
                    return False
                    
    # Check Boolean property x^2 = x
    for i in range(n):
        if mul[i][i] != i:
            return False
            
    # Check identity for mul (Boolean rings are typically required to have 1 != 0)
    one = -1
    for i in range(n):
        if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
            one = i
            break
    if one == -1 or one == zero:
        return False
        
    return True

def conditions(witness):
    try:
        # Parse the witness. It can be a full specification (R_elems, R_add, R_mul, X_elems),
        # a tuple (R_elems, X_elems), an integer representing |X|, or just an iterable for X.
        if isinstance(witness, tuple) and len(witness) == 4:
            R_elems, R_add, R_mul, X_elems = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            R_elems, X_elems = witness
            if isinstance(R_elems, int):
                R_elems = [0, 1]
            R_add = [[0, 1], [1, 0]]
            R_mul = [[0, 0], [0, 1]]
        elif isinstance(witness, int):
            R_elems = [0, 1]
            R_add = [[0, 1], [1, 0]]
            R_mul = [[0, 0], [0, 1]]
            X_elems = list(range(witness))
        else:
            R_elems = [0, 1]
            R_add = [[0, 1], [1, 0]]
            R_mul = [[0, 0], [0, 1]]
            X_elems = list(witness)
            
        h1 = is_boolean_ring(R_elems, R_add, R_mul)
        
        # R^X is the set of all functions from X to R.
        # This is true by definition of our construction.
        h2 = True
        
        # Addition and multiplication on R^X are defined pointwise.
        # This is true by definition of our construction.
        h3 = True
        
        # The size of R^X is |R|^|X|.
        # If X is empty, |R^X| = 1.
        # A Boolean ring must have 1 != 0, so it must have at least 2 elements.
        # Thus, if |X| == 0, R^X is the trivial ring, which is not a Boolean ring.
        neg_q = (len(R_elems) ** len(X_elems)) < 2
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R^X is the set of all functions from X to R",
    "H_3: Addition and multiplication on R^X are defined pointwise",
    "¬Q: R^X is not a Boolean ring"
]

N_HYP = 3
NEG_Q_INDEX = 3