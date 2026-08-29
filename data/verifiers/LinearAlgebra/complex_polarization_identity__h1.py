import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: x and y are vectors in V",
    "¬Q: <x, y> != (1/4) * (||x + y||^2 - ||x - y||^2 + i||x + iy||^2 - i||x - iy||^2)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_inner(a, b):
    if hasattr(a, 'inner'):
        return a.inner(b)
    elif hasattr(b, 'vdot'):
        # Standard math convention for complex inner product spaces:
        # linear in the first argument, antilinear in the second.
        # Sympy's vdot is antilinear in the first, linear in the second.
        return b.vdot(a)
    elif hasattr(a, 'dot'):
        return a.dot(b)
    elif isinstance(a, (int, float, complex)) or hasattr(a, 'conjugate'):
        return a * sp.conjugate(b)
    else:
        raise ValueError("No inner product found")

def get_norm_sq(a):
    if hasattr(a, 'norm_sq'):
        return a.norm_sq()
    elif hasattr(a, 'vdot'):
        return a.vdot(a)
    elif hasattr(a, 'dot'):
        return a.dot(a)
    elif hasattr(a, 'norm'):
        return a.norm()**2
    elif isinstance(a, (int, float, complex)) or hasattr(a, 'conjugate'):
        return a * sp.conjugate(a)
    else:
        raise ValueError("No norm found")

def conditions(witness):
    try:
        x, y = witness
    except Exception:
        return [False, False]
        
    try:
        # H1: x and y are vectors in V
        # Check if they support basic vector space operations and inner product/norm
        _ = x + y
        _ = 2 * x
        _ = get_inner(x, y)
        _ = get_norm_sq(x)
        _ = get_norm_sq(y)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # Evaluate the LHS and RHS of the Complex Polarization Identity
        lhs = get_inner(x, y)
        
        term1 = get_norm_sq(x + y)
        term2 = get_norm_sq(x - y)
        term3 = get_norm_sq(x + sp.I * y)
        term4 = get_norm_sq(x - sp.I * y)
        
        rhs = (term1 - term2 + sp.I * term3 - sp.I * term4) / 4
        
        diff = lhs - rhs
        try:
            diff = sp.simplify(diff)
        except Exception:
            pass
            
        if diff == 0:
            neg_q = False
        else:
            try:
                # Check numerically if it's a non-zero scalar
                neg_q = abs(complex(diff)) > 1e-9
            except Exception:
                # If it cannot be converted to complex (e.g., contains symbols or is a matrix),
                # and it didn't simplify to 0, we consider the identity to have failed.
                neg_q = True
    except Exception:
        # If evaluating the identity fails (e.g., complex scalar multiplication is not 
        # supported in a real vector space), then the identity is undefined and thus fails.
        neg_q = True

    return [h1_ok, neg_q]