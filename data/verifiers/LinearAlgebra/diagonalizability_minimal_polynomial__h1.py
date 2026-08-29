import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        A = witness
        if hasattr(A, 'is_square') and A.is_square:
            h1_ok = True
    except Exception:
        pass

    if not h1_ok:
        return [False, False]

    try:
        # The conjecture claims: A is diagonalizable over F iff m(x) splits into distinct linear factors over F.
        # This is true if F is a field and A is a matrix over F.
        # It fails if A has entries outside F (but eigenvalues in F), or if F is a ring (like ZZ) instead of a field.
        
        if A.is_diagonalizable():
            evs = list(A.eigenvals().keys())
            
            def in_QQ(val):
                try:
                    sympy.Rational(val)
                    return True
                except Exception:
                    return False
            
            def in_RR(val):
                try:
                    return bool(val.is_real)
                except Exception:
                    return False
                    
            def is_int(val):
                try:
                    return bool(val.is_integer)
                except Exception:
                    return False

            # Check Counterexample Type 1: F = ZZ (F is a ring, not a field)
            if all(is_int(ev) for ev in evs) and all(is_int(entry) for entry in A):
                # If all eigenspaces are 1D, we can easily check diagonalizability over ZZ
                if len(evs) == A.shape[0]:
                    P_cols = []
                    for ev in evs:
                        M = A - ev * sympy.eye(A.shape[0])
                        ns = M.nullspace()
                        for v in ns:
                            lcm = 1
                            for val in v:
                                if val != 0:
                                    lcm = sympy.lcm(lcm, sympy.Rational(val).q)
                            v_int = v * lcm
                            g = 0
                            for val in v_int:
                                g = sympy.gcd(g, sympy.Rational(val).p)
                            if g != 0:
                                v_prim = v_int / g
                            else:
                                v_prim = v_int
                            P_cols.append(v_prim)
                    if len(P_cols) == A.shape[0]:
                        P = sympy.Matrix.hstack(*P_cols)
                        # If the determinant of the eigenvector matrix is not ±1, 
                        # it is not invertible over ZZ, hence not diagonalizable over ZZ.
                        if abs(P.det()) != 1:
                            neg_q_ok = True

            # Check Counterexample Type 2: F = QQ (A is not a matrix over F)
            if not neg_q_ok:
                if all(in_QQ(ev) for ev in evs):
                    if any(not in_QQ(entry) for entry in A):
                        neg_q_ok = True

            # Check Counterexample Type 3: F = RR (A is not a matrix over F)
            if not neg_q_ok:
                if all(in_RR(ev) for ev in evs):
                    if any(not in_RR(entry) for entry in A):
                        neg_q_ok = True
                        
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: m(x) is the minimal polynomial of A",
    "¬Q: A is not diagonalizable over F but m(x) splits into distinct linear factors over F"
]

N_HYP = 1
NEG_Q_INDEX = 1