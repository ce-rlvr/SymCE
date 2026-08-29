import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    P = None
    pi = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            P_mat, pi_vec = witness
            P = Matrix(P_mat)
            pi = list(pi_vec)
        else:
            P = Matrix(witness)
            n = P.shape[0]
            pi_syms = sympy.symbols(f'pi0:{n}')
            eqs = []
            for i in range(n):
                for j in range(i+1, n):
                    eqs.append(pi_syms[i]*P[i, j] - pi_syms[j]*P[j, i])
            eqs.append(sum(pi_syms) - 1)
            sol = sympy.linsolve(eqs, pi_syms)
            if sol:
                s = list(sol)[0]
                if s.free_symbols:
                    subs = {fs: sympy.Rational(1, n) for fs in s.free_symbols}
                    pi_cand = [sympy.simplify(x.subs(subs)) for x in s]
                else:
                    pi_cand = [sympy.simplify(x) for x in s]
                
                valid_cand = True
                for p in pi_cand:
                    try:
                        c_p = complex(p)
                        if abs(c_p.imag) > 1e-9 or c_p.real < -1e-9:
                            valid_cand = False
                            break
                    except Exception:
                        if sympy.simplify(sympy.im(p)) != 0 or sympy.simplify(p) < 0:
                            valid_cand = False
                            break
                if valid_cand:
                    pi = pi_cand
    except Exception:
        pass

    # H1: P is an n x n stochastic transition matrix over the real numbers
    h1_ok = False
    try:
        if P is not None and P.is_square:
            n = P.shape[0]
            is_stoch = True
            for i in range(n):
                row_sum = 0
                for j in range(n):
                    val = P[i, j]
                    try:
                        c_val = complex(val)
                        if abs(c_val.imag) > 1e-9 or c_val.real < -1e-9:
                            is_stoch = False
                            break
                    except Exception:
                        if sympy.simplify(sympy.im(val)) != 0 or sympy.simplify(val) < 0:
                            is_stoch = False
                            break
                    row_sum += val
                if not is_stoch:
                    break
                
                try:
                    diff = float(sympy.simplify(row_sum - 1))
                    if abs(diff) > 1e-9:
                        is_stoch = False
                        break
                except Exception:
                    if sympy.simplify(row_sum - 1) != 0:
                        is_stoch = False
                        break
            h1_ok = is_stoch
    except Exception:
        h1_ok = False

    # H2: The detailed balance condition \pi_i P_{ij} = \pi_j P_{ji} holds for all 1 <= i, j <= n
    h2_ok = False
    try:
        if P is not None and pi is not None and len(pi) == P.shape[0]:
            n = P.shape[0]
            pi_sum = sum(pi)
            try:
                diff = float(sympy.simplify(pi_sum - 1))
                sum_ok = abs(diff) < 1e-9
            except Exception:
                sum_ok = sympy.simplify(pi_sum - 1) == 0
                
            if sum_ok:
                valid_pi = True
                for p in pi:
                    try:
                        c_p = complex(p)
                        if abs(c_p.imag) > 1e-9 or c_p.real < -1e-9:
                            valid_pi = False
                            break
                    except Exception:
                        if sympy.simplify(sympy.im(p)) != 0 or sympy.simplify(p) < 0:
                            valid_pi = False
                            break
                if valid_pi:
                    db_holds = True
                    for i in range(n):
                        for j in range(n):
                            diff = sympy.simplify(pi[i]*P[i, j] - pi[j]*P[j, i])
                            try:
                                diff_float = float(diff)
                                if abs(diff_float) > 1e-9:
                                    db_holds = False
                                    break
                            except Exception:
                                if diff != 0:
                                    db_holds = False
                                    break
                        if not db_holds:
                            break
                    h2_ok = db_holds
    except Exception:
        h2_ok = False

    # neg_Q: The transition matrix P is NOT diagonalizable over the real numbers.
    neg_q_ok = False
    try:
        if P is not None and P.is_square:
            try:
                diag = P.is_diagonalizable(reals_only=True)
                if diag is not None:
                    neg_q_ok = not diag
                else:
                    raise ValueError("is_diagonalizable returned None")
            except Exception:
                n = P.shape[0]
                eigenvects = P.eigenvects()
                total_geom_mult = 0
                is_diag = True
                for evalue, alg_mult, evects in eigenvects:
                    try:
                        c_ev = complex(evalue)
                        if abs(c_ev.imag) > 1e-9:
                            is_diag = False
                            break
                    except Exception:
                        if sympy.simplify(sympy.im(evalue)) != 0:
                            is_diag = False
                            break
                    total_geom_mult += len(evects)
                if is_diag and total_geom_mult == n:
                    neg_q_ok = False
                else:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is an n x n stochastic transition matrix over the real numbers",
    "H_2: The detailed balance condition \\pi_i P_{ij} = \\pi_j P_{ji} holds for all 1 <= i, j <= n",
    "¬Q: The transition matrix P is not diagonalizable over the real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2