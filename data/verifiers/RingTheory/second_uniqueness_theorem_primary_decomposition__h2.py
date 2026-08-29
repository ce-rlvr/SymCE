import sympy
from sympy import symbols, groebner

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, t, u, v, w = symbols('x y z t u v w')

def contains_ideal(I_gens, J_gens, vars):
    """Checks if ideal J is contained in ideal I."""
    if not I_gens or all(g == 0 for g in I_gens):
        return not J_gens or all(g == 0 for g in J_gens)
    try:
        G = groebner(I_gens, vars)
        for g in J_gens:
            if G.reduce(g)[1] != 0:
                return False
        return True
    except Exception:
        return False

def ideals_equal(I_gens, J_gens, vars):
    """Checks if ideal I equals ideal J."""
    return contains_ideal(I_gens, J_gens, vars) and contains_ideal(J_gens, I_gens, vars)

def intersect_ideals(I_gens, J_gens, vars):
    """Computes the intersection of two ideals using Groebner bases."""
    if not I_gens or not J_gens:
        return []
    t_var = symbols('t_intersect_123456789')
    new_vars = (t_var,) + tuple(vars)
    eqs = [t_var * g for g in I_gens] + [(1 - t_var) * g for g in J_gens]
    G = groebner(eqs, new_vars, order='lex')
    intersection = []
    for g in G:
        if t_var not in g.free_symbols:
            intersection.append(g)
    return intersection

def intersect_multiple(ideals, vars):
    """Computes the intersection of a list of ideals."""
    if not ideals:
        return [1]
    res = ideals[0]
    for I in ideals[1:]:
        res = intersect_ideals(res, I, vars)
    return res

def is_in_radical(p, Q_gens, vars):
    """Checks if polynomial p is in the radical of Q using the Rabinowitsch trick."""
    w_var = symbols('w_rabinowitsch_123456789')
    new_vars = (w_var,) + tuple(vars)
    eqs = list(Q_gens) + [1 - w_var * p]
    G = groebner(eqs, new_vars)
    return len(G) == 1 and G[0] == 1

def is_radical(P_gens, Q_gens, vars):
    """Checks if P is the radical of Q (assuming P is prime)."""
    if not contains_ideal(P_gens, Q_gens, vars):
        return False
    if not Q_gens or all(g == 0 for g in Q_gens):
        return all(p == 0 for p in P_gens)
    for p in P_gens:
        if not is_in_radical(p, Q_gens, vars):
            return False
    return True

def is_isolated(P_target, P_list, vars):
    """Checks if P_target is an isolated (minimal) prime among P_list."""
    found = False
    for P in P_list:
        if ideals_equal(P_target, P, vars):
            found = True
            break
    if not found:
        return False
    
    for P in P_list:
        if ideals_equal(P_target, P, vars):
            continue
        if contains_ideal(P_target, P, vars):
            # P is strictly contained in P_target, so P_target is not minimal
            return False
    return True

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness should be a dictionary with:
      - 'vars': tuple of SymPy symbols (e.g., (x, y))
      - 'I': list of generators for the ideal I
      - 'decomps': list of minimal primary decompositions, where each decomposition
                   is a list of dicts {'Q': [gens], 'P': [gens]}
      - 'P_target': list of generators for the isolated prime ideal P_i
    """
    # H_1: R is a commutative Noetherian ring
    try:
        vars_tuple = witness.get('vars')
        h1 = isinstance(vars_tuple, (tuple, list)) and len(vars_tuple) > 0 and all(hasattr(v, 'free_symbols') for v in vars_tuple)
    except Exception:
        h1 = False

    # H_2: I = Q_1 \cap Q_2 \cap \dots \cap Q_n is a minimal primary decomposition of I
    try:
        h2 = True
        I_gens = witness.get('I')
        decomps = witness.get('decomps')
        vars_tuple = witness.get('vars')
        
        if not decomps or not isinstance(decomps, list):
            h2 = False
        else:
            for decomp in decomps:
                Q_list = [comp['Q'] for comp in decomp]
                intersection = intersect_multiple(Q_list, vars_tuple)
                if not ideals_equal(I_gens, intersection, vars_tuple):
                    h2 = False
                    break
                
                minimal = True
                for i in range(len(Q_list)):
                    rest = Q_list[:i] + Q_list[i+1:]
                    if not rest:
                        continue
                    int_rest = intersect_multiple(rest, vars_tuple)
                    if ideals_equal(intersection, int_rest, vars_tuple):
                        minimal = False
                        break
                if not minimal:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: P_i is an isolated (minimal) prime ideal associated to I, where P_i is the radical of Q_i
    try:
        h3 = True
        P_target = witness.get('P_target')
        decomps = witness.get('decomps')
        vars_tuple = witness.get('vars')
        
        if not decomps or not isinstance(decomps, list):
            h3 = False
        else:
            for decomp in decomps:
                P_list = [comp['P'] for comp in decomp]
                Q_list = [comp['Q'] for comp in decomp]
                
                if not any(ideals_equal(P_target, P, vars_tuple) for P in P_list):
                    h3 = False
                    break
                    
                if not is_isolated(P_target, P_list, vars_tuple):
                    h3 = False
                    break
                    
                for P, Q in zip(P_list, Q_list):
                    if not is_radical(P, Q, vars_tuple):
                        h3 = False
                        break
                if not h3:
                    break
                    
                for P in P_list:
                    if contains_ideal(P, [1], vars_tuple): # Check proper ideal
                        h3 = False
                        break
                if not h3:
                    break
                    
                for i in range(len(P_list)):
                    for j in range(i+1, len(P_list)):
                        if ideals_equal(P_list[i], P_list[j], vars_tuple):
                            h3 = False
                            break
                    if not h3:
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # ¬Q: The primary component Q_i is NOT uniquely determined by I and P_i
    try:
        P_target = witness.get('P_target')
        decomps = witness.get('decomps')
        vars_tuple = witness.get('vars')
        
        Q_targets = []
        if decomps and isinstance(decomps, list):
            for decomp in decomps:
                for comp in decomp:
                    if ideals_equal(P_target, comp['P'], vars_tuple):
                        Q_targets.append(comp['Q'])
                        break
            
        neg_q = False
        if len(Q_targets) >= 2:
            for i in range(len(Q_targets)):
                for j in range(i+1, len(Q_targets)):
                    if not ideals_equal(Q_targets[i], Q_targets[j], vars_tuple):
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: I = Q_1 \\cap Q_2 \\cap \\dots \\cap Q_n is a minimal primary decomposition of I",
    "H_3: P_i is an isolated (minimal) prime ideal associated to I, where P_i is the radical of Q_i",
    "¬Q: The primary component Q_i is NOT uniquely determined by I and P_i"
]

N_HYP = 3
NEG_Q_INDEX = 3