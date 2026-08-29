import sympy as sp
import itertools

# Top-level setup
x, y, z = sp.symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In any ring, a non-zero proper ideal is primary if and only if it is a power of a prime ideal."
    
    Expected witness format:
    {
        'I_gens': [x**2, y],  # Generators of the ideal I
        'vars': [x, y],       # Variables of the polynomial ring
        'P_gens': [x, y]      # (Optional) Generators of the prime ideal P = rad(I)
    }
    """
    try:
        I_gens = witness['I_gens']
        vars = witness['vars']
        P_gens = witness.get('P_gens', None)
        if P_gens is None:
            # Infer P_gens as the variables that appear in I_gens
            P_gens = list(set().union(*[g.free_symbols for g in I_gens]))
            P_gens = sorted(P_gens, key=lambda v: v.name)
    except Exception:
        return [False, False]
        
    # H1: I is a non-zero proper ideal
    try:
        if not I_gens:
            h1 = False
        elif all(sp.expand(g) == 0 for g in I_gens):
            h1 = False
        else:
            gb_I = sp.groebner(I_gens, *vars)
            if len(gb_I.polys) == 1 and gb_I.polys[0].as_expr() == 1:
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: I is primary iff I is a power of a prime ideal (must FAIL)
    try:
        # Check if P is a maximal ideal of the form (x - a, y - b, ...)
        gb_P = sp.groebner(P_gens, *vars)
        P_is_maximal = True
        if len(gb_P.polys) != len(vars):
            P_is_maximal = False
        else:
            matched_vars = set()
            for p in gb_P.polys:
                expr = p.as_expr()
                fs = expr.free_symbols
                if len(fs) != 1:
                    P_is_maximal = False
                    break
                v = list(fs)[0]
                if sp.degree(expr, v) != 1:
                    P_is_maximal = False
                    break
                matched_vars.add(v)
            if matched_vars != set(vars):
                P_is_maximal = False
                
        # Check if I is a subset of P
        I_subset_P = True
        for g in I_gens:
            rem = sp.reduced(g, P_gens, *vars)[1]
            if sp.expand(rem) != 0:
                I_subset_P = False
                break
                
        # Check if P^k is a subset of I for some k
        P_k_subset_I = False
        k_found = -1
        for k in range(1, 11):
            Pk_gens = [sp.prod(comb) for comb in itertools.combinations_with_replacement(P_gens, k)]
            subset = True
            for g in Pk_gens:
                rem = sp.reduced(g, I_gens, *vars)[1]
                if sp.expand(rem) != 0:
                    subset = False
                    break
            if subset:
                P_k_subset_I = True
                k_found = k
                break
                
        # If P is maximal and P^k <= I <= P, then rad(I) = P, which implies I is primary.
        is_primary = P_is_maximal and I_subset_P and P_k_subset_I
        
        # Check if I is a power of P
        is_power_of_prime = False
        max_m = k_found if k_found != -1 else 10
        expr_I = [p.as_expr() for p in gb_I.polys]
        for m in range(1, max_m + 1):
            Pm_gens = [sp.prod(comb) for comb in itertools.combinations_with_replacement(P_gens, m)]
            gb_Pm = sp.groebner(Pm_gens, *vars)
            expr_Pm = [p.as_expr() for p in gb_Pm.polys]
            if expr_I == expr_Pm:
                is_power_of_prime = True
                break
                
        # The conclusion fails if the equivalence does not hold
        neg_q = (is_primary and not is_power_of_prime) or (not is_primary and is_power_of_prime and P_is_maximal)
        
    except Exception:
        neg_q = False
        
    return [h1, bool(neg_q)]

CONDITION_LABELS = [
    "H_1: I is a non-zero proper ideal of R",
    "¬Q: The equivalence 'I is primary iff I is a power of a prime ideal' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1