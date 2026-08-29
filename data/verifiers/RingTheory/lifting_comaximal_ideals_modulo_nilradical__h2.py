import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_ring(n, add, mul):
    if type(n) is not int or n < 1: return False, None
    if type(add) is not list or len(add) != n: return False, None
    if type(mul) is not list or len(mul) != n: return False, None
    
    for i in range(n):
        if type(add[i]) is not list or len(add[i]) != n: return False, None
        if type(mul[i]) is not list or len(mul[i]) != n: return False, None
        for j in range(n):
            if type(add[i][j]) is not int or not (0 <= add[i][j] < n): return False, None
            if type(mul[i][j]) is not int or not (0 <= mul[i][j] < n): return False, None
            
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False, None
            if mul[i][j] != mul[j][i]: return False, None
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False, None
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False, None
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False, None
                
    zero = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False, None
    
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False, None
        
    return True, zero

def check_ideal(n, add, mul, zero, S):
    if not S: return False
    if not all(type(x) is int and 0 <= x < n for x in S): return False
    if zero not in S: return False
    for x in S:
        for y in S:
            if add[x][y] not in S: return False
    for x in S:
        inv_x = next((y for y in range(n) if add[x][y] == zero), None)
        if inv_x is None or inv_x not in S: return False
    for x in S:
        for r in range(n):
            if mul[x][r] not in S: return False
    return True

def check_comaximal_mod_nil(n, add, mul, zero, I, J):
    Nil = set()
    for x in range(n):
        curr = x
        is_nil = False
        for _ in range(n):
            if curr == zero:
                is_nil = True
                break
            curr = mul[curr][x]
        if is_nil:
            Nil.add(x)
            
    sum_IJN = set()
    for i in I:
        for j in J:
            ij = add[i][j]
            for k in Nil:
                sum_IJN.add(add[ij][k])
                
    return len(sum_IJN) == n

def check_not_comaximal(n, add, I, J):
    sum_IJ = set()
    for i in I:
        for j in J:
            sum_IJ.add(add[i][j])
    return len(sum_IJ) != n

def conditions(witness):
    """
    witness must be a dictionary or object representing a finite ring with:
      - 'n': int, the size of the ring
      - 'add': list of lists of ints, the addition table
      - 'mul': list of lists of ints, the multiplication table
      - 'I': list of ints, the elements of ideal I
      - 'J': list of ints, the elements of ideal J
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            add = witness['add']
            mul = witness['mul']
            I = set(witness['I'])
            J = set(witness['J'])
        else:
            n = witness.n
            add = witness.add
            mul = witness.mul
            I = set(witness.I)
            J = set(witness.J)
    except Exception:
        return [False, False, False, False]
        
    try:
        is_ring, zero = check_ring(n, add, mul)
    except Exception:
        is_ring, zero = False, None
        
    try:
        if is_ring:
            is_I_ideal = check_ideal(n, add, mul, zero, I)
            is_J_ideal = check_ideal(n, add, mul, zero, J)
            h2 = is_I_ideal and is_J_ideal
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        if is_ring and h2:
            h3 = check_comaximal_mod_nil(n, add, mul, zero, I, J)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    try:
        if is_ring and h2:
            neg_q = check_not_comaximal(n, add, I, J)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [is_ring, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: The image of I and the image of J in R/Nil(R) are comaximal",
    "¬Q: The ideals I and J are not comaximal in R"
]

N_HYP = 3
NEG_Q_INDEX = 3