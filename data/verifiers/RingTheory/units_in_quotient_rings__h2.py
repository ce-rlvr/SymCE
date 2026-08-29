import itertools
import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
# We provide a helper to easily construct finite rings Z/nZ, as well as some pre-built ones.
def make_Zn(n):
    """
    Helper to create the ring Z/nZ.
    Returns a tuple: (n, R_add, R_mul)
    where R_add and R_mul are n x n lists representing the addition and multiplication tables.
    """
    R_add = [[(i + j) % n for j in range(n)] for i in range(n)]
    R_mul = [[(i * j) % n for j in range(n)] for i in range(n)]
    return n, R_add, R_mul

Z2_ring = make_Zn(2)
Z3_ring = make_Zn(3)
Z4_ring = make_Zn(4)
Z6_ring = make_Zn(6)

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: u is a unit in R",
    "¬Q: The coset u + I is NOT a unit in the quotient ring R/I (e.g. I is not an ideal, or R/I is the zero ring)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple: (n, R_add, R_mul, I, u)
      - n: int, size of the finite ring
      - R_add: list of lists, n x n addition table
      - R_mul: list of lists, n x n multiplication table
      - I: list of ints, a subset of the ring representing I
      - u: int, an element of the ring
    """
    try:
        if not (isinstance(witness, tuple) and len(witness) == 5):
            return [False, False, False]
        n, R_add, R_mul, I, u = witness
    except Exception:
        return [False, False, False]

    def check_H1():
        if not isinstance(n, int) or n <= 0: return False
        if not isinstance(R_add, list) or len(R_add) != n: return False
        if not isinstance(R_mul, list) or len(R_mul) != n: return False
        
        for row in R_add:
            if not isinstance(row, list) or len(row) != n: return False
        for row in R_mul:
            if not isinstance(row, list) or len(row) != n: return False
            
        for i in range(n):
            for j in range(n):
                if not isinstance(R_add[i][j], int) or not (0 <= R_add[i][j] < n): return False
                if not isinstance(R_mul[i][j], int) or not (0 <= R_mul[i][j] < n): return False

        # Addition is commutative
        for i in range(n):
            for j in range(n):
                if R_add[i][j] != R_add[j][i]: return False
                
        # Addition is associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if R_add[R_add[i][j]][k] != R_add[i][R_add[j][k]]: return False
                    
        # Find additive identity
        zero = None
        for i in range(n):
            if all(R_add[i][j] == j and R_add[j][i] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False
            
        # Additive inverses exist
        for i in range(n):
            if not any(R_add[i][j] == zero for j in range(n)): return False
            
        # Multiplication is associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if R_mul[R_mul[i][j]][k] != R_mul[i][R_mul[j][k]]: return False
                    
        # Distributive laws
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if R_mul[i][R_add[j][k]] != R_add[R_mul[i][j]][R_mul[i][k]]: return False
                    if R_mul[R_add[i][j]][k] != R_add[R_mul[i][k]][R_mul[j][k]]: return False
                    
        # Multiplicative identity exists
        has_id = False
        for i in range(n):
            if all(R_mul[i][j] == j and R_mul[j][i] == j for j in range(n)):
                has_id = True
                break
        if not has_id: return False
        
        return True

    def check_H2():
        if not isinstance(u, int) or not (0 <= u < n): return False
        id_R = None
        for i in range(n):
            if all(R_mul[i][j] == j and R_mul[j][i] == j for j in range(n)):
                id_R = i
                break
        if id_R is None: return False
        
        # Check if u has a two-sided inverse
        for v in range(n):
            if R_mul[u][v] == id_R and R_mul[v][u] == id_R:
                return True
        return False

    def check_neg_Q():
        if not isinstance(I, list): return True
        if not all(isinstance(x, int) and 0 <= x < n for x in I): return True
        if not I: return True
        
        zero = None
        for i in range(n):
            if all(R_add[i][j] == j and R_add[j][i] == j for j in range(n)):
                zero = i
                break
        if zero is None: return True
        
        # Check if I is a subgroup under addition
        for x in I:
            for y in I:
                if R_add[x][y] not in I: return True
                
        for x in I:
            inv_x = None
            for y in range(n):
                if R_add[x][y] == zero and R_add[y][x] == zero:
                    inv_x = y
                    break
            if inv_x not in I: return True
            
        # Check if I is an ideal (absorbing under multiplication)
        for x in I:
            for r in range(n):
                if R_mul[r][x] not in I: return True
                if R_mul[x][r] not in I: return True
                
        id_R = None
        for i in range(n):
            if all(R_mul[i][j] == j and R_mul[j][i] == j for j in range(n)):
                id_R = i
                break
        if id_R is None: return True
                
        def get_coset(x):
            return tuple(sorted(set(R_add[x][i] for i in I)))
            
        coset_1 = get_coset(id_R)
        coset_0 = get_coset(zero)
        
        # If R/I is the zero ring, it has no units (under the strict 1 != 0 definition)
        if coset_1 == coset_0:
            return True
            
        coset_u = get_coset(u)
        has_inverse = False
        for v in range(n):
            coset_v = get_coset(v)
            prod_uv = get_coset(R_mul[u][v])
            prod_vu = get_coset(R_mul[v][u])
            if prod_uv == coset_1 and prod_vu == coset_1:
                has_inverse = True
                break
                
        return not has_inverse

    try:
        h1 = check_H1()
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2()
    except Exception:
        h2 = False
        
    try:
        nq = check_neg_Q()
    except Exception:
        nq = False
        
    return [h1, h2, nq]