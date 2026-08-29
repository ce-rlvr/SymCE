import sympy as sp
import math

# Top-level setup
x, n, k = sp.symbols('x n k', real=True)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        if isinstance(witness, dict):
            f_n = witness['f_n']
            f = witness['f']
            a_k_n = witness['a_k_n']
            b_k_n = witness['b_k_n']
            a_k = witness['a_k']
            b_k = witness['b_k']
        else:
            f_n, f, a_k_n, b_k_n, a_k, b_k = witness
            
        # H_1: (f_n) converges uniformly to f
        h1_ok = True
        diff_f = f_n - f
        max_err_1000 = 0
        for x_val in [-math.pi, -1.5, 0, 1.5, math.pi]:
            val = abs(float(diff_f.subs({n: 1000, x: x_val}).evalf()))
            if val > max_err_1000:
                max_err_1000 = val
        if max_err_1000 > 1e-2:
            h1_ok = False
                
        # H_2: a_k^{(n)} and b_k^{(n)} are the Fourier coefficients of f_n
        f_n_2 = sp.lambdify(x, f_n.subs({n: 2}), 'math')
        grid = [-math.pi + 2*math.pi*i/500 for i in range(501)]
        
        a_1_2_num = sum(f_n_2(xv) * math.cos(xv) for xv in grid[:-1]) * (2*math.pi/500) / math.pi
        b_1_2_num = sum(f_n_2(xv) * math.sin(xv) for xv in grid[:-1]) * (2*math.pi/500) / math.pi
        a_2_2_num = sum(f_n_2(xv) * math.cos(2*xv) for xv in grid[:-1]) * (2*math.pi/500) / math.pi
        b_2_2_num = sum(f_n_2(xv) * math.sin(2*xv) for xv in grid[:-1]) * (2*math.pi/500) / math.pi
        
        a_1_n_val = float(a_k_n.subs({k: 1, n: 2}).evalf())
        b_1_n_val = float(b_k_n.subs({k: 1, n: 2}).evalf())
        a_2_n_val = float(a_k_n.subs({k: 2, n: 2}).evalf())
        b_2_n_val = float(b_k_n.subs({k: 2, n: 2}).evalf())
        
        h2_ok = (abs(a_1_n_val - a_1_2_num) < 0.1 and abs(b_1_n_val - b_1_2_num) < 0.1 and
                 abs(a_2_n_val - a_2_2_num) < 0.1 and abs(b_2_n_val - b_2_2_num) < 0.1)
                 
        # neg_Q: The sequences of Fourier coefficients do NOT converge uniformly in k
        diff_a = a_k_n - a_k
        diff_b = b_k_n - b_k
        diff_1000 = 0
        for k_val in [1, 2, 10, 100, 1000, 10000]:
            val_a = abs(float(diff_a.subs({n: 1000, k: k_val}).evalf()))
            val_b = abs(float(diff_b.subs({n: 1000, k: k_val}).evalf()))
            if val_a > diff_1000: diff_1000 = val_a
            if val_b > diff_1000: diff_1000 = val_b
        
        if diff_1000 > 1e-2:
            neg_q_ok = True
        else:
            neg_q_ok = False
                
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f_n converges uniformly to f",
    "H_2: a_k_n and b_k_n are the Fourier coefficients of f_n",
    "¬Q: The sequences of Fourier coefficients do not converge uniformly in k"
]

N_HYP = 2
NEG_Q_INDEX = 2