import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_field(subset, add_table, mul_table):
    n_sub = len(subset)
    if n_sub < 2:
        return False
    
    # Check closure
    for a in subset:
        for b in subset:
            if add_table[a][b] not in subset:
                return False
            if mul_table[a][b] not in subset:
                return False
                
    # Check commutativity
    for a in subset:
        for b in subset:
            if add_table[a][b] != add_table[b][a]:
                return False
            if mul_table[a][b] != mul_table[b][a]:
                return False
                
    # Check associativity and distributivity
    for a in subset:
        for b in subset:
            for c in subset:
                if add_table[add_table[a][b]][c] != add_table[a][add_table[b][c]]:
                    return False
                if mul_table[mul_table[a][b]][c] != mul_table[a][mul_table[b][c]]:
                    return False
                if mul_table[a][add_table[b][c]] != add_table[mul_table[a][b]][mul_table[a][c]]:
                    return False
                    
    # Find zero
    zero = None
    for e in subset:
        if all(add_table[e][a] == a for a in subset):
            zero = e
            break
    if zero is None:
        return False
        
    # Check additive inverses
    for a in subset:
        if not any(add_table[a][b] == zero for b in subset):
            return False
            
    # Find one
    one = None
    for e in subset:
        if all(mul_table[e][a] == a for a in subset):
            one = e
            break
    if one is None or one == zero:
        return False
        
    # Check multiplicative inverses
    for a in subset:
        if a != zero:
            if not any(mul_table[a][b] == one for b in subset):
                return False
                
    return True

def conditions(witness) -> list[bool]:
    """
    witness should be a tuple: (F_order, add_table, mul_table, p, n, m)
    where add_table and mul_table are 2D lists representing the ring operations on {0, 1, ..., F_order - 1}.
    Alternatively, witness can be (p, n, m) and F will be Z_{p^n}.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            p, n, m = witness
            if not (isinstance(p, int) and isinstance(n, int) and isinstance(m, int)):
                return [False, False, False, False]
            if p**n > 1000 or p**n < 1:
                return [False, False, False, False]
            F_order = p ** n
            add_table = [[(i + j) % F_order for j in range(F_order)] for i in range(F_order)]
            mul_table = [[(i * j) % F_order for j in range(F_order)] for i in range(F_order)]
        elif isinstance(witness, tuple) and len(witness) == 6:
            F_order, add_table, mul_table, p, n, m = witness
        else:
            return [False, False, False, False]
            
        if int(F_order) != F_order or int(n) != n or int(m) != m or int(p) != p:
            return [False, False, False, False]
        F_order = int(F_order)
        n = int(n)
        m = int(m)
        p = int(p)
    except Exception:
        return [False, False, False, False]
        
    # H_1: The order of F is p^n
    try:
        h1 = (n >= 0) and (F_order == p ** n)
        if h1:
            if len(add_table) != F_order or len(mul_table) != F_order:
                h1 = False
            else:
                for row in add_table:
                    if len(row) != F_order or any(not isinstance(x, int) or x < 0 or x >= F_order for x in row):
                        h1 = False
                        break
                for row in mul_table:
                    if len(row) != F_order or any(not isinstance(x, int) or x < 0 or x >= F_order for x in row):
                        h1 = False
                        break
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(sympy.isprime(p))
    except Exception:
        h2 = False
        
    # H_3: m is a positive integer
    try:
        h3 = (m > 0)
    except Exception:
        h3 = False
        
    # ¬Q: F contains a subfield of order p^m if and only if m divides n (must fail)
    try:
        target_order = p ** m
        has_sub = False
        if target_order <= F_order:
            if math.comb(F_order, target_order) > 100000:
                neg_q = False
            else:
                elements = list(range(F_order))
                for subset in itertools.combinations(elements, target_order):
                    if is_field(subset, add_table, mul_table):
                        has_sub = True
                        break
                m_divides_n = (n % m == 0)
                neg_q = (has_sub != m_divides_n)
        else:
            m_divides_n = (n % m == 0)
            neg_q = (has_sub != m_divides_n)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The order of F is p^n",
    "H_2: p is a prime number",
    "H_3: m is a positive integer",
    "¬Q: The equivalence (F contains a subfield of order p^m iff m divides n) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3