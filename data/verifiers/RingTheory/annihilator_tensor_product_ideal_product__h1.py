import sympy

def flatten(m):
    return sympy.Matrix(list(m))

def get_basis(matrices):
    if not matrices:
        return []
    vecs = [flatten(m).T for m in matrices]
    A = sympy.Matrix(vecs)
    _, pivot_cols = A.rref()
    return [matrices[i] for i in pivot_cols]

def in_span(x, basis):
    if not basis:
        return all(e == 0 for e in x)
    vecs = [flatten(b) for b in basis]
    A = sympy.Matrix.hstack(*vecs)
    b = flatten(x)
    try:
        return A.rank() == A.row_join(b).rank()
    except Exception:
        return False

def is_module(R_basis, M_basis):
    for r in R_basis:
        for m in M_basis:
            if not in_span(r * m, M_basis): return False
            if not in_span(m * r, M_basis): return False
    return True

def is_annihilator(I_basis, M_basis, R_basis):
    I_basis = get_basis(I_basis)
    R_basis = get_basis(R_basis)
    M_basis = get_basis(M_basis)
    
    for i in I_basis:
        if not in_span(i, R_basis): return False
        
    for i in I_basis:
        for m in M_basis:
            if not all(e == 0 for e in flatten(i * m)): return False
            if not all(e == 0 for e in flatten(m * i)): return False
            
    eqs = []
    for m in M_basis:
        mat_left = sympy.Matrix.hstack(*[flatten(rk * m) for rk in R_basis])
        mat_right = sympy.Matrix.hstack(*[flatten(m * rk) for rk in R_basis])
        eqs.append(mat_left)
        eqs.append(mat_right)
        
    if not eqs:
        return len(I_basis) == len(R_basis)
        
    BigMat = sympy.Matrix.vstack(*eqs)
    null_space = BigMat.nullspace()
    return len(null_space) == len(I_basis)

def kronecker(A, B):
    vA = flatten(A)
    vB = flatten(B)
    return sympy.Matrix([a * b for a in vA for b in vB])

def tensor_product_relations(M_basis, N_basis, R_basis):
    rels = []
    for m in M_basis:
        for n in N_basis:
            for r in R_basis:
                t1 = kronecker(m * r, n)
                t2 = kronecker(m, r * n)
                rels.append(t1 - t2)
    return rels

def check_conclusion(I_basis, J_basis, M_basis, N_basis, R_basis):
    rels = tensor_product_relations(M_basis, N_basis, R_basis)
    RelMat = sympy.Matrix.hstack(*[flatten(rel) for rel in rels]) if rels else sympy.Matrix()
    
    IJ_basis = []
    for i in I_basis:
        for j in J_basis:
            IJ_basis.append(i * j)
            
    annihilates = True
    for x in IJ_basis:
        for m in M_basis:
            for n in N_basis:
                t_left = flatten(kronecker(x * m, n))
                t_right = flatten(kronecker(m, n * x))
                if RelMat.cols == 0:
                    if not all(e == 0 for e in t_left): annihilates = False
                    if not all(e == 0 for e in t_right): annihilates = False
                else:
                    if RelMat.rank() != RelMat.row_join(t_left).rank(): annihilates = False
                    if RelMat.rank() != RelMat.row_join(t_right).rank(): annihilates = False
                    
    return annihilates

def conditions(witness):
    try:
        R_basis = get_basis(witness.get('R', []))
        M_basis = get_basis(witness.get('M', []))
        N_basis = get_basis(witness.get('N', []))
        I_basis = get_basis(witness.get('I', []))
        J_basis = get_basis(witness.get('J', []))
    except Exception:
        return [False] * 5

    try:
        h1 = is_module(R_basis, M_basis)
    except Exception:
        h1 = False

    try:
        h2 = is_module(R_basis, N_basis)
    except Exception:
        h2 = False

    try:
        h3 = is_annihilator(I_basis, M_basis, R_basis)
    except Exception:
        h3 = False

    try:
        h4 = is_annihilator(J_basis, N_basis, R_basis)
    except Exception:
        h4 = False

    try:
        conclusion_holds = check_conclusion(I_basis, J_basis, M_basis, N_basis, R_basis)
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: N is an R-module",
    "H_3: I is the annihilator ideal of M in R",
    "H_4: J is the annihilator ideal of N in R",
    "¬Q: The product ideal IJ is not a subset of the annihilator ideal of the tensor product M \\otimes_R N"
]

N_HYP = 4
NEG_Q_INDEX = 4