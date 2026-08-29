import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def parse_group(g):
    if isinstance(g, str):
        g_str = g.strip().lower()
        if g_str in ['q', 'rationals', 'rational numbers', '(q, +)', 'q_+', 'mathbb{q}', 'additive group of rational numbers', 'additive group of rationals']:
            return 'Q'
        if 'q^' in g_str or 'q ^' in g_str:
            return 'Q'
        if g_str in ['r', 'reals', 'real numbers', '(r, +)', 'r_+', 'mathbb{r}']:
            return 'R'
        if 'r^' in g_str or 'r ^' in g_str:
            return 'R'
        if g_str in ['c', 'complexes', 'complex numbers', '(c, +)', 'c_+', 'mathbb{c}']:
            return 'C'
        if g_str in ['q/z', 'q / z', 'rationals mod 1']:
            return 'Q/Z'
        if g_str in ['z', 'integers', '(z, +)', 'z_+', 'mathbb{z}']:
            return 'Z'
        if g_str in ['{0}', '0', 'trivial', 'trivial group', '[0]', '(0)']:
            return '{0}'
        if 'prod' in g_str and ('z_p' in g_str or 'z2' in g_str or 'z_2' in g_str):
            return 'prod Z_p'
        if 'sum' in g_str and ('z_p' in g_str or 'z2' in g_str or 'z_2' in g_str):
            return 'sum Z_p'
        if 'z' in g_str and ('p^infty' in g_str or 'p^inf' in g_str):
            return 'Z(p^infty)'
        if 'z^n' in g_str or 'baer-specker' in g_str or 'baer specker' in g_str:
            return 'Z^N'
    elif g == sympy.S.Rationals:
        return 'Q'
    elif g == sympy.S.Reals:
        return 'R'
    elif g == sympy.S.Complexes:
        return 'C'
    elif g == sympy.S.Integers:
        return 'Z'
    elif g == 0 or g == [0] or g == (0,):
        return '{0}'
    
    if hasattr(g, '__class__'):
        cname = g.__class__.__name__.lower()
        if cname in ['q', 'rationals', 'rationalgroup']:
            return 'Q'
        if cname in ['r', 'reals', 'realgroup']:
            return 'R'
        if cname in ['z', 'integers', 'integergroup']:
            return 'Z'
    
    return g

group_props = {
    'Q': {'abelian': True, 'torsion': '{0}', 'neg_q': True},
    'R': {'abelian': True, 'torsion': '{0}', 'neg_q': True},
    'C': {'abelian': True, 'torsion': '{0}', 'neg_q': True},
    'Z': {'abelian': True, 'torsion': '{0}', 'neg_q': False},
    '{0}': {'abelian': True, 'torsion': '{0}', 'neg_q': False},
    'Q/Z': {'abelian': True, 'torsion': 'Q/Z', 'neg_q': False},
    'Z(p^infty)': {'abelian': True, 'torsion': 'Z(p^infty)', 'neg_q': False},
    'prod Z_p': {'abelian': True, 'torsion': 'sum Z_p', 'neg_q': True},
    'sum Z_p': {'abelian': True, 'torsion': 'sum Z_p', 'neg_q': False},
    'Z^N': {'abelian': True, 'torsion': '{0}', 'neg_q': True},
}

def conditions(witness) -> list[bool]:
    G = witness
    T = None
    if isinstance(witness, tuple) and len(witness) == 2:
        G, T = witness
    elif isinstance(witness, dict):
        G = witness.get('G', witness)
        T = witness.get('T', None)
        
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        g_parsed = parse_group(G)
        t_parsed = parse_group(T) if T is not None else None
        
        if isinstance(g_parsed, str) and g_parsed in group_props:
            props = group_props[g_parsed]
            h1 = props['abelian']
            
            if T is None:
                h2 = True
            else:
                h2 = (t_parsed == props['torsion'])
                
            neg_q = props['neg_q']
                
        else:
            if hasattr(G, 'is_abelian'):
                h1 = bool(G.is_abelian() if callable(G.is_abelian) else G.is_abelian)
            else:
                h1 = False
                
            if hasattr(G, 'is_finite') and (G.is_finite() if callable(G.is_finite) else G.is_finite):
                if T is None:
                    h2 = True
                else:
                    h2 = (T == G)
                neg_q = False
            else:
                if T is None:
                    h2 = True
                else:
                    if hasattr(G, 'torsion_subgroup'):
                        torsion = G.torsion_subgroup() if callable(G.torsion_subgroup) else G.torsion_subgroup
                        h2 = (T == torsion)
                    else:
                        h2 = False
                        
                if hasattr(G, 'is_finitely_generated'):
                    is_fg = G.is_finitely_generated() if callable(G.is_finitely_generated) else G.is_finitely_generated
                    if is_fg:
                        neg_q = False
                    else:
                        splits = True
                        if hasattr(G, 'splits_over_torsion'):
                            splits = G.splits_over_torsion() if callable(G.splits_over_torsion) else G.splits_over_torsion
                        
                        quotient_free = True
                        if hasattr(G, 'quotient_free_abelian'):
                            quotient_free = G.quotient_free_abelian() if callable(G.quotient_free_abelian) else G.quotient_free_abelian
                            
                        neg_q = not (splits and quotient_free)
                        
                        if not hasattr(G, 'splits_over_torsion') and not hasattr(G, 'quotient_free_abelian'):
                            neg_q = False
                else:
                    splits = True
                    if hasattr(G, 'splits_over_torsion'):
                        splits = G.splits_over_torsion() if callable(G.splits_over_torsion) else G.splits_over_torsion
                    
                    quotient_free = True
                    if hasattr(G, 'quotient_free_abelian'):
                        quotient_free = G.quotient_free_abelian() if callable(G.quotient_free_abelian) else G.quotient_free_abelian
                        
                    if hasattr(G, 'splits_over_torsion') or hasattr(G, 'quotient_free_abelian'):
                        neg_q = not (splits and quotient_free)
                    else:
                        neg_q = False
                        
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: T is the subgroup of G consisting of all elements of finite order",
    "¬Q: G is not isomorphic to T ⊕ G/T, or G/T is not a free abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2