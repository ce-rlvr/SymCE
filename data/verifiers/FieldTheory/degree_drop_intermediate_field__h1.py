import sympy
import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: L is an intermediate field such that F is a subset of L and L is a subset of K",
    "H_2: alpha is an element of K that is algebraic over F",
    "neg_Q: alpha is not algebraic over L or the degree of L(alpha) over L is greater than the degree of F(alpha) over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_algebra_basis(generators, n):
    I = sympy.eye(n)
    basis = [I]
    basis_vectors = [list(I)]
    
    added = True
    while added:
        added = False
        new_basis = list(basis)
        for mat in basis:
            for g in generators:
                for new_mat in (mat * g, g * mat):
                    vec = list(new_mat)
                    test_mat = sympy.Matrix(basis_vectors + [vec])
                    if test_mat.rank() > len(basis_vectors):
                        basis_vectors.append(vec)
                        new_basis.append(new_mat)
                        added = True
        basis = new_basis
    return basis, basis_vectors

def is_field(gens, n):
    if not gens:
        return True
    for i in range(len(gens)):
        for j in range(i+1, len(gens)):
            if gens[i]*gens[j] != gens[j]*gens[i]:
                return False
    basis, _ = get_algebra_basis(gens, n)
    dim = len(basis)
    
    if dim == 1:
        return True
        
    for coeffs in itertools.product(range(-1, 2), repeat=dim):
        if all(c == 0 for c in coeffs): continue
        mat = sum(c*b for c, b in zip(coeffs, basis))
        try:
            p = sympy.minpoly(mat)
            if p.is_irreducible and sympy.degree(p) == dim:
                return True
        except Exception:
            pass
            
    for coeffs in itertools.product(range(-2, 3), repeat=dim):
        if all(c == 0 for c in coeffs): continue
        mat = sum(c*b for c, b in zip(coeffs, basis))
        try:
            p = sympy.minpoly(mat)
            if p.is_irreducible and sympy.degree(p) == dim:
                return True
        except Exception:
            pass
            
    return False

def is_subset(gens_sub, gens_super, n):
    basis_super, vecs_super = get_algebra_basis(gens_super, n)
    for g in gens_sub:
        vec = list(g)
        test_mat = sympy.Matrix(vecs_super + [vec])
        if test_mat.rank() > len(vecs_super):
            return False
    return True

def is_in_algebra(alpha, gens_K, n):
    basis_K, vecs_K = get_algebra_basis(gens_K, n)
    vec = list(alpha)
    test_mat = sympy.Matrix(vecs_K + [vec])
    return test_mat.rank() == len(vecs_K)

def degree_over(gens_base, alpha, n):
    basis_base, _ = get_algebra_basis(gens_base, n)
    dim_base = len(basis_base)
    basis_ext, _ = get_algebra_basis(gens_base + [alpha], n)
    dim_ext = len(basis_ext)
    return dim_ext / dim_base

def conditions(witness) -> list[bool]:
    # 1. Duck-typing for custom witness objects
    try:
        if hasattr(witness, 'h1') and hasattr(witness, 'h2') and hasattr(witness, 'neg_q'):
            return [bool(witness.h1()), bool(witness.h2()), bool(witness.neg_q())]
    except Exception:
        pass

    try:
        if isinstance(witness, dict) and 'h1' in witness and 'h2' in witness and 'neg_q' in witness:
            return [bool(witness['h1']()), bool(witness['h2']()), bool(witness['neg_q']())]
    except Exception:
        pass

    # 2. Extract F, L, K, alpha
    try:
        if isinstance(witness, dict):
            F = witness.get('F', [])
            L = witness.get('L', [])
            K = witness.get('K', [])
            alpha = witness.get('alpha', None)
        elif hasattr(witness, 'F'):
            F = witness.F
            L = witness.L
            K = witness.K
            alpha = witness.alpha
        else:
            F, L, K, alpha = witness
    except Exception:
        return [False, False, False]

    # 3. Matrix algebra approach
    if hasattr(alpha, 'shape'):
        try:
            n = alpha.shape[0]
            
            try:
                L_is_field = is_field(L, n)
                F_sub_L = is_subset(F, L, n)
                L_sub_K = is_subset(L, K, n)
                h1 = bool(L_is_field and F_sub_L and L_sub_K)
            except Exception:
                h1 = False
                
            try:
                alpha_in_K = is_in_algebra(alpha, K, n)
                h2 = bool(alpha_in_K)
            except Exception:
                h2 = False
                
            try:
                deg_F = degree_over(F, alpha, n)
                deg_L = degree_over(L, alpha, n)
                neg_q = not (deg_L <= deg_F)
            except Exception:
                neg_q = False
                
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 4. Fallback for other types (e.g. SymPy domains)
    try:
        h1 = False
        if hasattr(L, 'is_field'):
            L_is_field = L.is_field
        else:
            L_is_field = True
            
        if hasattr(F, 'issubset'):
            F_sub_L = F.issubset(L)
        else:
            F_sub_L = True
            
        if hasattr(L, 'issubset'):
            L_sub_K = L.issubset(K)
        else:
            L_sub_K = True
            
        h1 = bool(L_is_field and F_sub_L and L_sub_K)
    except Exception:
        h1 = False

    try:
        if hasattr(K, 'contains'):
            alpha_in_K = K.contains(alpha)
        else:
            alpha_in_K = True
            
        if hasattr(alpha, 'is_algebraic_over'):
            alg_F = alpha.is_algebraic_over(F)
        else:
            alg_F = True
            
        h2 = bool(alpha_in_K and alg_F)
    except Exception:
        h2 = False

    try:
        if hasattr(alpha, 'is_algebraic_over'):
            alg_L = alpha.is_algebraic_over(L)
        else:
            alg_L = True
            
        if not alg_L:
            neg_q = True
        else:
            deg_L = L.degree(alpha) if hasattr(L, 'degree') else 1
            deg_F = F.degree(alpha) if hasattr(F, 'degree') else 0
            neg_q = bool(deg_L > deg_F)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]