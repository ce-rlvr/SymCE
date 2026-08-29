import sympy
from sympy import groebner, Poly, reduced
from sympy.abc import x, y, z, a, b, c, d, w

def extract_polys(witness):
    if isinstance(witness, (list, tuple, set)):
        return list(witness)
    if hasattr(witness, 'ideal') and hasattr(witness.ideal, 'gens'):
        return list(witness.ideal.gens)
    if hasattr(witness, 'base_ideal') and hasattr(witness.base_ideal, 'gens'):
        return list(witness.base_ideal.gens)
    if isinstance(witness, sympy.Expr):
        return [witness]
    return None

def conditions(witness) -> list[bool]:
    try:
        polys = extract_polys(witness)
        if polys is None or not polys:
            return [False, False]
            
        free_syms = set()
        for p in polys:
            if hasattr(p, 'free_symbols'):
                free_syms.update(p.free_symbols)
        if not free_syms:
            return [False, False]
            
        V = tuple(sorted(free_syms, key=lambda s: s.name))
        
        # Compute Groebner basis
        G = groebner(polys, *V, order='lex')
        G_exprs = list(G)
        LMs = [Poly(g, *V).LM() for g in G_exprs]
        
        # Check if the ideal is zero-dimensional
        is_zero_dim = True
        for i in range(len(V)):
            has_power = False
            for lm in LMs:
                if lm[i] > 0 and all(lm[j] == 0 for j in range(len(V)) if j != i):
                    has_power = True
                    break
            if not has_power:
                is_zero_dim = False
                break
                
        if not is_zero_dim:
            return [False, False]
            
        # Find all standard monomials
        standard = [(0,)*len(V)]
        queue = [(0,)*len(V)]
        while queue:
            m = queue.pop(0)
            for i in range(len(V)):
                m_new = list(m)
                m_new[i] += 1
                m_new = tuple(m_new)
                if m_new not in standard:
                    divisible = False
                    for lm in LMs:
                        if all(m_new[j] >= lm[j] for j in range(len(V))):
                            divisible = True
                            break
                    if not divisible:
                        standard.append(m_new)
                        queue.append(m_new)
                        
        # Check if the ring is local at the origin (radical is the maximal ideal)
        is_local = True
        for i in range(len(V)):
            v = V[i]
            v_nilpotent = False
            for k in range(1, len(standard) + 2):
                rem = reduced(v**k, G_exprs, V)[1]
                if rem == 0:
                    v_nilpotent = True
                    break
            if not v_nilpotent:
                is_local = False
                break
                
        if not is_local:
            return [False, False]
            
        h1_ok = True
        
        # Compute the socle dimension to check if the ring is Gorenstein
        # The socle is the annihilator of the maximal ideal (x, y, ...)
        M = sympy.zeros(len(V) * len(standard), len(standard))
        for i in range(len(V)):
            for j, m in enumerate(standard):
                m_expr = sympy.Mul(*[V[k]**m[k] for k in range(len(V))])
                term = V[i] * m_expr
                rem = reduced(term, G_exprs, V)[1]
                if rem != 0:
                    rem_poly = Poly(rem, *V)
                    for monom, coeff in rem_poly.terms():
                        if monom in standard:
                            k_idx = standard.index(monom)
                            M[i * len(standard) + k_idx, j] = coeff
                            
        rank = M.rank()
        socle_dim = len(standard) - rank
        
        # A local Artinian ring is Gorenstein iff its socle dimension is exactly 1.
        # If it is not Gorenstein, its injective dimension is infinite (conclusion fails).
        neg_q_ok = (socle_dim != 1)
        
        return [h1_ok, neg_q_ok]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian local ring",
    "¬Q: The injective dimension of R is infinite or not equal to its Krull dimension"
]
N_HYP = 1
NEG_Q_INDEX = 1