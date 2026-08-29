import sympy
from sympy import Matrix, eye
from collections import deque
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

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

def conditions(witness):
    # The witness can be just the subgroup H, or a tuple (A, B, H)
    if isinstance(witness, tuple) and len(witness) == 3:
        A_wit, B_wit, H = witness
    else:
        A_wit = Matrix([[1, 2], [0, 1]])
        B_wit = Matrix([[1, 0], [2, 1]])
        H = witness

    try:
        h1 = bool(A_wit == Matrix([[1, 2], [0, 1]]))
    except Exception:
        h1 = False

    try:
        h2 = bool(B_wit == Matrix([[1, 0], [2, 1]]))
    except Exception:
        h2 = False

    try:
        def check_is_f2(H):
            if H.__class__.__name__ == 'FreeGroup':
                return len(H.generators) == 2
                
            if isinstance(H, set):
                H = list(H)
                
            if not isinstance(H, (list, tuple)):
                return False
                
            if len(H) != 2:
                return False
                
            X, Y = H
            
            # Check if they are Sanov matrices which are known to generate F_2
            def get_sanov_mn(M1, M2):
                try:
                    if M1[0,0] == 1 and M1[1,1] == 1 and M1[1,0] == 0:
                        m = M1[0,1]
                        if M2[0,0] == 1 and M2[1,1] == 1 and M2[0,1] == 0:
                            n = M2[1,0]
                            return m, n
                except Exception:
                    pass
                return None, None

            m, n = get_sanov_mn(X, Y)
            if m is None:
                m, n = get_sanov_mn(Y, X)
                
            if m is not None and n is not None:
                if abs(m) >= 2 and abs(n) >= 2:
                    return True
                if abs(m) == 1 and abs(n) == 1:
                    return False
                    
            # Check for commutativity (F_2 is not abelian)
            try:
                if X*Y == Y*X:
                    return False
            except Exception:
                return False
                
            # Check for short relations (length up to 6) using BFS
            try:
                X_inv = X.inv() if hasattr(X, 'inv') else X**-1
                Y_inv = Y.inv() if hasattr(Y, 'inv') else Y**-1
                I = X * X_inv
                gens = [X, Y, X_inv, Y_inv]
                inverses = {0: 2, 1: 3, 2: 0, 3: 1}
                
                q = deque([(I, -1, 0)])
                while q:
                    mat, last_idx, length = q.popleft()
                    if length > 0 and mat == I:
                        return False
                    if length < 6:
                        for i, g in enumerate(gens):
                            if last_idx != -1 and inverses[last_idx] == i:
                                continue
                            q.append((mat * g, i, length + 1))
            except Exception:
                return False
                
            # If no short relations are found, we conservatively assume it might be F_2
            return True

        is_f2 = check_is_f2(H)
        neg_q = not is_f2
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = ['H_1: A is the first matrix', 'H_2: B is the second matrix', '¬Q: H is not isomorphic to the free group of rank 2']
N_HYP = 2
NEG_Q_INDEX = 2