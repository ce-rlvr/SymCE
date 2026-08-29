import sympy as sp
import itertools
from sympy.abc import x, y, z

def is_zero_divisor(f, I_gens, vars):
    try:
        if not I_gens:
            return sp.simplify(f) == 0
        
        GB_I = sp.groebner(I_gens, *vars).polys
        if any(p.is_constant() and p.LC() != 0 for p in GB_I):
            return False
        
        _, rem = sp.reduced(f, GB_I, *vars)
        if rem == 0:
            return True
            
        t_name = 't_dummy'
        while any(str(v) == t_name for v in vars):
            t_name += '_'
        t = sp.symbols(t_name)
        
        J_gens = [t * h for h in I_gens] + [(1 - t) * f]
        GB_J = sp.groebner(J_gens, t, *vars, order='lex').polys
        
        intersect_gens = [p for p in GB_J if not p.has(t)]
        
        for g in intersect_gens:
            g_expr = g.as_expr()
            f_expr = f if not hasattr(f, 'as_expr') else f.as_expr()
            
            q = sp.cancel(g_expr / f_expr)
            
            try:
                _, rem_q = sp.reduced(q, GB_I, *vars)
            except Exception:
                continue
                
            if rem_q != 0:
                return True
                
        return False
    except Exception:
        return True

def is_regular_sequence(seq, vars):
    try:
        I_gens = []
        for f in seq:
            if is_zero_divisor(f, I_gens, vars):
                return False
            I_gens.append(f)
        
        GB_I = sp.groebner(I_gens, *vars).polys
        if any(p.is_constant() and p.LC() != 0 for p in GB_I):
            return False
            
        return True
    except Exception:
        return False

def is_maximal_ideal(m_gens, vars):
    try:
        GB = sp.groebner(m_gens, *vars).polys
        if len(GB) != len(vars):
            return False
        
        found_vars = set()
        for p in GB:
            expr = p.as_expr()
            fs = expr.free_symbols.intersection(set(vars))
            if len(fs) != 1:
                return False
            v = list(fs)[0]
            if sp.degree(expr, v) != 1:
                return False
            found_vars.add(v)
        return found_vars == set(vars)
    except Exception:
        return False

def in_ideal(seq, m_gens, vars):
    try:
        GB = sp.groebner(m_gens, *vars).polys
        for f in seq:
            _, rem = sp.reduced(f, GB, *vars)
            if rem != 0:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False, False, False]
            
        vars_list = witness.get('vars')
        m_gens = witness.get('m_gens')
        seq = witness.get('seq')
        
        if vars_list is None or m_gens is None or seq is None:
            return [False, False, False, False]
            
        if not isinstance(vars_list, list) or not isinstance(m_gens, list) or not isinstance(seq, list):
            return [False, False, False, False]
            
        if not all(isinstance(v, sp.Symbol) for v in vars_list):
            return [False, False, False, False]
            
        for f in seq + m_gens:
            if not hasattr(f, 'is_polynomial') or f.is_polynomial(*vars_list) is not True:
                return [False, False, False, False]
                
        # H1: R is a commutative Noetherian ring
        # Implied by the fact that we are working in a polynomial ring over QQ
        h1 = True
        
        # H2: The sequence x_1, ..., x_n is a regular sequence in R
        h2 = is_regular_sequence(seq, vars_list)
        
        # H3: The elements x_1, ..., x_n belong to the maximal ideal m
        h3 = is_maximal_ideal(m_gens, vars_list) and in_ideal(seq, m_gens, vars_list)
        
        # neg_Q: There exists a permutation of the sequence that is NOT a regular sequence in R
        neg_q = False
        for perm in itertools.permutations(seq):
            if not is_regular_sequence(perm, vars_list):
                neg_q = True
                break
                
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: The sequence x_1, ..., x_n is a regular sequence in R",
    "H_3: The elements x_1, ..., x_n belong to the maximal ideal m",
    "¬Q: There exists a permutation of the sequence that is NOT a regular sequence in R"
]

N_HYP = 3
NEG_Q_INDEX = 3