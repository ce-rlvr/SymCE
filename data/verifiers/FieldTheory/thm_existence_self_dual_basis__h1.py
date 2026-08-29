import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def get_trace_matrix_from_coeffs(coeffs, n, p):
    """
    Computes the trace matrix of the algebra F_p[x]/(P(x)) using Newton's identities.
    coeffs: list of coefficients [a_n, a_{n-1}, ..., a_0] of P(x).
    """
    lead = coeffs[0]
    lead_inv = pow(lead, -1, p)
    a = [(c * lead_inv) % p for c in coeffs]
    
    S = [0] * (2*n - 1)
    S[0] = n % p
    for k in range(1, 2*n - 1):
        s = 0
        limit = min(k - 1, n)
        for i in range(1, limit + 1):
            s = (s + a[i] * S[k - i]) % p
        if k <= n:
            s = (s + k * a[k]) % p
        S[k] = (-s) % p
        
    M = []
    for i in range(n):
        M.append([S[i+j] for j in range(n)])
    return M

def extract_witness(witness):
    p = q = n = detM = None
    
    try:
        if hasattr(witness, 'domain') and hasattr(witness, 'degree'):
            p = int(witness.domain.char)
            try:
                q = int(witness.domain.order)
            except Exception:
                q = p
            n = int(witness.degree())
            
            coeffs = witness.all_coeffs()
            try:
                int_coeffs = [int(c) for c in coeffs]
                M = get_trace_matrix_from_coeffs(int_coeffs, n, p)
                detM = int(sympy.Matrix(M).det()) % p
            except Exception:
                S = [witness.domain.zero] * (2*n - 1)
                S[0] = witness.domain.convert(n)
                for k in range(1, 2*n - 1):
                    s = witness.domain.zero
                    limit = min(k - 1, n)
                    for i in range(1, limit + 1):
                        s += coeffs[i] * S[k - i]
                    if k <= n:
                        s += witness.domain.convert(k) * coeffs[k]
                    S[k] = -s
                M = [[S[i+j] for j in range(n)] for i in range(n)]
                detM = sympy.Matrix(M).det()
                
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                p, q, n, M_val = witness
                if isinstance(M_val, (int, sympy.Integer)):
                    detM = int(M_val)
                elif isinstance(M_val, list) and isinstance(M_val[0], int):
                    M_mat = get_trace_matrix_from_coeffs(M_val, n, p)
                    detM = int(sympy.Matrix(M_mat).det()) % p
                else:
                    detM = int(sympy.Matrix(M_val).det()) % p
            elif len(witness) == 3:
                p, q, n = witness
                
        elif isinstance(witness, dict):
            p = witness.get('p')
            q = witness.get('q')
            n = witness.get('n')
            M_val = witness.get('M')
            if M_val is not None:
                if isinstance(M_val, (int, sympy.Integer)):
                    detM = int(M_val)
                elif isinstance(M_val, list) and isinstance(M_val[0], int):
                    M_mat = get_trace_matrix_from_coeffs(M_val, n, p)
                    detM = int(sympy.Matrix(M_mat).det()) % p
                else:
                    detM = int(sympy.Matrix(M_val).det()) % p
            elif 'coeffs' in witness:
                M_mat = get_trace_matrix_from_coeffs(witness['coeffs'], n, p)
                detM = int(sympy.Matrix(M_mat).det()) % p
    except Exception:
        pass
        
    return p, q, n, detM

def is_square(detM, p, q):
    if detM == 0:
        return False
    if p == 2:
        return True
    
    if isinstance(detM, int):
        return pow(detM, (q - 1) // 2, p) == 1
    else:
        res = detM ** ((q - 1) // 2)
        try:
            if res == 1: return True
        except Exception: pass
        try:
            if (res - 1) == 0: return True
        except Exception: pass
        return False

def conditions(witness) -> list[bool]:
    p, q, n, detM = extract_witness(witness)
    
    # H_1: Let E be a finite extension of F of degree n.
    try:
        h1 = (n is not None and n >= 1)
    except Exception:
        h1 = False
        
    # H_2: Either p = 2, or both q and n are odd integers.
    try:
        h2 = (p == 2) or (q % 2 == 1 and n % 2 == 1)
    except Exception:
        h2 = False
        
    # ¬Q: There does NOT exist a basis of E over F that is self-dual with respect to the trace form.
    # A self-dual basis exists iff the trace matrix is non-degenerate and congruent to the identity matrix.
    try:
        if detM is None:
            neg_q = False
        else:
            if isinstance(detM, int):
                is_zero = (detM % p == 0)
                detM = detM % p
            else:
                is_zero = (detM == 0)
                
            if is_zero:
                neg_q = True
            else:
                if p == 2:
                    neg_q = False
                else:
                    neg_q = not is_square(detM, p, q)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is a finite extension of F of degree n",
    "H_2: Either p = 2, or both q and n are odd integers",
    "¬Q: No self-dual basis exists"
]

N_HYP = 2
NEG_Q_INDEX = 2