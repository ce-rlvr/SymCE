import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            y = witness.get('y')
            L = witness.get('L')
        else:
            if len(witness) != 3:
                return [False, False, False]
            x, y, L = witness
            
        if not (isinstance(x, (list, tuple)) and isinstance(y, (list, tuple))):
            return [False, False, False]
            
        if len(x) == 0 or len(y) == 0:
            return [False, False, False]
            
        y_vals = [float(item) for item in y]
        h1 = True
        
        x_vals = [float(item) for item in x]
        L_val = float(L)
        h2 = True
        
        def lcm(a, b):
            return abs(a * b) // math.gcd(a, b)
        
        period = lcm(len(x), len(y))
        xy_limits = set()
        for i in range(period):
            xi = x_vals[i % len(x)]
            yi = y_vals[i % len(y)]
            xy_limits.add(round(xi * yi, 5))
            
        expected_limits = set(round(L_val * yi, 5) for yi in y_vals)
        
        neg_q = (xy_limits != expected_limits)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: (y_n) is a bounded sequence of real numbers",
    "H_2: S_y is the set of subsequential limits of (y_n)",
    "not_Q: The set of subsequential limits of (x_n y_n) is not equal to {L * s : s in S_y}"
]

N_HYP = 2
NEG_Q_INDEX = 2