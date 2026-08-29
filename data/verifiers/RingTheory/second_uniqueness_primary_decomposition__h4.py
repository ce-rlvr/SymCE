import sympy
from sympy import symbols, groebner, reduced, sqf_part
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness references
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def intersect_ideals(A_gens, B_gens, vars):
    t = symbols('t_intersect')
    J_gens = [t * a for a in A_gens] + [(1 - t) * b for b in B_gens]
    gb = groebner(J_gens, [t] + list(vars), order='lex')
    return [p for p in gb if t not in p.free_symbols]

def intersect_multiple(ideals_gens, vars):
    if not ideals_gens:
        return [1]
    res = ideals_gens[0]
    for i in range(1, len(ideals_gens)):
        res = intersect_ideals(res, ideals_gens[i], vars)
    return res

def ideals_equal(A_gens, B_gens, vars):
    gbA = groebner(A_gens, vars)
    gbB = groebner(B_gens, vars)
    for a in A_gens:
        if reduced(a, gbB, vars)[1] != 0: return False
    for b in B_gens:
        if reduced(b, gbA, vars)[1] != 0: return False
    return True

def is_primary(Q_gens, vars):
    gb = groebner(Q_gens, vars)
    if reduced(1, gb, vars)[1] == 0:
        return False
    
    try:
        is_linear = all(sympy.Poly(p, *vars).total_degree() == 1 for p in gb)
    except Exception:
        is_linear = False
        
    if is_linear:
        return True

    all_vars_nilpotent = True
    for v in vars:
        is_nilpotent = False
        for n in range(1, 10):
            if reduced(v**n, gb, vars)[1] == 0:
                is_nilpotent = True
                break
        if not is_nilpotent:
            all_vars_nilpotent = False
            break
    if all_vars_nilpotent:
        return True
        
    return False

def get_radical(Q_gens, vars):
    gb = groebner(Q_gens, vars)
    try:
        is_linear = all(sympy.Poly(p, *vars).total_degree() == 1 for p in gb)
    except Exception:
        is_linear = False
        
    if is_linear:
        return list(gb)
    
    if len(gb) == 1:
        return [sqf_part(gb[0])]
        
    all_vars_nilpotent = True
    for v in vars:
        is_nilpotent = False
        for n in range(1, 10):
            if reduced(v**n, gb, vars)[1] == 0:
                is_nilpotent = True
                break
        if not is_nilpotent:
            all_vars_nilpotent = False
            break
    if all_vars_nilpotent:
        return list(vars)
    
    return None

def conditions(witness) -> list[bool]:
    try:
        vars = witness['vars']
        I_gens = witness['I']
        decomp1 = witness['decomp1']
        decomp2 = witness['decomp2']
    except (KeyError, TypeError):
        return [False, False, False, False]

    # H_1: R is a commutative ring
    # Polynomial rings over fields are commutative.
    h1 = True

    # H_2: I is a proper ideal of R
    try:
        gb_I = groebner(I_gens, vars)
        h2 = (reduced(1, gb_I, vars)[1] != 0)
    except Exception:
        h2 = False

    # H_3: I = \bigcap_{i=1}^n Q_i is a minimal primary decomposition of I
    try:
        def check_decomp(decomp):
            # 1. Intersection equals I
            int_gens = intersect_multiple(decomp, vars)
            if not ideals_equal(int_gens, I_gens, vars):
                return False
            
            # 2. All components are primary
            for Q in decomp:
                if not is_primary(Q, vars):
                    return False
            
            # 3. Minimal: no component can be removed
            for i in range(len(decomp)):
                rest = decomp[:i] + decomp[i+1:]
                if not rest: continue
                int_rest = intersect_multiple(rest, vars)
                if ideals_equal(int_rest, I_gens, vars):
                    return False
            
            # 4. Minimal: radicals are distinct
            radicals = []
            for Q in decomp:
                rad = get_radical(Q, vars)
                if rad is None: return False
                radicals.append(rad)
            
            for i in range(len(radicals)):
                for j in range(i+1, len(radicals)):
                    if ideals_equal(radicals[i], radicals[j], vars):
                        return False
            return True

        h3 = check_decomp(decomp1) and check_decomp(decomp2)
    except Exception:
        h3 = False

    # ¬Q: The primary component Q_i is NOT uniquely determined by I
    try:
        def decomp_subset(d1, d2):
            for Q1 in d1:
                found = False
                for Q2 in d2:
                    if ideals_equal(Q1, Q2, vars):
                        found = True
                        break
                if not found:
                    return False
            return True
        
        same_decomps = decomp_subset(decomp1, decomp2) and decomp_subset(decomp2, decomp1)
        neg_q = not same_decomps
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a proper ideal of R",
    "H_3: I = \\bigcap_{i=1}^n Q_i is a minimal primary decomposition of I",
    "¬Q: The primary components Q_i are not uniquely determined by I"
]

N_HYP = 3
NEG_Q_INDEX = 3