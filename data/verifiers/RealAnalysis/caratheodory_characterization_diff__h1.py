import sympy
from sympy import FiniteSet, Interval, Symbol, Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    try:
        U = witness['U']
        a = witness['a']
        f = witness['f']
        Phi = witness['Phi']
        n = witness.get('n', 1)
        m = witness.get('m', 1)
    except KeyError:
        return [False, False]

    # H1: f is a function from U to R^m
    h1_ok = False
    try:
        if isinstance(U, FiniteSet):
            for x in U:
                _ = f(x)
        else:
            _ = f(a)
        h1_ok = True
    except Exception:
        pass

    # neg_Q: The equivalence fails
    neg_q_ok = False
    try:
        # If a is not in U, f(a) is undefined, making the equation undefined.
        # In this case, both sides of the equivalence are false/undefined, so it holds.
        if a not in U:
            return [h1_ok, False]

        # Check if a is an interior point of U
        is_interior = False
        if hasattr(U, 'interior'):
            is_interior = (a in U.interior)
            
        # If a is an interior point, Caratheodory's equivalence is a true theorem.
        # Thus, the equivalence holds and the conclusion does NOT fail.
        if is_interior:
            return [h1_ok, False]
            
        # If a is NOT an interior point, f is NOT differentiable at a (LHS is False).
        # We now check if there exists a continuous Phi satisfying the equation (RHS is True).
        # If RHS is True, the equivalence fails (False <==> True).
        
        rhs_eq = True
        is_continuous = False
        
        def to_col_vector(v):
            if isinstance(v, Matrix):
                return v
            if isinstance(v, (list, tuple)):
                return Matrix(v)
            return Matrix([[v]])
            
        if isinstance(U, FiniteSet):
            is_continuous = True  # Any function on a finite set is continuous at its points
            for x in U:
                fx = f(x)
                fa = f(a)
                phix = Phi(x)
                
                fx_mat = to_col_vector(fx)
                fa_mat = to_col_vector(fa)
                x_mat = to_col_vector(x)
                a_mat = to_col_vector(a)
                
                if isinstance(phix, Matrix):
                    phix_mat = phix
                elif isinstance(phix, (list, tuple)):
                    phix_mat = Matrix(phix)
                else:
                    phix_mat = Matrix([[phix]])
                    
                diff = fx_mat - fa_mat
                prod = phix_mat * (x_mat - a_mat)
                
                if sympy.simplify(diff - prod) != sympy.zeros(fx_mat.shape[0], fx_mat.shape[1]):
                    rhs_eq = False
                    break
                    
        elif isinstance(U, Interval):
            x_sym = Symbol('x', real=True)
            phi_x = Phi(x_sym)
            phi_a = Phi(a)
            
            if U.inf == a:
                lim = sympy.limit(phi_x, x_sym, a, dir='+')
            elif U.sup == a:
                lim = sympy.limit(phi_x, x_sym, a, dir='-')
            else:
                lim = sympy.limit(phi_x, x_sym, a)
                
            if isinstance(lim, Matrix) and isinstance(phi_a, Matrix):
                cont_check = sympy.simplify(lim - phi_a) == sympy.zeros(lim.shape[0], lim.shape[1])
            else:
                cont_check = sympy.simplify(lim - phi_a) == 0
                
            if cont_check:
                is_continuous = True
                
            fx = f(x_sym)
            fa = f(a)
            
            fx_mat = to_col_vector(fx)
            fa_mat = to_col_vector(fa)
            x_mat = to_col_vector(x_sym)
            a_mat = to_col_vector(a)
            
            if isinstance(phi_x, Matrix):
                phix_mat = phi_x
            elif isinstance(phi_x, (list, tuple)):
                phix_mat = Matrix(phi_x)
            else:
                phix_mat = Matrix([[phi_x]])
                
            diff = fx_mat - fa_mat
            prod = phix_mat * (x_mat - a_mat)
            
            if sympy.simplify(diff - prod) != sympy.zeros(fx_mat.shape[0], fx_mat.shape[1]):
                rhs_eq = False
                
        if rhs_eq and is_continuous:
            neg_q_ok = True
            
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a function from U to R^m",
    "¬Q: The equivalence fails (e.g., f is not differentiable at a, but Phi exists and is continuous)"
]

N_HYP = 1
NEG_Q_INDEX = 1