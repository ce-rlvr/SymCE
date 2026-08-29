import sympy
from sympy import Matrix, eye

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over F",
    "H_2: A is a nilpotent matrix",
    "¬Q: The trace of A is not zero"
]

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The conjecture states that the trace of a nilpotent matrix over F is zero.
    This is true if F is a field, but false if F is a general commutative ring 
    (which is the dropped hypothesis).
    
    The witness should be a tuple (A, mod) where:
      - A is a sympy.Matrix of integers (or a list of lists)
      - mod is an integer >= 2
    This represents the matrix A over the commutative ring Z/mod Z.
    
    Alternatively, the witness can be a sympy.Matrix of sympy.Mod objects.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, mod = witness
            if not isinstance(A, Matrix):
                try:
                    A = Matrix(A)
                except Exception:
                    return [False, False, False]
            if not isinstance(mod, int) or mod < 2:
                return [False, False, False]
        elif isinstance(witness, Matrix) or isinstance(witness, list):
            try:
                A = Matrix(witness)
            except Exception:
                return [False, False, False]
            mods = set()
            for x in A:
                if isinstance(x, sympy.Mod):
                    mods.add(int(x.args[1]))
            if len(mods) == 1:
                mod = mods.pop()
            else:
                mod = None
        else:
            return [False, False, False]
            
        def get_int(x):
            if isinstance(x, int):
                return x
            if isinstance(x, sympy.Mod):
                return int(x.args[0]) % int(x.args[1])
            if hasattr(x, 'is_integer'):
                if callable(x.is_integer):
                    if x.is_integer():
                        return int(x)
                else:
                    if x.is_integer:
                        return int(x)
            raise ValueError("Not an integer")
            
        try:
            A_ints = A.applyfunc(get_int)
        except Exception:
            return [False, False, False]
            
        # H1: A is an n x n matrix over F
        h1 = A_ints.is_square
        
        # H2: A is a nilpotent matrix
        h2 = False
        if h1:
            m = A_ints.shape[0]
            if m == 0:
                h2 = True
            else:
                Ak = eye(m)
                max_iter = (m * mod + 2) if mod is not None else (m + 2)
                max_iter = min(max_iter, 100)  # Cap iterations for performance
                for _ in range(max_iter):
                    if mod is not None:
                        Ak = (Ak * A_ints).applyfunc(lambda x: x % mod)
                    else:
                        Ak = Ak * A_ints
                    if Ak.is_zero_matrix:
                        h2 = True
                        break
                        
        # neg_Q: The trace of A is NOT zero
        neg_q = False
        if h1:
            tr = A_ints.trace()
            if mod is not None:
                tr = tr % mod
            neg_q = (tr != 0)
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]