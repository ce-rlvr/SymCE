import sympy
from sympy import Matrix, Symbol, simplify, zeros, eye
from sympy.abc import *

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (n, T) where n is the dimension of the inner product space R^n,
    and T is a callable representing the mapping from V to F.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, T = witness
        else:
            n = 1
            T = witness
    except Exception:
        return [False, False]
    
    # H_1: Let V be a finite-dimensional inner product space over the field F.
    # We verify this by checking if n is a valid dimension and T is a valid scalar-valued function on R^n.
    h1 = False
    try:
        if isinstance(n, int) and n >= 1 and callable(T):
            v = Matrix([Symbol(f'v{i}', real=True) for i in range(n)])
            expr = T(v)
            if isinstance(expr, (sympy.Expr, int, float, complex)):
                h1 = True
            elif isinstance(expr, Matrix) and expr.shape == (1, 1):
                h1 = True
    except Exception:
        h1 = False

    # ¬Q: The conclusion FAILS.
    # Conclusion: There exists a unique vector u in V such that T(v) = <v, u> for all v in V.
    # If such a u exists, its components must be u_i = conjugate(T(e_i)).
    # We construct this candidate u and check if T(v) == <v, u> holds for all v.
    neg_q = False
    try:
        if h1:
            u_list = []
            for i in range(n):
                e_i = zeros(n, 1)
                e_i[i, 0] = 1
                val = T(e_i)
                if isinstance(val, Matrix) and val.shape == (1, 1):
                    val = val[0, 0]
                val = sympy.sympify(val)
                u_list.append(sympy.conjugate(val))
            u = Matrix(u_list)
            
            v = Matrix([Symbol(f'v{i}', real=True) for i in range(n)])
            T_v = T(v)
            if isinstance(T_v, Matrix) and T_v.shape == (1, 1):
                T_v = T_v[0, 0]
            T_v = sympy.sympify(T_v)
                
            inner_product = v.dot(u)
            
            diff = simplify(T_v - inner_product)
            conclusion_holds = (diff == 0)
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space over F",
    "¬Q: There does NOT exist a unique vector u in V such that T(v) = <v, u> for all v in V"
]

N_HYP = 1
NEG_Q_INDEX = 1