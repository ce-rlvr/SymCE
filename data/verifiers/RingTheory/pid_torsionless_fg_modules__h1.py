import itertools
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def is_valid_ring(R_add, R_mul):
    if not isinstance(R_add, list) or not isinstance(R_mul, list): return False
    N = len(R_add)
    if N < 2 or N > 50: return False
    if len(R_mul) != N: return False
    for row in R_add + R_mul:
        if not isinstance(row, list): return False
        if len(row) != N: return False
        for val in row:
            if not isinstance(val, int): return False
            if not (0 <= val < N): return False
            
    # Check R_add is commutative group with identity 0
    for i in range(N):
        if R_add[i][0] != i or R_add[0][i] != i: return False
        for j in range(N):
            if R_add[i][j] != R_add[j][i]: return False
            for k in range(N):
                if R_add[R_add[i][j]][k] != R_add[i][R_add[j][k]]: return False
                
    # Check inverses
    for i in range(N):
        has_inv = False
        for j in range(N):
            if R_add[i][j] == 0:
                has_inv = True
                break
        if not has_inv: return False
        
    # Check R_mul is commutative monoid with identity 1
    for i in range(N):
        if R_mul[i][1] != i or R_mul[1][i] != i: return False
        for j in range(N):
            if R_mul[i][j] != R_mul[j][i]: return False
            for k in range(N):
                if R_mul[R_mul[i][j]][k] != R_mul[i][R_mul[j][k]]: return False
                
    # Check distributivity
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if R_mul[i][R_add[j][k]] != R_add[R_mul[i][j]][R_mul[i][k]]: return False
                
    return True

def is_valid_module(R_add, R_mul, M_add, rmul):
    if not isinstance(M_add, list) or not isinstance(rmul, list): return False
    N = len(R_add)
    K = len(M_add)
    if K < 1 or K > 50: return False
    if len(rmul) != N: return False
    for row in M_add:
        if not isinstance(row, list): return False
        if len(row) != K: return False
        for val in row:
            if not isinstance(val, int): return False
            if not (0 <= val < K): return False
    for row in rmul:
        if not isinstance(row, list): return False
        if len(row) != K: return False
        for val in row:
            if not isinstance(val, int): return False
            if not (0 <= val < K): return False
            
    # Check M_add is commutative group with identity 0
    for i in range(K):
        if M_add[i][0] != i or M_add[0][i] != i: return False
        for j in range(K):
            if M_add[i][j] != M_add[j][i]: return False
            for k in range(K):
                if M_add[M_add[i][j]][k] != M_add[i][M_add[j][k]]: return False
                
    # Check inverses
    for i in range(K):
        has_inv = False
        for j in range(K):
            if M_add[i][j] == 0:
                has_inv = True
                break
        if not has_inv: return False
        
    # Check module axioms
    for r in range(N):
        for m1 in range(K):
            for m2 in range(K):
                if rmul[r][M_add[m1][m2]] != M_add[rmul[r][m1]][rmul[r][m2]]: return False
                
    for r1 in range(N):
        for r2 in range(N):
            for m in range(K):
                if rmul[R_add[r1][r2]][m] != M_add[rmul[r1][m]][rmul[r2][m]]: return False
                if rmul[R_mul[r1][r2]][m] != rmul[r1][rmul[r2][m]]: return False
                
    for m in range(K):
        if rmul[1][m] != m: return False
        
    return True

def is_torsion_free(R_add, R_mul, M_add, rmul):
    N = len(R_add)
    K = len(M_add)
    regular_elements = []
    for r in range(N):
        is_regular = True
        for s in range(1, N):
            if R_mul[r][s] == 0:
                is_regular = False
                break
        if is_regular:
            regular_elements.append(r)
            
    for m in range(1, K):
        for r in regular_elements:
            if rmul[r][m] == 0:
                return False
    return True

def is_injective_to_double_dual(R_add, R_mul, M_add, rmul):
    N = len(R_add)
    K = len(M_add)
    if N**K > 200000:
        raise ValueError("Witness too large to verify in time")
        
    M_star = []
    for f in itertools.product(range(N), repeat=K):
        if f[0] != 0: continue
        valid = True
        for m1 in range(K):
            fm1 = f[m1]
            for m2 in range(m1, K):
                if f[M_add[m1][m2]] != R_add[fm1][f[m2]]:
                    valid = False
                    break
            if not valid: break
        if not valid: continue
        
        for r in range(N):
            for m in range(K):
                if f[rmul[r][m]] != R_mul[r][f[m]]:
                    valid = False
                    break
            if not valid: break
        if valid:
            M_star.append(f)
            
    for m in range(1, K):
        m_is_nonzero_in_double_dual = False
        for f in M_star:
            if f[m] != 0:
                m_is_nonzero_in_double_dual = True
                break
        if not m_is_nonzero_in_double_dual:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_add = witness.get('R_add')
            R_mul = witness.get('R_mul')
            M_add = witness.get('M_add')
            rmul = witness.get('rmul')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            R_add, R_mul, M_add, rmul = witness
        else:
            return [False, False]
            
        if R_add is None or R_mul is None or M_add is None or rmul is None:
            return [False, False]
            
        if not is_valid_ring(R_add, R_mul):
            return [False, False]
        if not is_valid_module(R_add, R_mul, M_add, rmul):
            return [False, False]
            
        # H1: M is a finitely generated R-module
        # Since M is finite, it is automatically finitely generated by its elements.
        h1_ok = True
        
        torsion_free = is_torsion_free(R_add, R_mul, M_add, rmul)
        injective = is_injective_to_double_dual(R_add, R_mul, M_add, rmul)
        
        # The conclusion is "injective iff torsion-free".
        # We want the conclusion to FAIL, so they must have different truth values.
        neg_q_ok = bool(injective != torsion_free)
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "¬Q: M is torsion-free but M -> M** is not injective, or vice versa"
]

N_HYP = 1
NEG_Q_INDEX = 1