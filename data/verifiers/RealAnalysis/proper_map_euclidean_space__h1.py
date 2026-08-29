import z3

# Top-level setup
# No specific algebraic objects are required for this real analysis theorem.

# Expected witness format:
# A dictionary containing:
# {
#     'f': callable,       # takes a z3.Real, returns a z3.Real
#     'N_of_M': callable,  # takes a z3.Real M, returns a z3.Real N such that |x| > N => |f(x)| > M
#     'K_min': float,      # minimum of the compact interval K
#     'K_max': float,      # maximum of the compact interval K
#     'x0': float          # a limit point of f^{-1}(K) that is NOT in f^{-1}(K)
# }
# Example of a valid witness:
# {
#     'f': lambda x: z3.If(x == 0, z3.RealVal(1), x),
#     'N_of_M': lambda M: M,
#     'K_min': 0.0,
#     'K_max': 0.5,
#     'x0': 0.0
# }

def conditions(witness) -> list[bool]:
    # H1: ||x|| -> oo implies ||f(x)|| -> oo
    h1_ok = False
    try:
        f = witness['f']
        N_of_M = witness['N_of_M']
        M, x = z3.Reals('M x')
        
        N = N_of_M(M)
        if isinstance(N, (int, float)):
            N = z3.RealVal(N)
            
        fx = f(x)
        
        abs_x_gt_N = z3.Or(x > N, x < -N)
        abs_fx_le_M = z3.And(fx <= M, fx >= -M)
        
        solver = z3.Solver()
        solver.add(M > 0)
        solver.add(abs_x_gt_N)
        solver.add(abs_fx_le_M)
        
        solver.set("timeout", 2000)
        res = solver.check()
        h1_ok = (res == z3.unsat)
    except Exception:
        h1_ok = False

    # Negated Conclusion: There exists a compact K such that f^{-1}(K) is not compact
    # Since H1 implies f^{-1}(K) is bounded, it is not compact iff it is not closed.
    # It is not closed iff there is a limit point x0 of f^{-1}(K) that is not in f^{-1}(K).
    neg_q_ok = False
    try:
        f = witness['f']
        K_min = float(witness['K_min'])
        K_max = float(witness['K_max'])
        x0 = float(witness['x0'])
        
        if K_min <= K_max:
            K_min_val = z3.RealVal(K_min)
            K_max_val = z3.RealVal(K_max)
            x0_val = z3.RealVal(x0)
            
            # Check x0 is not in f^{-1}(K)
            fx0 = f(x0_val)
            solver1 = z3.Solver()
            solver1.add(z3.And(fx0 >= K_min_val, fx0 <= K_max_val))
            solver1.set("timeout", 2000)
            
            if solver1.check() == z3.unsat:
                # Check x0 is a limit point of f^{-1}(K)
                # ForAll eps > 0, Exists x, x != x0 and |x - x0| < eps and f(x) in K
                eps, x = z3.Reals('eps x')
                fx = f(x)
                
                x_neq_x0 = z3.Or(x > x0_val, x < x0_val)
                dist_less_eps = z3.And(x - x0_val < eps, x0_val - x < eps)
                fx_in_K = z3.And(fx >= K_min_val, fx <= K_max_val)
                
                # We check if the negation is unsat
                solver2 = z3.Solver()
                solver2.add(eps > 0)
                solver2.add(z3.ForAll([x], z3.Not(z3.And(x_neq_x0, dist_less_eps, fx_in_K))))
                solver2.set("timeout", 2000)
                
                if solver2.check() == z3.unsat:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: For every sequence x_k -> oo, ||f(x_k)|| -> oo",
    "¬Q: There exists a compact subset K such that f^{-1}(K) is not compact"
]

N_HYP = 1
NEG_Q_INDEX = 1