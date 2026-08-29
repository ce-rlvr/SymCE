import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

# Q8 represented as 2x2 complex matrices (a subgroup of the quaternions)
I = sympy.I
Q8_matrices = [
    sympy.Matrix([[1, 0], [0, 1]]),
    sympy.Matrix([[-1, 0], [0, -1]]),
    sympy.Matrix([[I, 0], [0, -I]]),
    sympy.Matrix([[-I, 0], [0, I]]),
    sympy.Matrix([[0, 1], [-1, 0]]),
    sympy.Matrix([[0, -1], [1, 0]]),
    sympy.Matrix([[0, I], [I, 0]]),
    sympy.Matrix([[0, -I], [-I, 0]])
]

def is_valid_scalar(x):
    if isinstance(x, (int, float, complex)): 
        return True
    if isinstance(x, sympy.Expr):
        if x.has(sympy.Mod): 
            return False
        return True
    return False

def is_equal(A, B):
    try:
        if hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix'):
            if A.shape != B.shape: return False
            diff = A - B
            if diff == sympy.zeros(*diff.shape): return True
            return all(sympy.simplify(diff[i]) == 0 for i in range(len(diff)))
        elif type(A).__name__ == 'Quaternion' and type(B).__name__ == 'Quaternion':
            if A.a == B.a and A.b == B.b and A.c == B.c and A.d == B.d: return True
            return (sympy.simplify(A.a - B.a) == 0 and 
                    sympy.simplify(A.b - B.b) == 0 and 
                    sympy.simplify(A.c - B.c) == 0 and 
                    sympy.simplify(A.d - B.d) == 0)
        elif type(A).__name__ == 'Permutation' and type(B).__name__ == 'Permutation':
            return A == B
        else:
            if A == B: return True
            return sympy.simplify(A - B) == 0
    except Exception:
        return False

def is_identity(A):
    try:
        if hasattr(A, 'is_Matrix'):
            if A.shape[0] != A.shape[1]: return False
            I_mat = sympy.eye(A.shape[0])
            if A == I_mat: return True
            diff = A - I_mat
            return all(sympy.simplify(diff[i]) == 0 for i in range(len(diff)))
        elif type(A).__name__ == 'Quaternion':
            if A.a == 1 and A.b == 0 and A.c == 0 and A.d == 0: return True
            return (sympy.simplify(A.a - 1) == 0 and 
                    sympy.simplify(A.b) == 0 and 
                    sympy.simplify(A.c) == 0 and 
                    sympy.simplify(A.d) == 0)
        elif type(A).__name__ == 'Permutation':
            return A.is_Identity
        else:
            if A == 1: return True
            return sympy.simplify(A - 1) == 0
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H1: R is an integral domain
    # We verify this by checking if the elements of G belong to a known integral domain.
    # Specifically, we check if they are scalars, SymPy Quaternions, or 2x2 matrices 
    # of the form [[a, b], [-conj(b), conj(a)]] which generate a subring of the quaternions.
    h1_ok = False
    try:
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            h1_ok = True
            for M in witness:
                if type(M).__name__ == 'Quaternion':
                    continue
                elif hasattr(M, 'is_Matrix') and M.is_Matrix:
                    if M.shape != (2, 2): 
                        h1_ok = False
                        break
                    a, b, c, d = M[0,0], M[0,1], M[1,0], M[1,1]
                    
                    if not (is_valid_scalar(a) and is_valid_scalar(b) and is_valid_scalar(c) and is_valid_scalar(d)):
                        h1_ok = False
                        break
                        
                    d_conj_a = d - sympy.conjugate(a)
                    if d_conj_a != 0 and sympy.simplify(d_conj_a) != 0:
                        h1_ok = False
                        break
                    c_conj_b = c + sympy.conjugate(b)
                    if c_conj_b != 0 and sympy.simplify(c_conj_b) != 0:
                        h1_ok = False
                        break
                elif isinstance(M, sympy.Expr):
                    if hasattr(M, 'is_commutative') and M.is_commutative is False:
                        h1_ok = False
                        break
                    if M.has(sympy.Mod):
                        h1_ok = False
                        break
                elif isinstance(M, (int, float, complex)):
                    continue
                else:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H2: G is a finite subgroup of U(R)
    h2_ok = False
    try:
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            h2_ok = True
            n = len(witness)
            # Check for duplicates
            for i in range(n):
                for j in range(i+1, n):
                    if is_equal(witness[i], witness[j]):
                        h2_ok = False
                        break
                if not h2_ok: break
            
            if h2_ok:
                # Check identity
                has_id = False
                for M in witness:
                    if is_identity(M):
                        has_id = True
                        break
                if not has_id:
                    h2_ok = False
            
            if h2_ok:
                # Check closure
                for A in witness:
                    for B in witness:
                        AB = A * B
                        found = False
                        for C in witness:
                            if is_equal(AB, C):
                                found = True
                                break
                        if not found:
                            h2_ok = False
                            break
                    if not h2_ok: break
    except Exception:
        h2_ok = False

    # neg_Q: G is NOT cyclic
    neg_q = False
    try:
        if h2_ok:
            n = len(witness)
            is_cyc = False
            for g in witness:
                current = g
                order = 1
                while not is_identity(current) and order <= n:
                    current = current * g
                    order += 1
                if order == n and is_identity(current):
                    is_cyc = True
                    break
            neg_q = not is_cyc
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: G is a finite subgroup of U(R)",
    "¬Q: G is not cyclic"
]
N_HYP = 2
NEG_Q_INDEX = 2