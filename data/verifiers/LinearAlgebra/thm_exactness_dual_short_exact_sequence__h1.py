import sympy
from sympy import Matrix
import z3

# Top-level setup for standard objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def check_dims(P_U, P_V, P_W, F, G):
    if P_U.rows != F.cols: return False
    if P_V.rows != F.rows: return False
    if P_V.rows != G.cols: return False
    if P_W.rows != G.rows: return False
    return True

def in_image_z3(A, v):
    if A.cols == 0:
        return all(int(x) == 0 for x in v)
    solver = z3.Solver()
    x = [z3.Int(f'x_{i}') for i in range(A.cols)]
    for i in range(A.rows):
        expr = sum(int(A[i, j]) * x[j] for j in range(A.cols))
        solver.add(expr == int(v[i]))
    return solver.check() == z3.sat

def is_homomorphism(F, P_M, P_N):
    if P_M.cols == 0:
        return True
    for j in range(P_M.cols):
        v = F * P_M[:, j]
        if not in_image_z3(P_N, v):
            return False
    return True

def is_injective(F, P_U, P_V):
    solver = z3.Solver()
    x = [z3.Int(f'x_{i}') for i in range(F.cols)]
    
    y = [z3.Int(f'y_{i}') for i in range(P_V.cols)]
    for i in range(F.rows):
        fx_i = sum(int(F[i, j]) * x[j] for j in range(F.cols)) if F.cols > 0 else 0
        py_i = sum(int(P_V[i, j]) * y[j] for j in range(P_V.cols)) if P_V.cols > 0 else 0
        solver.add(fx_i == py_i)
        
    z = [z3.Int(f'z_{i}') for i in range(P_U.cols)]
    if P_U.cols > 0:
        eqs = []
        for i in range(P_U.rows):
            pz_i = sum(int(P_U[i, j]) * z[j] for j in range(P_U.cols))
            eqs.append(x[i] == pz_i)
        solver.add(z3.Not(z3.Exists(z, z3.And(eqs))))
    else:
        if len(x) > 0:
            solver.add(z3.Or([x_i != 0 for x_i in x]))
        else:
            return True
            
    if len(x) == 0:
        return True
        
    return solver.check() == z3.unsat

def is_exact_at_V(F, G, P_U, P_V, P_W):
    GF = G * F
    for j in range(GF.cols):
        if not in_image_z3(P_W, GF[:, j]):
            return False
            
    solver = z3.Solver()
    v = [z3.Int(f'v_{i}') for i in range(G.cols)]
    
    w = [z3.Int(f'w_{i}') for i in range(P_W.cols)]
    for i in range(G.rows):
        gv_i = sum(int(G[i, j]) * v[j] for j in range(G.cols)) if G.cols > 0 else 0
        pw_i = sum(int(P_W[i, j]) * w[j] for j in range(P_W.cols)) if P_W.cols > 0 else 0
        solver.add(gv_i == pw_i)
        
    x = [z3.Int(f'x_{i}') for i in range(F.cols)]
    y = [z3.Int(f'y_{i}') for i in range(P_V.cols)]
    eqs = []
    for i in range(F.rows):
        fx_i = sum(int(F[i, j]) * x[j] for j in range(F.cols)) if F.cols > 0 else 0
        py_i = sum(int(P_V[i, j]) * y[j] for j in range(P_V.cols)) if P_V.cols > 0 else 0
        eqs.append(v[i] == fx_i + py_i)
        
    if len(x) + len(y) > 0:
        solver.add(z3.Not(z3.Exists(x + y, z3.And(eqs))))
    else:
        if len(v) > 0:
            solver.add(z3.Or([v_i != 0 for v_i in v]))
        else:
            return True
            
    if len(v) == 0:
        return True
        
    return solver.check() == z3.unsat

def is_surjective(G, P_W):
    for i in range(G.rows):
        e_i = [1 if j == i else 0 for j in range(G.rows)]
        solver = z3.Solver()
        v = [z3.Int(f'v_{j}') for j in range(G.cols)]
        w = [z3.Int(f'w_{j}') for j in range(P_W.cols)]
        for k in range(G.rows):
            gv_k = sum(int(G[k, j]) * v[j] for j in range(G.cols)) if G.cols > 0 else 0
            pw_k = sum(int(P_W[k, j]) * w[j] for j in range(P_W.cols)) if P_W.cols > 0 else 0
            solver.add(e_i[k] == gv_k + pw_k)
        if solver.check() != z3.sat:
            return False
    return True

