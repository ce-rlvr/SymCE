import sympy as sp

# Standard linear algebra objects for witness construction
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that in ANY ring R, a polynomial f(x) is a unit 
    iff its constant term is a unit and all higher coefficients are nilpotent.
    This is true for commutative rings, but fails for non-commutative rings.
    We expect the witness to be a list of square SymPy matrices of the same size,
    representing the coefficients [a_0, a_1, ..., a_n] of f(x) over the ring M_k(Q).
    """
    try:
        # H_1: witness represents a valid polynomial f(x) over a ring R.
        # We enforce R to be a matrix ring M_k(Q) by requiring a list of numeric square matrices.
        if not isinstance(witness, list) or len(witness) == 0:
            h1 = False
        else:
            h1 = True
            for m in witness:
                if not isinstance(m, sp.MatrixBase):
                    h1 = False
                    break
                if not m.is_square:
                    h1 = False
                    break
            if h1:
                k = witness[0].rows
                for m in witness:
                    if m.rows != k:
                        h1 = False
                        break
                    # Ensure matrices are purely numeric to avoid symbolic evaluation issues
                    if m.free_symbols:
                        h1 = False
                        break
    except Exception:
        h1 = False

    try:
        if not h1:
            return [False, False]
            
        k = witness[0].rows
        a0 = witness[0]
        
        # In M_k(Q), a matrix is a unit iff its determinant is non-zero
        a0_is_unit = (a0.det() != 0)
        
        # In M_k(Q), a matrix is nilpotent iff its k-th power is the zero matrix
        ai_are_nilpotent = True
        for m in witness[1:]:
            if not (m**k).is_zero_matrix:
                ai_are_nilpotent = False
                break
                
        # Construct the matrix polynomial F(x)
        x = sp.Symbol('x')
        Fx = sp.zeros(k, k)
        for i, m in enumerate(witness):
            Fx = Fx + m * (x**i)
            
        # f(x) is a unit in M_k(Q)[x] iff its determinant is a non-zero constant
        det_Fx = Fx.det()
        det_poly = sp.Poly(det_Fx, x)
        fx_is_unit = (det_poly.degree() == 0 and det_poly.coeffs()[0] != 0)
        
        # The conclusion claims: f(x) is a unit <==> (a0 is a unit AND a_i are nilpotent)
        rhs = a0_is_unit and ai_are_nilpotent
        
        # The negated conclusion is True if the equivalence fails
        neg_q = bool(fx_is_unit != rhs)
        
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over a ring R",
    "¬Q: The equivalence between f(x) being a unit and (a_0 unit, a_i nilpotent) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1