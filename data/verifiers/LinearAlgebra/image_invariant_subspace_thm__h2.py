import sympy as sp
import itertools
import math

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def check_finite_witness(witness):
    V = witness['V']
    W = witness['W']
    T = witness['T']
    add = witness['add']
    smul = witness.get('smul', lambda c, u: u)
    scalars = witness.get('scalars', [1])
    zero = witness['zero']
    
    h1_ok = True
    if zero not in V: h1_ok = False
    for u in V:
        for v in V:
            if add(u, v) not in V: h1_ok = False
        for c in scalars:
            if smul(c, u) not in V: h1_ok = False
            
    h2_ok = True
    if zero not in W: h2_ok = False
    for u in W:
        if u not in V: h2_ok = False
        if T[u] not in W: h2_ok = False
        for v in W:
            if add(u, v) not in W: h2_ok = False
        for c in scalars:
            if smul(c, u) not in W: h2_ok = False
            
    TW = [T[w] for w in W]
    tw_is_subspace = True
    if zero not in TW:
        tw_is_subspace = False
    else:
        for u in TW:
            for v in TW:
                if add(u, v) not in TW:
                    tw_is_subspace = False
                    break
            for c in scalars:
                if smul(c, u) not in TW:
                    tw_is_subspace = False
                    break
                    
    tw_is_invariant = True
    for u in TW:
        if T[u] not in TW:
            tw_is_invariant = False
            break
            
    neg_q_ok = not (tw_is_subspace and tw_is_invariant)
    
    return [h1_ok, h2_ok, neg_q_ok]

def check_gf2_witness(witness):
    n = witness['n']
    T = witness['T']
    W = witness['W']
    
    V = list(itertools.product([0, 1], repeat=n))
    
    def add(u, v):
        return tuple(a ^ b for a, b in zip(u, v))
        
    h1_ok = n > 0 and all(v in T for v in V) and all(T[v] in V for v in V)
    
    W_set = set(W)
    zero = tuple([0]*n)
    
    h2_ok = False
    if W_set.issubset(set(V)) and zero in W_set:
        is_subspace = all(add(u, v) in W_set for u in W_set for v in W_set)
        is_invariant = all(T[w] in W_set for w in W_set)
        h2_ok = is_subspace and is_invariant
        
    TW_set = set(T[w] for w in W_set)
    tw_is_subspace = (zero in TW_set) and all(add(u, v) in TW_set for u in TW_set for v in TW_set)
    tw_is_invariant = all(T[u] in TW_set for u in TW_set)
    
    neg_q_ok = not (tw_is_subspace and tw_is_invariant)
    
    return [h1_ok, h2_ok, neg_q_ok]

def check_R_witness(witness):
    V_dim, T_input, W_basis = witness
    
    h1_ok = isinstance(V_dim, int) and V_dim > 0
    
    if isinstance(T_input, sp.Matrix):
        T = lambda x: T_input * x
    else:
        T = T_input
        
    W_basis = [sp.Matrix(b) for b in W_basis]
    
    if not W_basis:
        w_generic = sp.zeros(V_dim, 1)
        Tw = T(w_generic)
        if not isinstance(Tw, sp.Matrix): Tw = sp.Matrix(Tw)
        h2_ok = sp.simplify(Tw).is_zero_matrix
        neg_q_ok = not h2_ok
        return [h1_ok, h2_ok, neg_q_ok]
        
    c = sp.symbols(f'c0:{len(W_basis)}')
    w_generic = sp.zeros(V_dim, 1)
    for i, basis_vec in enumerate(W_basis):
        w_generic += c[i] * basis_vec
        
    Tw = T(w_generic)
    if not isinstance(Tw, sp.Matrix): Tw = sp.Matrix(Tw)
    
    W_mat = sp.Matrix.hstack(*W_basis)
    left_null = W_mat.T.nullspace()
    is_invariant = True
    for n in left_null:
        dot_prod = sp.simplify(n.dot(Tw))
        if dot_prod != 0:
            is_invariant = False
            break
            
    h2_ok = is_invariant
    
    neg_q_ok = False
    T0 = T(sp.zeros(V_dim, 1))
    if not isinstance(T0, sp.Matrix): T0 = sp.Matrix(T0)
    if not sp.simplify(T0).is_zero_matrix:
        neg_q_ok = True
        return [h1_ok, h2_ok, neg_q_ok]
        
    w_points = []
    for coeffs in itertools.product([-1, 0, 1, 2], repeat=len(W_basis)):
        if all(coeff == 0 for coeff in coeffs): continue
        w_val = sp.zeros(V_dim, 1)
        for i, c_val in enumerate(coeffs):
            w_val += c_val * W_basis[i]
        w_points.append(w_val)
        if len(w_points) >= 4:
            break
            
    tw_points = []
    for w in w_points:
        tw = T(w)
        if not isinstance(tw, sp.Matrix): tw = sp.Matrix(tw)
        tw_points.append(tw)
    
    test_points = []
    for p in tw_points:
        test_points.append(-p)
        test_points.append(2*p)
    for i in range(len(tw_points)):
        for j in range(i+1, len(tw_points)):
            test_points.append(tw_points[i] + tw_points[j])
            
    for tp in test_points:
        eqs = [Tw[i] - tp[i] for i in range(V_dim)]
        try:
            sols = sp.solve(eqs, c, dict=True)
            has_real = False
            for sol in sols:
                if all(abs(sp.im(val.evalf())) < 1e-9 for val in sol.values()):
                    has_real = True
                    break
            if not has_real:
                neg_q_ok = True
                break
        except Exception:
            pass
            
    return [h1_ok, h2_ok, neg_q_ok]

def conditions(witness):
    try:
        if isinstance(witness, dict) and 'add' in witness:
            return check_finite_witness(witness)
    except Exception:
        pass
        
    try:
        if isinstance(witness, dict) and 'n' in witness and 'T' in witness:
            return check_gf2_witness(witness)
    except Exception:
        pass
        
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            return check_R_witness(witness)
    except Exception:
        pass
        
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            T, W_basis = witness
            if callable(T) and isinstance(W_basis, list):
                W_basis_mat = [sp.Matrix(b) for b in W_basis]
                V_dim = W_basis_mat[0].shape[0]
                return check_R_witness((V_dim, T, W_basis_mat))
    except Exception:
        pass
        
    try:
        if callable(witness):
            V_dim = 2
            W_basis = [sp.Matrix([1, 0]), sp.Matrix([0, 1])]
            return check_R_witness((V_dim, witness, W_basis))
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: The image T(W) is not a T-invariant subspace of V"
]

N_HYP = 2
NEG_Q_INDEX = 2