import math
import itertools
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    res = [False, False, False]
    
    try:
        if not isinstance(witness, Matrix):
            return res
        n = witness.shape[0]
        if n != witness.shape[1]:
            return res
            
        # Convert to a list of lists of Python ints.
        # If the witness contains non-integers (e.g. symbols or floats), this will raise an exception.
        # This ensures we are working over Z, where the characteristic is 0.
        A_list = [[int(witness[i, j]) for j in range(n)] for i in range(n)]
    except Exception:
        return res

    # H_1: The characteristic of F is not 2
    # Since the witness is an integer matrix, we consider it as a form over Z (or Q).
    # The characteristic of Z is 0, which is not 2.
    res[0] = True

    # H_2: B is a symmetric bilinear form on V
    try:
        is_sym = True
        for i in range(n):
            for j in range(n):
                if A_list[i][j] != A_list[j][i]:
                    is_sym = False
                    break
        res[1] = is_sym
    except Exception:
        pass

    # ¬Q: B is not diagonalizable
    # We check if there exists a unimodular matrix P such that P^T * A * P is diagonal.
    try:
        diag = False
        if n == 1:
            diag = True
        else:
            is_zero = all(A_list[i][j] == 0 for i in range(n) for j in range(n))
            if is_zero:
                diag = True
            else:
                if n == 2:
                    limit = 200
                elif n == 3:
                    limit = 15
                elif n == 4:
                    limit = 5
                else:
                    limit = 3

                candidates = []
                ranges = [range(-limit, limit + 1)] * n
                
                for v_tuple in itertools.product(*ranges):
                    g = v_tuple[0]
                    for x in v_tuple[1:]:
                        g = math.gcd(g, x)
                    if g != 1:
                        continue
                        
                    Av = [sum(A_list[i][j] * v_tuple[j] for j in range(n)) for i in range(n)]
                    
                    g_Av = Av[0]
                    for x in Av[1:]:
                        g_Av = math.gcd(g_Av, x)
                        
                    q = sum(v_tuple[i] * Av[i] for i in range(n))
                    
                    if q == 0:
                        if all(x == 0 for x in Av):
                            candidates.append(v_tuple)
                        continue
                        
                    if abs(q) == abs(g_Av):
                        candidates.append(v_tuple)
                        
                if n == 2:
                    diag = len(candidates) > 0
                else:
                    cand_Av = []
                    for v in candidates:
                        Av = [sum(A_list[i][j] * v[j] for j in range(n)) for i in range(n)]
                        cand_Av.append((v, Av))
                        
                    if len(cand_Av) > 200:
                        cand_Av.sort(key=lambda x: sum(vi**2 for vi in x[0]))
                        cand_Av = cand_Av[:200]
                        
                    def search(basis_v, basis_Av):
                        if len(basis_v) == n:
                            P = Matrix(basis_v)
                            return abs(P.det()) == 1
                            
                        for v, Av in cand_Av:
                            ok = True
                            for b_Av in basis_Av:
                                dot = sum(v[i] * b_Av[i] for i in range(n))
                                if dot != 0:
                                    ok = False
                                    break
                            if ok:
                                if search(basis_v + [v], basis_Av + [Av]):
                                    return True
                        return False

                    diag = search([], [])
                    
        res[2] = not diag
    except Exception:
        pass

    return res

CONDITION_LABELS = [
    "H_1: The characteristic of F is not 2",
    "H_2: B is a symmetric bilinear form on V",
    "¬Q: B is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2