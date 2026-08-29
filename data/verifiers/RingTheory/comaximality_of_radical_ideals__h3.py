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

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (n, add_table, mul_table, I, J)
    where:
      - n is the number of elements in the ring (elements are 0, 1, ..., n-1)
      - add_table is an n x n list of lists for addition
      - mul_table is an n x n list of lists for multiplication
      - I is a list of elements in ideal I
      - J is a list of elements in ideal J
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 5:
            return [False, False, False]
        n, add_table, mul_table, I, J = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative ring
    try:
        h1 = True
        if not isinstance(n, int) or n <= 0 or n > 100:
            h1 = False
        else:
            if len(add_table) != n or any(len(row) != n for row in add_table):
                h1 = False
            elif any(not isinstance(val, int) or val < 0 or val >= n for row in add_table for val in row):
                h1 = False
            
            if len(mul_table) != n or any(len(row) != n for row in mul_table):
                h1 = False
            elif any(not isinstance(val, int) or val < 0 or val >= n for row in mul_table for val in row):
                h1 = False
            
            if h1:
                # Commutativity of addition
                for i in range(n):
                    for j in range(i, n):
                        if add_table[i][j] != add_table[j][i]:
                            h1 = False
                            break
                    if not h1: break
                
                # Identity 0 for addition
                if h1:
                    for i in range(n):
                        if add_table[i][0] != i:
                            h1 = False
                            break
                
                # Additive inverses
                if h1:
                    for i in range(n):
                        if 0 not in add_table[i]:
                            h1 = False
                            break
                
                # Associativity of addition
                if h1:
                    for i in range(n):
                        for j in range(n):
                            for k in range(n):
                                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                                    h1 = False
                                    break
                            if not h1: break
                        if not h1: break

                # Commutativity of multiplication
                if h1:
                    for i in range(n):
                        for j in range(i, n):
                            if mul_table[i][j] != mul_table[j][i]:
                                h1 = False
                                break
                        if not h1: break

                # Associativity of multiplication
                if h1:
                    for i in range(n):
                        for j in range(n):
                            for k in range(n):
                                if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                                    h1 = False
                                    break
                            if not h1: break
                        if not h1: break

                # Distributivity
                if h1:
                    for i in range(n):
                        for j in range(n):
                            for k in range(n):
                                if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                                    h1 = False
                                    break
                            if not h1: break
                        if not h1: break
    except Exception:
        h1 = False

    # H2: I and J are ideals of R
    try:
        h2 = True
        if not h1:
            h2 = False
        else:
            I_set = set(I)
            J_set = set(J)
            if not I_set.issubset(range(n)) or not J_set.issubset(range(n)):
                h2 = False
            elif 0 not in I_set or 0 not in J_set:
                h2 = False
            else:
                for ideal in [I_set, J_set]:
                    for a in ideal:
                        for b in ideal:
                            if add_table[a][b] not in ideal:
                                h2 = False
                                break
                        if not h2: break
                        
                        # Additive inverse
                        inv_a = -1
                        for x in range(n):
                            if add_table[a][x] == 0:
                                inv_a = x
                                break
                        if inv_a not in ideal:
                            h2 = False
                            break
                        
                        # Scalar multiplication
                        for r in range(n):
                            if mul_table[r][a] not in ideal:
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
    except Exception:
        h2 = False

    # neg_Q: Comaximality equivalence fails
    try:
        neg_q = False
        if h1 and h2:
            I_set = set(I)
            J_set = set(J)
            
            # I + J
            I_plus_J = set(add_table[a][b] for a in I_set for b in J_set)
            I_J_comaximal = (len(I_plus_J) == n)
            
            # Radical of I
            rad_I = set()
            for x in range(n):
                curr = x
                for _ in range(n):
                    if curr in I_set:
                        rad_I.add(x)
                        break
                    curr = mul_table[curr][x]
            
            # Radical of J
            rad_J = set()
            for x in range(n):
                curr = x
                for _ in range(n):
                    if curr in J_set:
                        rad_J.add(x)
                        break
                    curr = mul_table[curr][x]
            
            # rad(I) + rad(J)
            rad_I_plus_rad_J = set(add_table[a][b] for a in rad_I for b in rad_J)
            rad_comaximal = (len(rad_I_plus_rad_J) == n)
            
            # The conjecture states they are equivalent. We want the negation (they are not equivalent).
            neg_q = (I_J_comaximal != rad_comaximal)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "¬Q: I and J are comaximal if and only if their radicals are comaximal is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2