import sympy as sp
from sympy.abc import x, y, z, t, u, v, w

CONDITION_LABELS = [
    "H_1: R and S are graded rings",
    "¬Q: The kernel of f is not a homogeneous ideal of R"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture:
    "Let R and S be graded rings. The kernel of f is a homogeneous ideal of R."
    
    The witness should be a dictionary specifying:
      - 'R_gens': list of generators for R (e.g., ['x', 'y'])
      - 'S_gens': list of generators for S (e.g., ['t'])
      - 'R_grading': list of positive integer degrees for R_gens (e.g., [1, 1])
      - 'S_grading': list of positive integer degrees for S_gens (e.g., [1])
      - 'f_map': dictionary mapping R_gens to polynomials in S_gens (e.g., {'x': 't', 'y': 't + 1'})
    """
    try:
        if not isinstance(witness, dict):
            return [False, False]
            
        R_gens = [sp.sympify(g) for g in witness.get('R_gens', [])]
        S_gens = [sp.sympify(g) for g in witness.get('S_gens', [])]
        R_grading = witness.get('R_grading', [])
        S_grading = witness.get('S_grading', [])
        f_map_raw = witness.get('f_map', {})
        
        # Generators must be symbols
        if not all(isinstance(g, sp.Symbol) for g in R_gens):
            return [False, False]
        if not all(isinstance(g, sp.Symbol) for g in S_gens):
            return [False, False]
            
        # H_1: R and S are graded rings (represented by polynomial rings with positive integer gradings)
        h1 = (isinstance(R_grading, (list, tuple)) and 
              isinstance(S_grading, (list, tuple)) and
              len(R_gens) == len(R_grading) and 
              len(S_gens) == len(S_grading) and
              len(R_gens) > 0 and
              all(isinstance(d, int) and d > 0 for d in R_grading) and 
              all(isinstance(d, int) and d > 0 for d in S_grading))
              
        if not h1:
            return [False, False]
            
        f_map = {sp.sympify(k): sp.sympify(val) for k, val in f_map_raw.items()}
        
        # f must be defined on all generators of R
        if set(f_map.keys()) != set(R_gens):
            return [False, False]
            
        # f must map to polynomials in S
        for val in f_map.values():
            if S_gens:
                if not val.is_polynomial(*S_gens):
                    return [False, False]
            else:
                if not val.is_number:
                    return [False, False]
            if not val.free_symbols.issubset(set(S_gens)):
                return [False, False]
                
        # Use dummy variables for S to avoid any overlap with R_gens during Groebner basis computation
        dummy_S_gens = [sp.Dummy(f"S_{i}") for i in range(len(S_gens))]
        dummy_map = dict(zip(S_gens, dummy_S_gens))
        
        f_map_dummy = {k: val.subs(dummy_map) for k, val in f_map.items()}
        
        # Compute the kernel of f using elimination ideal
        # I = <x_i - f(x_i)> in k[S_gens, R_gens]
        I_gens = [g - f_map_dummy[g] for g in R_gens]
        
        # Lexicographic order with S_gens > R_gens eliminates S_gens
        order = dummy_S_gens + R_gens
        gb = sp.groebner(I_gens, *order, order='lex')
        
        # Extract the reduced Groebner basis of the kernel (polynomials only in R_gens)
        ker_f_gens = []
        for p in gb:
            if not any(p.has(s) for s in dummy_S_gens):
                ker_f_gens.append(p)
                
        # Check if the kernel is a homogeneous ideal
        # An ideal is homogeneous iff its reduced Groebner basis consists of homogeneous polynomials
        is_homogeneous_ideal = True
        for p in ker_f_gens:
            p_poly = sp.Poly(p, *R_gens)
            terms = p_poly.terms()
            if not terms:
                continue
            
            degrees = []
            for powers, coeff in terms:
                deg = sum(pw * g for pw, g in zip(powers, R_grading))
                degrees.append(deg)
                
            if len(set(degrees)) > 1:
                is_homogeneous_ideal = False
                break
                
        neg_q = not is_homogeneous_ideal
        
        return [h1, neg_q]
    except Exception:
        return [False, False]