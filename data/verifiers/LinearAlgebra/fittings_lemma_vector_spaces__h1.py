import sympy

# Top-level setup: named object bindings that the witness expression may reference.
# We provide a standard symbol 'x' and some common infinite-dimensional linear operators
# on the vector space of polynomials in x.
x = sympy.Symbol('x')

class ShiftOperator:
    """
    The shift operator T(P) = x * P.
    It is injective but not surjective.
    """
    def __call__(self, p):
        return sympy.expand(x * p)

class DerivativeOperator:
    """
    The derivative operator T(P) = P'.
    It is surjective but not injective.
    """
    def __call__(self, p):
        return sympy.diff(p, x)

shift = ShiftOperator()
derivative = DerivativeOperator()

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: T: V -> V is a linear operator
    try:
        a, b = sympy.symbols('a b')
        p1 = x**2 + 2*x + 1
        p2 = 3*x**3 - x
        expr1 = witness(a*p1 + b*p2)
        expr2 = a*witness(p1) + b*witness(p2)
        h1 = bool(sympy.simplify(expr1 - expr2) == 0)
    except Exception:
        h1 = False

    # neg_Q: There does not exist a non-negative integer k such that V = ker(T^k) ⊕ im(T^k)
    # Note: For k=0, V = ker(I) ⊕ im(I) = {0} ⊕ V is a tautology for all operators.
    # The mathematical intent of Fitting's lemma requires k >= 1 (or k as the index of stabilization).
    # We test k from 1 to 5. If Fitting's lemma fails for all these k, we consider neg_Q = True.
    try:
        neg_q = True
        for k in range(1, 6):
            M = 10
            B = [x**i for i in range(M+1)]
            
            def apply_Tk(poly, times):
                res = poly
                for _ in range(times):
                    res = witness(res)
                return sympy.expand(res)
            
            Tk_B = [apply_Tk(b_poly, k) for b_poly in B]
            T2k_B = [apply_Tk(b_poly, 2*k) for b_poly in B]
            
            all_polys = T2k_B + Tk_B
            max_deg = max([sympy.degree(p, x) if p != 0 else 0 for p in all_polys] + [0])
            
            def poly_to_vec(p):
                if p == 0:
                    return [0] * (max_deg + 1)
                d = sympy.Poly(p, x).as_dict()
                vec = [0] * (max_deg + 1)
                for k_tuple, coeff in d.items():
                    deg = k_tuple[0]
                    if deg <= max_deg:
                        vec[deg] = coeff
                return vec
            
            # Matrix representing T^{2k} on the subspace spanned by B
            T2k_matrix = sympy.Matrix([poly_to_vec(p) for p in T2k_B]).T
            
            # 1. Check if ker(T^k) + im(T^k) = V
            # This holds iff for all P, T^k(P) is in the image of T^{2k}
            sum_holds = True
            for i in range(4):
                P = x**i
                Tk_P = apply_Tk(P, k)
                vec_Tk_P = sympy.Matrix(poly_to_vec(Tk_P))
                
                aug = T2k_matrix.row_join(vec_Tk_P)
                if T2k_matrix.rank() != aug.rank():
                    sum_holds = False
                    break
            
            if not sum_holds:
                continue  # Fitting's lemma fails for this k, check next k
                
            # 2. Check if ker(T^k) ∩ im(T^k) = {0}
            # This holds iff ker(T^{2k}) = ker(T^k)
            null_space = T2k_matrix.nullspace()
            intersection_zero = True
            for vec in null_space:
                v = sum(vec[i] * B[i] for i in range(M+1))
                Tk_v = apply_Tk(v, k)
                if sympy.simplify(Tk_v) != 0:
                    intersection_zero = False
                    break
                    
            if intersection_zero:
                # Both conditions hold -> Fitting's lemma holds for this k
                neg_q = False
                break
                
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T: V -> V is a linear operator",
    "¬Q: There does not exist a non-negative integer k such that V = ker(T^k) ⊕ im(T^k)"
]
N_HYP = 1
NEG_Q_INDEX = 1