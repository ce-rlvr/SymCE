import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that S_n acts on L by the standard permutation of variables.
    Without this, S_n could act trivially (or via another representation), making the fixed field larger than K(e_1, ..., e_n).
    
    Witness should be a dictionary with:
      - 'K': a SymPy field (e.g., sympy.QQ)
      - 'n': an integer >= 1
      - 'action': a function `f(sigma, expr, vars)` defining the action of S_n on L
      - 'counterexample_expr': a SymPy expression in L that is in L^{S_n} but not K(e_1..e_n), or vice versa.
    """
    try:
        K = witness['K']
        n = witness['n']
        action = witness['action']
        expr = witness['counterexample_expr']
    except Exception:
        return [False, False, False]

    # H_1: K is a field
    try:
        h1 = getattr(K, 'is_Field', False)
    except Exception:
        h1 = False

    # H_2: L = K(x_1, ..., x_n) is the field of rational functions in n variables over K
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False

    # neg_Q: The fixed field L^{S_n} is not equal to K(e_1, ..., e_n)
    try:
        if not (isinstance(n, int) and 1 <= n <= 5):
            neg_q = False
        else:
            vars = sympy.symbols(f'x1:{n+1}')
            Sn = SymmetricGroup(n)
            elements = list(Sn.generate())
            
            # Verify that the provided action is a valid group action on the generators of L
            is_left_action = True
            is_right_action = True
            for sigma in elements:
                for tau in elements:
                    sig_tau = sigma * tau
                    for v in vars:
                        lhs = action(sig_tau, v, vars)
                        rhs_left = action(sigma, action(tau, v, vars), vars)
                        rhs_right = action(tau, action(sigma, v, vars), vars)
                        if sympy.cancel(lhs - rhs_left) != 0:
                            is_left_action = False
                        if sympy.cancel(lhs - rhs_right) != 0:
                            is_right_action = False
            valid_action = is_left_action or is_right_action
            
            if not valid_action:
                neg_q = False
            else:
                # Verify that expr is a valid rational function in L
                num, den = sympy.fraction(sympy.cancel(expr))
                if not (num.is_polynomial(*vars) and den.is_polynomial(*vars)):
                    neg_q = False
                elif not expr.free_symbols.issubset(set(vars)):
                    neg_q = False
                else:
                    # Check if expr is in the fixed field L^{S_n}
                    is_fixed_by_action = True
                    for sigma in elements:
                        if sympy.cancel(action(sigma, expr, vars) - expr) != 0:
                            is_fixed_by_action = False
                            break
                    
                    # Check if expr is in K(e_1, ..., e_n)
                    # By the true Fundamental Theorem, this is equivalent to being symmetric under the standard action
                    is_symmetric = True
                    for sigma in elements:
                        subs_dict = {vars[i]: vars[sigma(i)] for i in range(n)}
                        if sympy.cancel(expr.subs(subs_dict) - expr) != 0:
                            is_symmetric = False
                            break
                    
                    # The conclusion fails if the two fields are not equal, 
                    # meaning there exists an element in one but not the other.
                    neg_q = (is_fixed_by_action != is_symmetric)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is the field of rational functions in n variables over K",
    "¬Q: The fixed field L^{S_n} is not equal to K(e_1, ..., e_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2