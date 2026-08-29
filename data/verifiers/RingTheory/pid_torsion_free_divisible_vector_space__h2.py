import sympy
from sympy import S

# Top-level setup: named object bindings that the witness expression may reference.
Z = S.Integers
Q = S.Rationals
R = S.Reals
C = S.Complexes

def get_name(obj):
    if obj == S.Integers: return 'Z'
    if obj == S.Rationals: return 'Q'
    if obj == S.Reals: return 'R'
    if obj == S.Complexes: return 'C'
    if isinstance(obj, str):
        if obj in ['Z', 'Q', 'R', 'C', 'Z/2Z']: return obj
        s = obj.lower()
        if s in ['z', 'integers', 'integer']: return 'Z'
        if s in ['q', 'rationals', 'rational']: return 'Q'
        if s in ['r', 'reals', 'real']: return 'R'
        if s in ['c', 'complexes', 'complex']: return 'C'
        return obj
    return str(obj)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_obj = witness.get('R')
            M_obj = witness.get('M')
            K_obj = witness.get('K')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            R_obj, M_obj, K_obj = witness
        else:
            return [False] * 5
            
        r_str = get_name(R_obj)
        m_str = get_name(M_obj)
        k_str = get_name(K_obj)
        
        # H_1: R is a principal ideal domain
        h1 = r_str in ['Z', 'Q', 'R', 'C']
        
        # H_2: M is an R-module
        def is_mod(r, m):
            if r == 'Z': return m in ['Z', 'Q', 'R', 'C', 'Z/2Z']
            if r == 'Q': return m in ['Q', 'R', 'C']
            if r == 'R': return m in ['R', 'C']
            if r == 'C': return m in ['C']
            return False
        h2 = is_mod(r_str, m_str)
        
        # H_3: M is torsion-free
        def is_tf(r, m):
            if m == 'Z/2Z': return False
            return is_mod(r, m)
        h3 = is_tf(r_str, m_str)
        
        # H_4: M is divisible
        def is_div(r, m):
            if r == 'Z': return m in ['Q', 'R', 'C']
            if r in ['Q', 'R', 'C']: return is_mod(r, m)
            return False
        h4 = is_div(r_str, m_str)
        
        # ¬Q: M does NOT admit a unique K-vector space structure extending its R-module structure
        def unique_k_vs(r, m, k):
            if k not in ['Q', 'R', 'C']: return False
            subrings = {
                'Q': ['Z', 'Q'],
                'R': ['Z', 'Q', 'R'],
                'C': ['Z', 'Q', 'R', 'C']
            }
            if r not in subrings.get(k, []): return False
            frac = {'Z': 'Q', 'Q': 'Q', 'R': 'R', 'C': 'C'}
            return k == frac.get(r)
            
        neg_q = not unique_k_vs(r_str, m_str, k_str)
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is an R-module",
    "H_3: M is torsion-free",
    "H_4: M is divisible",
    "¬Q: M does not admit a unique K-vector space structure extending its R-module structure"
]

N_HYP = 4
NEG_Q_INDEX = 4