import sympy as sp

# Top-level setup
x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        A, C = witness
    except Exception:
        return [False, False, False]
        
    # H1: The sequence satisfies a homogeneous linear recurrence relation with constant coefficients
    try:
        h1 = False
        if isinstance(A, list) and isinstance(C, list):
            if len(C) >= 2 and len(A) == len(C) - 1:
                if C[-1] != 0:
                    h1 = True
    except Exception:
        h1 = False

    # H2: The sequence is not identically zero
    try:
        h2 = any(a != 0 for a in A)
    except Exception:
        h2 = False

    # neg_Q: The radius of convergence is NOT exactly 1/M
    try:
        k = len(C) - 1
        
        # Characteristic polynomial P(x) = sum(c_i x^i)
        P = sum(C[i] * x**i for i in range(k + 1))
        P_poly = sp.Poly(P, x)
        roots_P = sp.roots(P_poly)
        
        # Check if all roots were found
        if sum(roots_P.values()) < P_poly.degree():
            neg_q = False
        else:
            if not roots_P:
                M = 0
            else:
                M = max([sp.Abs(r) for r in roots_P.keys()], key=lambda val: sp.N(val))
            
            if M == 0:
                inv_M = sp.oo
            else:
                inv_M = 1 / M
                
            # Generating function A(x) = U(x) / V(x)
            V = sum(C[i] * x**(k - i) for i in range(k + 1))
            U = 0
            for i in range(1, k + 1):
                U += C[i] * x**(k - i) * sum(A[j] * x**j for j in range(i))
                
            A_x = sp.cancel(U / V)
            V_red = sp.denom(A_x)
            V_red_poly = sp.Poly(V_red, x)
            
            roots_V_red = sp.roots(V_red_poly)
            if sum(roots_V_red.values()) < V_red_poly.degree():
                neg_q = False
            else:
                if not roots_V_red:
                    R = sp.oo
                else:
                    R = min([sp.Abs(r) for r in roots_V_red.keys()], key=lambda val: sp.N(val))
                
                if R == sp.oo and inv_M == sp.oo:
                    neg_q = False
                elif R == sp.oo or inv_M == sp.oo:
                    neg_q = True
                else:
                    diff = sp.simplify(R - inv_M)
                    neg_q = (diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The sequence satisfies a homogeneous linear recurrence relation with constant coefficients",
    "H_2: The sequence is not identically zero",
    "¬Q: The radius of convergence is NOT exactly 1/M"
]

N_HYP = 2
NEG_Q_INDEX = 2