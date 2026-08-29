import sympy as sp
from sympy import Poly, groebner, reduced

# Top-level setup for potential witness expressions
X, Y, Z, W = sp.symbols('X Y Z W')
x, y, z = sp.symbols('x y z')
t, u, v, w = sp.symbols('t u v w')
a, b, c, d = sp.symbols('a b c d')

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with:
      - 'ring_vars': list of variables generating the base ring R
      - 'ring_ideal': list of polynomials generating the ideal to quotient by
      - 'poly_vars': list of two variables [x, y] for the polynomial ring
      - 'f': polynomial f in R[x, y]
      - 'g': polynomial g in R[y]
    """
    try:
        ring_vars = witness['ring_vars']
        ring_ideal = witness['ring_ideal']
        poly_vars = witness['poly_vars']
        f = witness['f']
        g = witness['g']
        
        if len(poly_vars) != 2:
            return [False, False, False]
            
        var_x, var_y = poly_vars
        
        # H_1: R is a commutative ring with identity
        # By construction, a quotient of a polynomial ring over Q is a commutative ring with identity.
        h1 = isinstance(ring_vars, list) and isinstance(ring_ideal, list)
        
        # H_2: g is a polynomial in R[y], where x and y are distinct, independent variables
        h2 = (var_x not in g.free_symbols) and (var_x != var_y)
        
        # Compute content ideals
        f_poly = Poly(f, var_x, var_y)
        g_poly = Poly(g, var_x, var_y)
        fg_poly = Poly((f * g).expand(), var_x, var_y)
        
        c_f = [sp.sympify(coeff) for coeff in f_poly.coeffs()]
        c_g = [sp.sympify(coeff) for coeff in g_poly.coeffs()]
        c_fg = [sp.sympify(coeff) for coeff in fg_poly.coeffs()]
        
        # Product of content ideals c(f)c(g)
        c_f_c_g = [a_coeff * b_coeff for a_coeff in c_f for b_coeff in c_g]
        
        # Helper to check if two ideals are equal in the quotient ring R
        def ideals_equal(gens1, gens2, ideal, vars):
            if not vars:
                is_zero1 = all(sp.simplify(gen) == 0 for gen in gens1)
                is_zero2 = all(sp.simplify(gen) == 0 for gen in gens2)
                return is_zero1 == is_zero2
                
            list1 = [gen for gen in gens1 + ideal if sp.simplify(gen) != 0]
            list2 = [gen for gen in gens2 + ideal if sp.simplify(gen) != 0]
            
            # Check if gens1 is contained in <gens2 U ideal>
            if list2:
                GB2 = groebner(list2, *vars)
                for gen in gens1:
                    if sp.simplify(reduced(gen, GB2, *vars)[1]) != 0:
                        return False
            else:
                if any(sp.simplify(gen) != 0 for gen in gens1):
                    return False
                    
            # Check if gens2 is contained in <gens1 U ideal>
            if list1:
                GB1 = groebner(list1, *vars)
                for gen in gens2:
                    if sp.simplify(reduced(gen, GB1, *vars)[1]) != 0:
                        return False
            else:
                if any(sp.simplify(gen) != 0 for gen in gens2):
                    return False
                    
            return True
            
        # Q: The content ideal of fg in R[x,y] is equal to the product of c(f) and c(g) in R
        q = ideals_equal(c_fg, c_f_c_g, ring_ideal, ring_vars)
        
        # We want the conclusion to FAIL
        neg_q = not q
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: g is a polynomial in R(y), where x and y are distinct, independent variables",
    "not Q: The content ideal of fg in R(x,y) is not equal to the product of c(f) and c(g) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2