import sympy
from sympy import minpoly, Poly, simplify, Rational, I, sqrt
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Expected witness format:
    {
        'theta_val': expression, # e.g., sqrt(2), generating the Galois extension E = Q(theta)
        'alpha_val': expression, # e.g., sqrt(3), the element alpha
        'auto_polys': list,      # e.g., [x, -x], polynomials in x representing the Galois group actions on theta
    }
    """
    try:
        theta_val = witness['theta_val']
        alpha_val = witness['alpha_val']
        auto_polys = witness['auto_polys']
    except Exception:
        return [False, False, False]
        
    # H1: E/F is a finite Galois extension
    try:
        p_theta = minpoly(theta_val, z, domain='QQ')
        deg_E = p_theta.degree()
        
        H1 = True
        if len(auto_polys) != deg_E:
            H1 = False
        else:
            evaluated_roots = []
            for poly in auto_polys:
                r = simplify(poly.subs(x, theta_val))
                if simplify(p_theta.subs(z, r)) != 0:
                    H1 = False
                    break
                evaluated_roots.append(r)
            
            # Check that all provided roots are distinct
            if H1:
                for i in range(len(evaluated_roots)):
                    for j in range(i+1, len(evaluated_roots)):
                        if simplify(evaluated_roots[i] - evaluated_roots[j]) == 0:
                            H1 = False
                            break
                    if not H1:
                        break
    except Exception:
        H1 = False

    # H2: G = Gal(E/F) is the Galois group of the extension
    # If H1 holds, the provided automorphisms exactly form the Galois group.
    H2 = H1

    # ¬Q: The field trace and norm formulas fail for alpha
    try:
        try:
            p_alpha = minpoly(alpha_val, z, domain='QQ')
            p_alpha_poly = Poly(p_alpha, z)
            deg_alpha = p_alpha_poly.degree()
            coeffs = p_alpha_poly.all_coeffs()
            
            trace_val = -coeffs[1] if deg_alpha >= 1 else 0
            norm_val = ((-1)**deg_alpha) * coeffs[-1] if deg_alpha >= 1 else 0
            
            if deg_E % deg_alpha == 0:
                k = deg_E // deg_alpha
                trace_E_F = k * trace_val
                norm_E_F = norm_val ** k
            else:
                trace_E_F = trace_val
                norm_E_F = norm_val
                
            trace_defined = True
        except Exception:
            trace_defined = False
            
        if len(auto_polys) > 0:
            r0 = auto_polys[0].subs(x, theta_val)
            prod_sigma = alpha_val.subs(theta_val, r0)
            sum_sigma = alpha_val.subs(theta_val, r0)
            for poly in auto_polys[1:]:
                r = poly.subs(x, theta_val)
                sigma_alpha = alpha_val.subs(theta_val, r)
                sum_sigma += sigma_alpha
                prod_sigma *= sigma_alpha
        else:
            sum_sigma = 0
            prod_sigma = 1
            
        if trace_defined:
            try:
                trace_match = simplify(trace_E_F - sum_sigma) == 0
            except Exception:
                trace_match = (trace_E_F == sum_sigma)
                
            try:
                norm_match = simplify(norm_E_F - prod_sigma) == 0
            except Exception:
                norm_match = (norm_E_F == prod_sigma)
        else:
            trace_match = False
            norm_match = False
            
        neg_Q = not (trace_match and norm_match)
        
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: G = Gal(E/F) is the Galois group of the extension",
    "¬Q: The field trace and norm formulas fail for alpha"
]

N_HYP = 2
NEG_Q_INDEX = 2