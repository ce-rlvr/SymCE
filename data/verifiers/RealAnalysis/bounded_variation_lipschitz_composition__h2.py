import math
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: gamma is a function of bounded variation on the interval",
    "¬Q: f o gamma is not of bounded variation, or its total variation exceeds L * V(gamma)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        f = witness['f']
        gamma = witness['gamma']
        a = float(witness['a'])
        b = float(witness['b'])
        L = float(witness['L'])
    except Exception:
        return [False, False]
        
    def calc_dist(v1, v2):
        try:
            iter(v1)
            is_iter = not isinstance(v1, str)
        except TypeError:
            is_iter = False
        
        if is_iter:
            return math.sqrt(sum((float(x) - float(y))**2 for x, y in zip(v1, v2)))
        else:
            return abs(float(v2) - float(v1))
            
    try:
        n_points = 2000
        if a >= b:
            return [False, False]
            
        t_values = [a + i * (b - a) / n_points for i in range(n_points + 1)]
        
        v_gamma_grid = 0.0
        for i in range(n_points):
            val1 = gamma(t_values[i])
            val2 = gamma(t_values[i+1])
            v_gamma_grid += calc_dist(val1, val2)
            
        V_gamma_exact = float(witness.get('V_gamma', v_gamma_grid))
        
        h1_ok = bool(v_gamma_grid < 1e6 and v_gamma_grid <= V_gamma_exact + 1e-3)
    except Exception:
        h1_ok = False

    try:
        v_f_gamma_grid = 0.0
        for i in range(n_points):
            g1 = gamma(t_values[i])
            g2 = gamma(t_values[i+1])
            
            try:
                val1 = f(g1)
            except TypeError:
                val1 = f(*g1)
                
            try:
                val2 = f(g2)
            except TypeError:
                val2 = f(*g2)
                
            v_f_gamma_grid += calc_dist(val1, val2)
            
        neg_q_ok = bool((v_f_gamma_grid > L * V_gamma_exact + 1e-4) or (v_f_gamma_grid > 1e6))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]