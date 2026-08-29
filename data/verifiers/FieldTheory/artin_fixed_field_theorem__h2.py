import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x

# Standard bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to represent a generator g(x) of a group G acting on K = QQ(x).
    It can be provided as a SymPy expression (e.g., x + 1), a callable, a 2x2 matrix, 
    or a dictionary containing one of these.
    """
    h1 = False
    h2 = False
    neg_q = False

    try:
        M = None
        
        # Attempt to extract a 2x2 matrix representation of the fractional linear transformation
        if isinstance(witness, sympy.Matrix) and witness.shape == (2, 2):
            M = witness
        elif isinstance(witness, dict):
            for key in ['g', 'G', 'action', 'generator', 'matrix', 'M']:
                if key in witness:
                    val = witness[key]
                    if isinstance(val, sympy.Matrix) and val.shape == (2, 2):
                        M = val
                        break
                    if isinstance(val, list) and len(val) > 0 and isinstance(val[0], sympy.Matrix) and val[0].shape == (2, 2):
                        M = val[0]
                        break

        # If no matrix was found, attempt to extract a SymPy expression or callable
        if M is None:
            expr = None
            if isinstance(witness, sympy.Expr):
                expr = witness
            elif callable(witness):
                try:
                    expr = witness(x)
                except Exception:
                    pass
            elif isinstance(witness, dict):
                for key in ['g', 'G', 'action', 'generator', 'expr']:
                    if key in witness:
                        val = witness[key]
                        if isinstance(val, sympy.Expr):
                            expr = val
                            break
                        if callable(val):
                            try:
                                expr = val(x)
                                break
                            except Exception:
                                pass
                        if isinstance(val, list) and len(val) > 0:
                            if isinstance(val[0], sympy.Expr):
                                expr = val[0]
                                break
                            if callable(val[0]):
                                try:
                                    expr = val[0](x)
                                    break
                                except Exception:
                                    pass
            elif isinstance(witness, (list, tuple)):
                for item in witness:
                    if isinstance(item, sympy.Expr):
                        expr = item
                        break
                    if callable(item):
                        try:
                            expr = item(x)
                            break
                        except Exception:
                            pass
                    if isinstance(item, list) and len(item) > 0:
                        if isinstance(item[0], sympy.Expr):
                            expr = item[0]
                            break
                        if callable(item[0]):
                            try:
                                expr = item[0](x)
                                break
                            except Exception:
                                pass
            
            # Convert the expression into a 2x2 matrix for the fractional linear transformation
            if expr is not None:
                expr = sympy.cancel(expr)
                n, d = sympy.fraction(expr)
                n_poly = sympy.Poly(n, x)
                d_poly = sympy.Poly(d, x)
                
                if n_poly.degree() <= 1 and d_poly.degree() <= 1:
                    n_coeffs = n_poly.all_coeffs()
                    d_coeffs = d_poly.all_coeffs()
                    
                    a = n_coeffs[0] if n_poly.degree() == 1 else 0
                    b = n_coeffs[1] if n_poly.degree() == 1 else n_coeffs[0]
                    
                    c = d_coeffs[0] if d_poly.degree() == 1 else 0
                    d_coeff = d_coeffs[1] if d_poly.degree() == 1 else d_coeffs[0]
                    
                    M = sympy.Matrix([[a, b], [c, d_coeff]])

        # Evaluate the hypotheses and the negated conclusion
        if M is not None and sympy.simplify(M.det()) != 0:
            # H1: K is a field. (K = QQ(x) is a field, and G acts on it via valid automorphisms)
            h1 = True
            
            # H2: F is the fixed field of K under G. (True by definition in our setup)
            h2 = True
            
            # ¬Q: K/F is not a finite Galois extension or Gal(K/F) != G.
            # This is true if and only if G is an infinite group.
            # We check if the matrix M has infinite order in PGL(2, C).
            is_finite = False
            for k in range(1, 25):
                Mk = M**k
                # Check if Mk is a non-zero scalar multiple of the identity matrix
                if sympy.simplify(Mk[0, 1]) == 0 and sympy.simplify(Mk[1, 0]) == 0:
                    if sympy.simplify(Mk[0, 0] - Mk[1, 1]) == 0 and sympy.simplify(Mk[0, 0]) != 0:
                        is_finite = True
                        break
            neg_q = not is_finite

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: F is the fixed field of K under the action of G",
    "¬Q: K/F is not a finite Galois extension or Gal(K/F) != G"
]

N_HYP = 2
NEG_Q_INDEX = 2