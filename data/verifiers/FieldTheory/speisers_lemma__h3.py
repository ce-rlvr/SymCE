import sympy
from sympy import Symbol, Matrix, eye, zeros, rem, Poly, QQ

# Top-level setup: named object bindings that the witness expression may reference.
alpha = Symbol('alpha')
x = Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for Speiser's Lemma (with dropped semi-linear action hypothesis).
    
    Expected witness attributes:
      - alpha: sympy.Symbol (the primitive element of L over K, e.g., alpha)
      - min_poly: sympy.Expr (the minimal polynomial of alpha over K=QQ)
      - G: list of sympy.Expr (the images of alpha under the Galois group G)
      - V_dim: int (dimension of V over L)
      - action_matrices: list of sympy.Matrix (K-linear action of G on V, represented as 
                         (V_dim * d) x (V_dim * d) matrices over QQ, where d is the degree of L/K)
    """
    ans = [False, False, False]
    
    try:
        w_alpha = witness.alpha
        min_poly_expr = witness.min_poly
        G = witness.G
        
        min_poly = Poly(min_poly_expr, w_alpha, domain=QQ)
        d = min_poly.degree()
        
        # H_1: L/K is a finite Galois extension of fields with Galois group G
        h1_ok = False
        if min_poly.is_irreducible:
            if len(G) == d:
                roots_ok = True
                roots_set = set()
                for g in G:
                    if rem(sympy.expand(min_poly_expr.subs(w_alpha, g)), min_poly_expr, w_alpha) != 0:
                        roots_ok = False
                        break
                    g_red = rem(sympy.expand(g), min_poly_expr, w_alpha)
                    roots_set.add(g_red)
                if roots_ok and len(roots_set) == d:
                    h1_ok = True
        ans[0] = h1_ok
    except Exception:
        pass

    try:
        V_dim = witness.V_dim
        action_matrices = witness.action_matrices
        
        # H_2: V is a vector space over L (and G acts on V)
        h2_ok = False
        if isinstance(V_dim, int) and V_dim >= 1:
            if len(action_matrices) == d:
                id_idx = -1
                for i, g in enumerate(G):
                    if rem(sympy.expand(g - w_alpha), min_poly_expr, w_alpha) == 0:
                        id_idx = i
                        break
                
                if id_idx != -1 and action_matrices[id_idx] == eye(V_dim * d):
                    hom_ok = True
                    for i, g1 in enumerate(G):
                        for j, g2 in enumerate(G):
                            g3_expr = rem(sympy.expand(g1.subs(w_alpha, g2)), min_poly_expr, w_alpha)
                            g3_idx = -1
                            for k, g3 in enumerate(G):
                                if rem(sympy.expand(g3 - g3_expr), min_poly_expr, w_alpha) == 0:
                                    g3_idx = k
                                    break
                            if g3_idx == -1:
                                hom_ok = False
                                break
                            if action_matrices[i] * action_matrices[j] != action_matrices[g3_idx]:
                                hom_ok = False
                                break
                        if not hom_ok:
                            break
                    if hom_ok:
                        h2_ok = True
        ans[1] = h2_ok
    except Exception:
        pass

    try:
        # ¬Q: V^G is not a K-vector space or the natural map V^G \otimes_K L \to V is not an isomorphism
        # Since the witness provides K-linear action matrices, V^G is guaranteed to be a K-vector space.
        # We only need to check if the natural map is an isomorphism.
        stacked = []
        I = eye(V_dim * d)
        for M in action_matrices:
            stacked.append(M - I)
        
        BigM = Matrix.vstack(*stacked)
        nullspace = BigM.nullspace()
        
        dim_VG = len(nullspace)
        
        if dim_VG != V_dim:
            ans[2] = True
        else:
            L_vectors = []
            for vec in nullspace:
                L_vec = []
                for i in range(V_dim):
                    coords = vec[i*d : (i+1)*d, 0]
                    elem = sum(coords[j] * w_alpha**j for j in range(d))
                    L_vec.append(elem)
                L_vectors.append(L_vec)
            
            L_matrix = Matrix(L_vectors).T
            det = L_matrix.det()
            det_red = rem(sympy.expand(det), min_poly_expr, w_alpha)
            
            if det_red == 0:
                ans[2] = True
            else:
                ans[2] = False
    except Exception:
        pass

    return ans

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension of fields with Galois group G",
    "H_2: V is a vector space over L",
    "¬Q: V^G is not a K-vector space or the natural map V^G \\otimes_K L \\to V is not an isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2