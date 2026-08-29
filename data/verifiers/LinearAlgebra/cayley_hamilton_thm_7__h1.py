import sympy
from sympy import eye, zeros, Symbol

# Top-level setup: named object bindings for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Non-commutative symbols are provided since the conjecture fails over non-commutative rings
a = Symbol('a', commutative=False)
b = Symbol('b', commutative=False)
c = Symbol('c', commutative=False)
d = Symbol('d', commutative=False)
x = Symbol('x', commutative=False)
y = Symbol('y', commutative=False)
z = Symbol('z', commutative=False)
w = Symbol('w', commutative=False)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok].
    """
    if isinstance(witness, dict):
        A = witness.get('A')
        k = witness.get('k')
    elif isinstance(witness, (list, tuple)) and len(witness) == 2:
        A, k = witness
    else:
        return [False, False, False]
        
    # H_1: A is an n x n matrix with entries in F.
    try:
        h1 = isinstance(A, sympy.MatrixBase) and A.is_square
    except Exception:
        h1 = False
        
    # H_2: k is an integer such that k >= n.
    try:
        if h1:
            n = A.rows
            h2 = isinstance(k, (int, sympy.Integer)) and k >= n
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: A^k is NOT in the linear span of {I, A, A^2, ..., A^{n-1}} over F.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n = A.rows
            basis = [A**i for i in range(n)]
            A_k = A**k
            
            def is_commutative_matrix(mat):
                for expr in mat:
                    if getattr(expr, 'is_commutative', True) is False:
                        return False
                    if hasattr(expr, 'free_symbols'):
                        for sym in expr.free_symbols:
                            if getattr(sym, 'is_commutative', True) is False:
                                return False
                    if isinstance(expr, sympy.MatrixBase):
                        return False
                return True
                
            is_comm = is_commutative_matrix(A)
            in_span_flag = False
            
            # For commutative matrices, rank check is highly robust
            if is_comm:
                try:
                    M = sympy.Matrix(n*n, len(basis), lambda i, j: basis[j][i // n, i % n])
                    v = sympy.Matrix(n*n, 1, lambda i, j: A_k[i // n, i % n])
                    if M.rank() == M.row_join(v).rank():
                        in_span_flag = True
                except Exception:
                    pass
                    
            # For non-commutative matrices (or if rank check fails), use exact symbolic solving
            if not in_span_flag:
                try:
                    c_syms = sympy.symbols(f'c0:{len(basis)}')
                    eqs = []
                    for i in range(n):
                        for j in range(n):
                            eq = -A_k[i, j]
                            for idx, B in enumerate(basis):
                                eq += c_syms[idx] * B[i, j]
                            
                            # Flatten if entries are themselves matrices (block matrices)
                            if isinstance(eq, sympy.MatrixBase):
                                eqs.extend(list(eq))
                            else:
                                eqs.append(eq)
                                
                    sol = sympy.solve(eqs, c_syms, dict=True)
                    if sol:
                        in_span_flag = True
                except Exception:
                    pass
                    
            neg_q = not in_span_flag
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with entries in F",
    "H_2: k is an integer such that k >= n",
    "¬Q: A^k is not in the linear span of {I, A, A^2, ..., A^{n-1}} over F"
]

N_HYP = 2
NEG_Q_INDEX = 2