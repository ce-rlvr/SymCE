import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: E and F are subfields of L containing K",
    "H_2: The extension E/K is finite",
    "H_3: The extension F/K is finite",
    "¬Q: The composite field EF is not a finite extension of K, or dim(EF) > dim(E)dim(F)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_field_gen(M):
    """
    Checks if the matrix M generates a field over Q.
    This is true iff its minimal polynomial is irreducible over Q.
    Returns (is_field, degree).
    """
    try:
        x = sp.Symbol('x')
        poly_expr = M.charpoly(x).as_expr()
        p = sp.Poly(poly_expr, x, domain='QQ')
        factors = p.factor_list()
        
        # If the characteristic polynomial has more than one irreducible factor,
        # the minimal polynomial either has multiple factors or is reducible.
        if len(factors[1]) != 1:
            return False, 0
            
        P_poly, _ = factors[1][0]
        coeffs = P_poly.all_coeffs()
        n = M.shape[0]
        
        # Evaluate P_poly(M)
        M_pow = sp.eye(n)
        res = sp.zeros(n, n)
        for c in reversed(coeffs):
            res += c * M_pow
            M_pow = M_pow * M
            
        # If P_poly(M) == 0, then P_poly is the minimal polynomial.
        # Since P_poly is irreducible, Q[M] is a field.
        if res.is_zero_matrix:
            return True, P_poly.degree()
            
        return False, 0
    except Exception:
        return False, 0

def is_algebra_field(M_E, M_F):
    """
    Given two commuting matrices that generate fields, checks if the 
    commutative algebra Q[M_E, M_F] is a field.
    Returns (is_field, dimension).
    """
    try:
        n = M_E.shape[0]
        basis = []
        basis_vecs = []
        
        # Find a basis for the algebra Q[M_E, M_F]
        queue = [sp.eye(n)]
        while queue:
            M = queue.pop(0)
            vec = sp.Matrix(n * n, 1, list(M))
            if not basis:
                basis.append(M)
                basis_vecs.append(vec)
                queue.append(M * M_E)
                queue.append(M * M_F)
            else:
                mat = sp.Matrix.hstack(*(basis_vecs + [vec]))
                if mat.rank() > len(basis):
                    basis.append(M)
                    basis_vecs.append(vec)
                    queue.append(M * M_E)
                    queue.append(M * M_F)
                    
        dim = len(basis)
        
        # The algebra is a field iff a generic element generates a field of degree `dim`.
        for k in range(1, dim + 6):
            M_rand = M_E + k * M_F
            is_fg, deg = is_field_gen(M_rand)
            if is_fg and deg == dim:
                return True, dim
                
        return False, dim
    except Exception:
        return False, 0

def conditions(witness):
    """
    Evaluates the witness against the hypotheses and negated conclusion.
    The witness is expected to contain at least two sympy matrices M_E and M_F
    representing the generators of the subfields E and F within the matrix ring L = M_n(Q).
    """
    best_result = [False, False, False, False]
    
    try:
        items = []
        if isinstance(witness, (list, tuple)):
            items = list(witness)
        elif isinstance(witness, dict):
            items = list(witness.values())
        else:
            items = [witness]

        matrices = [x for x in items if isinstance(x, sp.Matrix)]
        
        if len(matrices) >= 2:
            for i in range(len(matrices)):
                for j in range(len(matrices)):
                    if i == j:
                        continue
                        
                    M_E = matrices[i]
                    M_F = matrices[j]
                    
                    if M_E.shape == M_F.shape:
                        is_E_field, deg_E = is_field_gen(M_E)
                        is_F_field, deg_F = is_field_gen(M_F)
                        
                        if is_E_field and is_F_field:
                            h1 = True
                            h2 = True
                            h3 = True
                            
                            # If they do not commute, they generate a non-commutative ring,
                            # which cannot be a field. Thus the composite field EF does not exist.
                            if M_E * M_F != M_F * M_E:
                                neg_q = True
                            else:
                                # If they commute, they might generate a commutative ring with zero divisors.
                                is_alg_field, dim = is_algebra_field(M_E, M_F)
                                if not is_alg_field:
                                    neg_q = True
                                else:
                                    # If it is a field, check the degree inequality
                                    neg_q = bool(dim > deg_E * deg_F)
                                    
                            result = [h1, h2, h3, neg_q]
                            if neg_q:
                                return result
                            else:
                                best_result = result
    except Exception:
        pass

    return best_result