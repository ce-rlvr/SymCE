import math
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: C is a non-empty, closed, and convex subset of H",
    "H_2: P_C maps each point in H to its unique nearest point in C",
    "¬Q: The projection operator P_C is not 1-Lipschitz continuous on H"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Expected witness format:
    A dictionary or object with the following attributes:
      - p: float (exponent for the L^p norm on R^2, must be between 1.1 and 100.0)
      - line: tuple of 3 floats (c1, c2, c3) defining the line C as c1*x + c2*y = c3
      - x1: tuple of 2 floats (x, y) for the first point in H
      - x2: tuple of 2 floats (x, y) for the second point in H
      - q1: tuple of 2 floats (x, y) for the projection of x1 onto C
      - q2: tuple of 2 floats (x, y) for the projection of x2 onto C
    """
    try:
        if isinstance(witness, dict):
            get = lambda k: witness[k]
        else:
            get = lambda k: getattr(witness, k)
            
        p = float(get('p'))
        c1, c2, c3 = map(float, get('line'))
        x1, y1 = map(float, get('x1'))
        x2, y2 = map(float, get('x2'))
        qx1, qy1 = map(float, get('q1'))
        qx2, qy2 = map(float, get('q2'))
        
        # H1: C is a non-empty, closed, and convex subset of H
        # We use H = (R^2, L^p) and C = line c1*x + c2*y = c3.
        # For H to be a strictly convex reflexive Banach space, we need 1 < p < infinity.
        # This guarantees C is closed and convex, and P_C is globally well-defined and unique.
        h1_ok = (1.1 <= p <= 100.0) and not (math.isclose(c1, 0) and math.isclose(c2, 0))
        
        if not h1_ok:
            return [False, False, False]
            
        norm_c = math.hypot(c1, c2)
        c1 /= norm_c
        c2 /= norm_c
        c3 /= norm_c
        
        def D(x):
            if x == 0:
                return 0.0
            return (abs(x) ** (p - 1)) * math.copysign(1.0, x)
            
        def check_proj(x, y, qx, qy):
            # Check if (qx, qy) is on the line C
            line_val = c1 * qx + c2 * qy
            if not math.isclose(line_val, c3, abs_tol=1e-4 * (abs(c3) + math.hypot(qx, qy) + 1)):
                return False
                
            # Check gradient orthogonality (KKT condition for the unique minimum distance)
            gx = D(qx - x)
            gy = D(qy - y)
            cross = gx * c2 - gy * c1
            mag = math.hypot(gx, gy)
            if not math.isclose(cross, 0, abs_tol=1e-4 * (mag + 1)):
                return False
            return True
            
        # H2: P_C maps each point in H to its unique nearest point in C
        # We verify that the witness provided the correct projections for the chosen points.
        h2_ok = check_proj(x1, y1, qx1, qy1) and check_proj(x2, y2, qx2, qy2)
        
        # neg_Q: P_C is not 1-Lipschitz continuous on H
        def dist(a, b):
            return (abs(a[0] - b[0])**p + abs(a[1] - b[1])**p)**(1/p)
            
        dist_p = dist((x1, y1), (x2, y2))
        dist_q = dist((qx1, qy1), (qx2, qy2))
        
        # Check if the distance between projections strictly exceeds the distance between original points
        neg_q_ok = dist_q > dist_p + 1e-5 * (dist_p + 1)
        
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]