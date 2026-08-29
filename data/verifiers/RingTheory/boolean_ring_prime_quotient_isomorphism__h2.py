import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def is_ring(add_table, mul_table):
    try:
        n = len(add_table)
        if n == 0: return False
        if len(mul_table) != n: return False
        
        for i in range(n):
            if len(add_table[i]) != n or len(mul_table[i]) != n: return False
            
        for i in range(n):
            for j in range(n):
                if not (isinstance(add_table[i][j], int) and 0 <= add_table[i][j] < n): return False
                if not (isinstance(mul_table[i][j], int) and 0 <= mul_table[i][j] < n): return False

        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return False

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False

        zero = -1
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero == -1: return False

        for i in range(n):
            if not any(add_table[i][j] == zero for j in range(n)): return False

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return False

        return True
    except Exception:
        return False

def is_ideal(add_table, mul_table, P, zero):
    try:
        if not P: return False
        P_set = set(P)
        if zero not in P_set: return False
        n = len(add_table)
        
        for x in P_set:
            for y in P_set:
                if add_table[x][y] not in P_set: return False
                
        for x in P_set:
            inv_x = next(y for y in range(n) if add_table[x][y] == zero)
            if inv_x not in P_set: return False
            
        for x in P_set:
            for r in range(n):
                if mul_table[r][x] not in P_set: return False
                if mul_table[x][r] not in P_set: return False
                
        return True
    except Exception:
        return False

def extract_tables_and_P(witness):
    if isinstance(witness, dict):
        if 'add_table' in witness:
            return witness['add_table'], witness['mul_table'], witness['P']
        if 'R' in witness:
            R = witness['R']
            P = witness['P']
            if isinstance(R, dict):
                return R['add_table'], R['mul_table'], P
            if isinstance(R, tuple):
                return R[0], R[1], P
            return R.add_table, R.mul_table, P
    if isinstance(witness, tuple):
        if len(witness) == 3:
            return witness[0], witness[1], witness[2]
        if len(witness) == 2:
            R, P = witness
            if isinstance(R, dict):
                return R['add_table'], R['mul_table'], P
            if isinstance(R, tuple):
                return R[0], R[1], P
            return R.add_table, R.mul_table, P
    return witness.add_table, witness.mul_table, witness.P

def conditions(witness):
    try:
        add_table, mul_table, P = extract_tables_and_P(witness)
        n = len(add_table)
        
        # H1: R is a Boolean ring
        h1 = False
        if is_ring(add_table, mul_table):
            is_bool = True
            for i in range(n):
                if mul_table[i][i] != i:
                    is_bool = False
                    break
            if is_bool:
                h1 = True
                
        # Q: The quotient ring R/P is isomorphic to Z/2Z
        q = False
        zero = -1
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
                
        if zero != -1 and is_ideal(add_table, mul_table, P, zero):
            P_set = set(P)
            if n == 2 * len(P_set):
                is_z2 = True
                R_minus_P = [x for x in range(n) if x not in P_set]
                for a in R_minus_P:
                    for b in R_minus_P:
                        if mul_table[a][b] in P_set:
                            is_z2 = False
                            break
                    if not is_z2: break
                if is_z2:
                    q = True
                    
        neg_q = not q
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The quotient ring R/P is not isomorphic to Z/2Z"
]
N_HYP = 1
NEG_Q_INDEX = 1