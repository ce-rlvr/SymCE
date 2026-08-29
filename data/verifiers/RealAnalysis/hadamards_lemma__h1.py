import sympy
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z, t, u, v, w

# Top-level setup for potential witness objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: a in I",
    "H_2: f: I -> R is continuously differentiable",
    "not Q: The conclusion fails (no such continuous g exists, e.g. due to type mismatch in n > 1 dimensions)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Extract properties from the witness
        if isinstance(witness, dict):
            a = witness.get('a')
            I = witness.get('I')
            f = witness.get('f')
            vars = witness.get('vars')
        else:
            a = getattr(witness, 'a', None)
            I = getattr(witness, 'I', None)
            f = getattr(witness, 'f', None)
            vars = getattr(witness, 'vars', None)
            
        if vars is None and isinstance(f, sympy.Basic):
            vars = tuple(sorted(f.free_symbols, key=lambda s: s.name))
            
        if not isinstance(a, (list, tuple)):
            a = (a,)
        if vars is not None and not isinstance(vars, (list, tuple)):
            vars = (vars,)
            
        # H1: a in I
        h1 = False
        try:
            if I is None:
                h1 = True
            elif hasattr(I, 'contains'):
                if len(a) == 1:
                    h1 = bool(I.contains(a[0]))
                else:
                    h1 = bool(I.contains(a))
            else:
                h1 = True
        except Exception:
            h1 = False
            
        # H2: f is continuously differentiable
        h2 = False
        try:
            if isinstance(f, sympy.Basic) and vars:
                h2 = True
                for v in vars:
                    df = sympy.diff(f, v)
                    subs_dict = dict(zip(vars, a))
                    val = df.subs(subs_dict)
                    # Check for obvious singularities at 'a'
                    if val.has(sympy.oo, sympy.nan, sympy.zoo):
                        h2 = False
                        break
            elif callable(f):
                try:
                    val = f(*a)
                    h2 = True
                except Exception:
                    h2 = False
            else:
                h2 = False
        except Exception:
            h2 = False
            
        # neg_Q: The conclusion fails
        # In 1D (scalar to scalar), Hadamard's Lemma is always true and g is continuous.
        # The conjecture is false because it drops the hypothesis that the domain is 1D (or drops the dot product / summation for n > 1).
        # If n > 1, f'(a) is a vector/matrix, but g(a) is a scalar, so g(a) = f'(a) is a type mismatch.
        # Similarly, (x - a)g(x) is a vector, but f(x) - f(a) is a scalar.
        neg_q = False
        try:
            is_scalar_eq = True
            
            # Check if domain is scalar
            if vars is not None:
                if len(vars) > 1:
                    is_scalar_eq = False
                elif len(vars) == 1 and hasattr(vars[0], 'is_Matrix') and vars[0].is_Matrix:
                    is_scalar_eq = False
            
            if len(a) > 1:
                is_scalar_eq = False
            elif len(a) == 1:
                if hasattr(a[0], 'is_Matrix') and a[0].is_Matrix:
                    is_scalar_eq = False
                elif isinstance(a[0], (list, tuple)):
                    is_scalar_eq = False
                    
            # Check if codomain is scalar
            if hasattr(f, 'is_Matrix') and f.is_Matrix:
                is_scalar_eq = False
                
            neg_q = not is_scalar_eq
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]