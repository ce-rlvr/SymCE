import sympy as sp
import math

# Top-level setup
r, theta, phi = sp.symbols('r theta phi', real=True)

def conditions(witness):
    try:
        # 1. Check if witness is a sympy ProductSet representing the domain
        if isinstance(witness, sp.ProductSet) and len(witness.sets) == 3:
            r_set, theta_set, phi_set = witness.sets
            r_can_be_zero = (r_set.contains(0) == True)
            if r_can_be_zero:
                neg_q = True
            else:
                int1 = theta_set.intersect(sp.Interval(-sp.pi, 0))
                int2 = theta_set.intersect(sp.Interval(sp.pi, 2*sp.pi))
                int1_empty = (int1 == sp.S.EmptySet) or (int1.is_empty == True)
                int2_empty = (int2 == sp.S.EmptySet) or (int2.is_empty == True)
                if not int1_empty or not int2_empty:
                    neg_q = True
                else:
                    neg_q = False
            return [neg_q]

        # 2. Check if witness is a tuple/list of 3 elements
        r_val, theta_val, phi_val = witness
        
        # Check if they are tuples/lists (representing bounds of the domain)
        if isinstance(r_val, (list, tuple)) and isinstance(theta_val, (list, tuple)):
            r_min, r_max = r_val
            theta_min, theta_max = theta_val
            
            r_min = float(r_min)
            r_max = float(r_max)
            theta_min = float(theta_min)
            theta_max = float(theta_max)
            
            r_can_be_zero = (r_min <= 0 <= r_max)
            
            if r_can_be_zero:
                neg_q = True
            else:
                if max(theta_min, -math.pi) <= min(theta_max, 0.0):
                    neg_q = True
                elif max(theta_min, math.pi) <= min(theta_max, 2*math.pi):
                    neg_q = True
                else:
                    neg_q = False
            return [neg_q]
            
        # 3. Otherwise, assume it's a specific point (r, theta, phi) in the domain
        r_sym = sp.sympify(r_val)
        theta_sym = sp.sympify(theta_val)
        
        jac_det = (r_sym**2) * sp.sin(theta_sym)
        
        if jac_det.is_number:
            val = jac_det.evalf()
            neg_q = bool(val <= 0)
        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Jacobian determinant r^2 sin(theta) is <= 0 at the witness point or domain"
]

N_HYP = 0
NEG_Q_INDEX = 0