def dual_is_injective(G, P_W):
    solver = z3.Solver()
    phi = [z3.Int(f'phi_{i}') for i in range(G.rows)]
    
    for i in range(P_W.cols):
        solver.add(sum(int(P_W[j, i]) * phi[j] for j in range(P_W.rows)) == 0)
        
    for i in range(G.cols):
        solver.add(sum(int(G[j, i]) * phi[j] for j in range(G.rows)) == 0)
        
    if len(phi) > 0:
        solver.add(z3.Or([phi_i != 0 for phi_i in phi]))
    else:
        return True
    
    return solver.check() == z3.unsat

def dual_is_exact_at_V(F, G, P_V, P_W):
    solver = z3.Solver()
    psi = [z3.Int(f'psi_{i}') for i in range(F.rows)]
    
    for i in range(P_V.cols):
        solver.add(sum(int(P_V[j, i]) * psi[j] for j in range(P_V.rows)) == 0)
        
    for i in range(F.cols):
        solver.add(sum(int(F[j, i]) * psi[j] for j in range(F.rows)) == 0)
        
    phi = [z3.Int(f'phi_{i}') for i in range(G.rows)]
    eqs = []
    for i in range(P_W.cols):
        eqs.append(sum(int(P_W[j, i]) * phi[j] for j in range(P_W.rows)) == 0)
    for i in range(G.cols):
        eqs.append(psi[i] == sum(int(G[j, i]) * phi[j] for j in range(G.rows)))
        
    if len(phi) > 0:
        solver.add(z3.Not(z3.Exists(phi, z3.And(eqs))))
    else:
        if len(psi) > 0:
            solver.add(z3.Or([psi_i != 0 for psi_i in psi]))
        else:
            return True
            
    if len(psi) == 0:
        return True
        
    return solver.check() == z3.unsat

def dual_is_surjective(F, P_U, P_V):
    solver = z3.Solver()
    omega = [z3.Int(f'omega_{i}') for i in range(F.cols)]
    
    omega_in_U_star = []
    for i in range(P_U.cols):
        omega_in_U_star.append(sum(int(P_U[j, i]) * omega[j] for j in range(P_U.rows)) == 0)
        
    psi = [z3.Int(f'psi_{i}') for i in range(F.rows)]
    
    psi_in_V_star = []
    for i in range(P_V.cols):
        psi_in_V_star.append(sum(int(P_V[j, i]) * psi[j] for j in range(P_V.rows)) == 0)
        
    omega_eq_F_T_psi = []
    for i in range(F.cols):
        omega_eq_F_T_psi.append(omega[i] == sum(int(F[j, i]) * psi[j] for j in range(F.rows)))
        
    if len(omega_in_U_star) > 0:
        solver.add(z3.And(omega_in_U_star))
        
    if len(psi) > 0:
        exists_psi = z3.Exists(psi, z3.And(psi_in_V_star + omega_eq_F_T_psi))
        solver.add(z3.Not(exists_psi))
    else:
        if len(omega) > 0:
            solver.add(z3.Or([o != 0 for o in omega]))
        else:
            return True
            
    if len(omega) == 0:
        return True
        
    return solver.check() == z3.unsat

def conditions(witness) -> list[bool]:
    try:
        P_U = witness['P_U']
        P_V = witness['P_V']
        P_W = witness['P_W']
        F = witness['F']
        G = witness['G']
        
        if not check_dims(P_U, P_V, P_W, F, G):
            return [False, False, False]
            
        H1 = is_homomorphism(F, P_U, P_V) and is_homomorphism(G, P_V, P_W)
        H2 = is_injective(F, P_U, P_V) and is_exact_at_V(F, G, P_U, P_V, P_W) and is_surjective(G, P_W)
        
        Q = dual_is_injective(G, P_W) and dual_is_exact_at_V(F, G, P_V, P_W) and dual_is_surjective(F, P_U, P_V)
        
        return [bool(H1), bool(H2), not bool(Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f: U -> V and g: V -> W are linear transformations",
    "H_2: The sequence 0 -> U -> V -> W -> 0 is a short exact sequence",
    "¬Q: The induced sequence of dual spaces 0 -> W^* -> V^* -> U^* -> 0 is not exact"
]

N_HYP = 2
NEG_Q_INDEX = 2