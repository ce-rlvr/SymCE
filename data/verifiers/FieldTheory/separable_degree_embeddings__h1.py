import sympy
from sympy import S
from sympy.abc import x, y, z

QQ = S.Rationals
ZZ = S.Integers
RR = S.Reals
CC = S.Complexes

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            K, E, Omega = witness
        elif isinstance(witness, dict):
            K = witness.get('K')
            E = witness.get('E')
            Omega = witness.get('Omega')
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = False
        omega_str = str(Omega)
        k_str = str(K)
        
        if Omega == CC or omega_str in ['CC', 'C', 'Complexes', 'ComplexField', 'S.Complexes']:
            if K in [QQ, RR, ZZ] or k_str in ['QQ', 'Q', 'Rationals', 'ZZ', 'Z', 'Integers', 'RR', 'R', 'Reals', 'S.Rationals', 'S.Reals', 'S.Integers']:
                h1 = True
        elif getattr(Omega, 'is_algebraically_closed', False):
            if getattr(Omega, 'contains', lambda _x: False)(K):
                h1 = True
            elif getattr(K, 'is_subset', lambda _x: False)(Omega):
                h1 = True
            elif K == QQ and getattr(Omega, 'characteristic', None) == 0:
                h1 = True
    except Exception:
        h1 = False
        
    try:
        neg_q = False
        e_str = str(E)
        
        if hasattr(E, 'is_FracField') and E.is_FracField:
            neg_q = True
        elif hasattr(E, 'is_PolyRing') and E.is_PolyRing:
            neg_q = True
        elif E in [CC, RR] or e_str in ['CC', 'C', 'Complexes', 'ComplexField', 'RR', 'R', 'Reals', 'RealField', 'S.Complexes', 'S.Reals']:
            neg_q = True
        elif getattr(E, 'is_infinite_extension', False):
            neg_q = True
        elif getattr(E, 'is_finite_extension', True) is False:
            neg_q = True
        elif '(x)' in e_str or '(t)' in e_str or 'transcendental' in e_str.lower() or 'infinite' in e_str.lower():
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Omega is an algebraically closed field containing K",
    "not Q: The number of distinct K-algebra homomorphisms from E to Omega is not exactly the separable degree"
]

N_HYP = 1
NEG_Q_INDEX = 1