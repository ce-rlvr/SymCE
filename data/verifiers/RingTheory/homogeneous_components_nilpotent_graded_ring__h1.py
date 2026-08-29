import sympy
from sympy import expand, Matrix, MatrixBase, Symbol

# Top-level setup
t = Symbol('t')

def get_laurent_degree(expr, gen):
    """
    Returns the degree d if expr is of the form c * gen**d.
    Returns -inf if expr is 0.
    Returns None if expr is not homogeneous.
    """
    expr = expand(expr)
    if expr == 0:
        return -float('inf')
    if not expr.has(gen):
        return 0
    
    try:
        p = sympy.Poly(expr, gen)
        if len(p.terms()) == 1:
            return p.terms()[0][0][0]
    except Exception:
        pass
        
    try:
        inv_gen = 1/gen
        p = sympy.Poly(expr, inv_gen)
        if len(p.terms()) == 1:
            return -p.terms()[0][0][0]
    except Exception:
        pass

    return None

def matrix_laurent_degree(M, gen):
    """
    Returns the homogeneous degree of a matrix or scalar.
    A matrix is homogeneous if all its non-zero entries have the same degree.
    """
    if isinstance(M, MatrixBase):
        degs = set()
        for val in M:
            if val != 0:
                d = get_laurent_degree(val, gen)
                if d is None:
                    return None
                degs.add(d)
        if len(degs) == 1:
            return degs.pop()
        elif len(degs) == 0:
            return -float('inf')
        else:
            return None
    else:
        return get_laurent_degree(M, gen)

def is_nilpotent(x, max_pow=20):
    """
    Checks if x is a nilpotent element.
    For matrices, checks up to the matrix dimension.
    """
    if x == 0: 
        return True
    if isinstance(x, MatrixBase) and x.is_zero_matrix:
        return True
    
    curr = x
    limit = x.rows if isinstance(x, MatrixBase) else max_pow
    for _ in range(limit):
        if isinstance(curr, MatrixBase) and curr.is_zero_matrix:
            return True
        if curr == 0:
            return True
        
        try:
            curr = expand(curr * x)
        except Exception:
            return False
            
    if isinstance(curr, MatrixBase) and curr.is_zero_matrix:
        return True
    if curr == 0:
        return True
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a list of homogeneous components (e.g., matrices with polynomial entries).
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) == 0:
            return [False, False, False]
        
        # Find the grading generator (e.g., 't')
        symbols = set()
        for w in witness:
            if hasattr(w, 'free_symbols'):
                symbols.update(w.free_symbols)
        
        if len(symbols) > 1:
            gen = None
        else:
            gen = symbols.pop() if symbols else None
            
        # H_2: x_i are the homogeneous components of x (must have distinct valid degrees)
        h2_ok = True
        degs = set()
        for w in witness:
            if gen is None:
                is_zero = False
                if isinstance(w, MatrixBase):
                    is_zero = w.is_zero_matrix
                elif w == 0:
                    is_zero = True
                d = -float('inf') if is_zero else 0
            else:
                d = matrix_laurent_degree(w, gen)
                
            if d is None:
                h2_ok = False
                break
            if d != -float('inf'):
                if d in degs:
                    h2_ok = False
                    break
                degs.add(d)
                
        # H_1: x is a nilpotent element of R
        try:
            x = sum(witness[1:], witness[0])
            h1_ok = is_nilpotent(x)
        except Exception:
            h1_ok = False
            
        # ¬Q: Not all homogeneous components x_i are nilpotent
        neg_q_ok = False
        for w in witness:
            if not is_nilpotent(w):
                neg_q_ok = True
                break
                
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: x is a nilpotent element of R",
    "H_2: x_i are the homogeneous components of x such that x is the sum of x_i",
    "¬Q: Not all homogeneous components x_i are nilpotent elements of R"
]

N_HYP = 2
NEG_Q_INDEX = 2