import sympy as sp
import itertools

# Top-level setup for witness expressions
x, y, z = sp.symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "If R is a commutative ring and N is its nilradical, then the nilradical 
    of the localization S^{-1}R is equal to S^{-1}N."
    
    The dropped hypothesis is that S must be a multiplicatively closed subset.
    When S is just a subset, S^{-1}N = {n/s | n \in N, s \in S} might be strictly 
    smaller than the nilradical of S^{-1}R (which has denominators in \bar{S}).
    """
    try:
        # Parse witness
        if isinstance(witness, dict):
            ideal_gens = witness.get('ideal', [])
            N_gens = witness.get('N_gens', [])
            S_gens = witness.get('S_gens', [])
            nil_elem = witness.get('nil_elem', 0)
            s_bar = witness.get('s_bar', 1)
            vars_list = witness.get('vars', [x, y, z])
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 5:
                ideal_gens = witness[0]
                N_gens = witness[1]
                S_gens = witness[2]
                nil_elem = witness[3]
                s_bar = witness[4]
                vars_list = witness[5] if len(witness) > 5 else [x, y, z]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(vars_list, str):
            vars_list = sp.symbols(vars_list)
        if not isinstance(vars_list, (list, tuple)):
            vars_list = [vars_list]
            
        ideal_gens = [sp.sympify(p) for p in ideal_gens]
        if not ideal_gens:
            ideal_gens = [sp.Integer(0)]
            
        N_gens = [sp.sympify(p) for p in N_gens]
        if not N_gens:
            N_gens = [sp.Integer(0)]
            
        S_gens = [sp.sympify(p) for p in S_gens]
        if not S_gens:
            return [False, False, False]
            
        nil_elem = sp.sympify(nil_elem)
        s_bar = sp.sympify(s_bar)
        
        # H_1: R is a commutative ring
        # We represent R as a polynomial quotient ring Q[vars] / <ideal_gens>, 
        # which is inherently commutative.
        h1 = True
        
        # H_2: N is the nilradical of R
        # We verify that the generators of N are indeed nilpotent in R.
        h2 = True
        GB_ideal = sp.groebner(ideal_gens, *vars_list)
        for g in N_gens:
            is_nil = False
            for k in range(1, 5):
                _, rem = sp.reduced(g**k, GB_ideal)
                if rem == 0:
                    is_nil = True
                    break
            if not is_nil:
                h2 = False
                break
                
        # neg_Q: The nilradical of S^{-1}R is NOT equal to S^{-1}N
        # We verify that nil_elem / s_bar is in Nilradical(S^{-1}R) but NOT in S^{-1}N.
        
        # 1. Check nil_elem is in N (so nil_elem / s_bar is in the nilradical of S^{-1}R)
        GB_N = sp.groebner(N_gens + ideal_gens, *vars_list)
        _, rem_nil = sp.reduced(nil_elem, GB_N)
        if rem_nil != 0:
            return [h1, h2, False]
            
        # 2. Check s_bar is in the multiplicative closure \bar{S}
        S_elements = S_gens + [sp.Integer(1)]
        is_s_bar_valid = False
        for combo in itertools.product(S_elements, repeat=4):
            prod = sp.Integer(1)
            for factor in combo:
                prod *= factor
            if sp.expand(s_bar - prod) == 0:
                is_s_bar_valid = True
                break
        if not is_s_bar_valid:
            return [h1, h2, False]
            
        # 3. Check impossibility: nil_elem / s_bar != n / s for all n \in N, s \in S
        # This means there is no t \in \bar{S} such that t * (nil_elem * s - n * s_bar) \in I
        t_candidates = []
        for combo in itertools.product(S_elements, repeat=3):
            prod = sp.Integer(1)
            for factor in combo:
                prod *= factor
            t_candidates.append(prod)
        t_candidates = list(set(t_candidates))
        
        neg_q = True
        for s in S_gens:
            found_solution_for_s = False
            for t in t_candidates:
                target = sp.expand(t * nil_elem * s)
                ideal_t = ideal_gens + [sp.expand(t * s_bar * n) for n in N_gens]
                GB_t = sp.groebner(ideal_t, *vars_list)
                _, rem = sp.reduced(target, GB_t)
                if rem == 0:
                    # Found a solution, so it IS in S^{-1}N
                    found_solution_for_s = True
                    break
            if found_solution_for_s:
                neg_q = False
                break
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: N is the nilradical of R",
    "¬Q: The nilradical of S^{-1}R is not equal to S^{-1}N"
]

N_HYP = 2
NEG_Q_INDEX = 2