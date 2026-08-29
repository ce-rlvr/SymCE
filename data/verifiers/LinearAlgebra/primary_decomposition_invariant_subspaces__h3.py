import sympy
from sympy import Matrix, eye, zeros, Poly
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T is a linear operator on V",
    "¬Q: The primary components are not T-invariant or do not form a direct sum decomposition of V"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Extract T and p_e_list from the witness
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            p_e_list = witness.get('p_e_list')
        elif hasattr(witness, 'T') and hasattr(witness, 'p_e_list'):
            T = witness.T
            p_e_list = witness.p_e_list
        else:
            T, p_e_list = witness
    except Exception:
        return [False, False, False]

    # H_1: V is a finite-dimensional vector space (represented by a matrix)
    try:
        h1 = isinstance(T, Matrix)
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V (represented by a square matrix)
    try:
        h2 = h1 and T.is_square
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        if not h2:
            neg_q = False
        else:
            # Normalize p_e_list if a single tuple was provided
            if isinstance(p_e_list, tuple) and len(p_e_list) == 2 and not isinstance(p_e_list[0], (list, tuple)):
                p_e_list = [p_e_list]
                
            n = T.shape[0]
            V_i_bases = []
            
            # Compute the nullspace for each primary component
            for p_expr, e in p_e_list:
                # Determine the variable of the polynomial
                if hasattr(p_expr, 'free_symbols'):
                    syms = p_expr.free_symbols
                    if len(syms) == 1:
                        var = list(syms)[0]
                    elif len(syms) > 1:
                        var = x if x in syms else list(syms)[0]
                    else:
                        var = x
                else:
                    var = x
                
                p = Poly(p_expr, var)
                coeffs = p.all_coeffs()
                pT = zeros(n, n)
                degree = len(coeffs) - 1
                
                # Evaluate p(T)
                for i, c in enumerate(coeffs):
                    power = degree - i
                    if power == 0:
                        pT += c * eye(n)
                    else:
                        pT += c * (T ** power)
                
                pTe = pT ** e
                ns = pTe.nullspace()
                V_i_bases.append(ns)
            
            q_holds = True
            
            # Check T-invariance of each V_i
            for ns in V_i_bases:
                if len(ns) > 0:
                    M_ns = Matrix.hstack(*ns)
                    rank_ns = M_ns.rank()
                    for v in ns:
                        Tv = T * v
                        if Matrix.hstack(M_ns, Tv).rank() > rank_ns:
                            q_holds = False
                            break
                if not q_holds:
                    break
            
            # Check if V is the direct sum of V_i
            if q_holds:
                all_basis_vectors = []
                for ns in V_i_bases:
                    all_basis_vectors.extend(ns)
                
                if len(all_basis_vectors) != n:
                    q_holds = False
                elif n > 0:
                    M = Matrix.hstack(*all_basis_vectors)
                    if M.rank() < n:
                        q_holds = False
            
            neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]