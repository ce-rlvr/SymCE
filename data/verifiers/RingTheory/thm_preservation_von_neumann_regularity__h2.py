import sympy
from sympy import eye, zeros, Rational, Integer

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_ring(ring):
    """
    Attempts to parse a ring into a finite list of elements and its addition/multiplication tables.
    Supports integers n (representing Z/nZ), tuples (n, add_table, mul_table), and finite iterables.
    """
    if isinstance(ring, int):
        if ring >= 1:
            n = ring
            add = [[(i + j) % n for j in range(n)] for i in range(n)]
            mul = [[(i * j) % n for j in range(n)] for i in range(n)]
            return list(range(n)), add, mul
        return None, None, None
        
    if isinstance(ring, tuple) and len(ring) == 3:
        n, add, mul = ring
        if isinstance(n, int) and isinstance(add, list) and isinstance(mul, list):
            return list(range(n)), add, mul
            
    if isinstance(ring, (list, tuple, set)):
        elements = list(ring)
        n = len(elements)
        if n == 0:
            return None, None, None
        add = [[None] * n for _ in range(n)]
        mul = [[None] * n for _ in range(n)]
        try:
            for i in range(n):
                for j in range(n):
                    s = elements[i] + elements[j]
                    p = elements[i] * elements[j]
                    if s not in elements or p not in elements:
                        return None, None, None
                    add[i][j] = elements.index(s)
                    mul[i][j] = elements.index(p)
            return list(range(n)), add, mul
        except Exception:
            pass
            
    return None, None, None

def is_ring(ring):
    """
    Checks if the given object satisfies the axioms of a ring.
    """
    if ring in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
        return True
    if hasattr(ring, 'is_Ring') and ring.is_Ring:
        return True
    if hasattr(ring, 'is_ring') and ring.is_ring:
        return True
    
    elements, add, mul = parse_ring(ring)
    if elements is None:
        return False
    n = len(elements)
    
    # Commutativity of addition
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            
    # Associativity of addition
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                
    # Identity of addition
    id_add = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            id_add = i
            break
    if id_add == -1: return False
    
    # Inverses of addition
    for i in range(n):
        if not any(add[i][j] == id_add for j in range(n)): return False
        
    # Associativity of multiplication
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                
    # Distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
                
    return True

def is_von_neumann_regular(ring):
    """
    Checks if the ring is von Neumann regular (for all a, exists x such that a*x*a = a).
    """
    if ring in [sympy.QQ, sympy.RR, sympy.CC]:
        return True
    if ring == sympy.ZZ:
        return False
    if hasattr(ring, 'is_Field') and ring.is_Field:
        return True
        
    elements, add, mul = parse_ring(ring)
    if elements is None:
        return False
    n = len(elements)
    
    for a in range(n):
        found = False
        for x in range(n):
            if mul[mul[a][x]][a] == a:
                found = True
                break
        if not found:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        R, S = witness
        
        try:
            h1 = is_ring(R) and is_ring(S)
        except Exception:
            h1 = False
            
        try:
            h2 = is_von_neumann_regular(R)
        except Exception:
            h2 = False
            
        try:
            neg_q = not is_von_neumann_regular(S)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: R is a von Neumann regular ring",
    "¬Q: S is not a von Neumann regular ring"
]

N_HYP = 2
NEG_Q_INDEX = 2