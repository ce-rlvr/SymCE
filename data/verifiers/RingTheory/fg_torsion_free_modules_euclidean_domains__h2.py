import sympy
from sympy import ZZ, QQ, RR, CC, Symbol, S

x = Symbol('x')

def is_euclidean_domain(R):
    if R in (ZZ, QQ, RR, CC, S.Integers, S.Rationals, S.Reals, S.Complexes):
        return True
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if hasattr(R, 'is_PID') and R.is_PID:
        return True
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        if len(R.symbols) == 1 and getattr(R.domain, 'is_Field', False):
            return True
    if str(R) in ['ZZ', 'QQ', 'RR', 'CC', 'Integers', 'Rationals', 'Reals', 'Complexes']:
        return True
    return False

def is_torsion_free(R, M):
    if R == M:
        return True
    if R in (ZZ, S.Integers) or str(R) in ('ZZ', 'Integers'):
        if M in (QQ, RR, CC, S.Rationals, S.Reals, S.Complexes) or str(M) in ('QQ', 'RR', 'CC', 'Rationals', 'Reals', 'Complexes'):
            return True
    if R in (QQ, S.Rationals) or str(R) in ('QQ', 'Rationals'):
        if M in (RR, CC, S.Reals, S.Complexes) or str(M) in ('RR', 'CC', 'Reals', 'Complexes'):
            return True
    if R in (RR, S.Reals) or str(R) in ('RR', 'Reals'):
        if M in (CC, S.Complexes) or str(M) in ('CC', 'Complexes'):
            return True
    if hasattr(R, 'frac_field'):
        try:
            if M == R.frac_field():
                return True
        except Exception:
            pass
    if hasattr(M, 'domain') and M.domain == R:
        return True
    return False

def is_free_module(R, M):
    if R == M:
        return True
    if R in (QQ, RR, CC, S.Rationals, S.Reals, S.Complexes) or str(R) in ('QQ', 'RR', 'CC', 'Rationals', 'Reals', 'Complexes'):
        return True
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if R in (ZZ, S.Integers) or str(R) in ('ZZ', 'Integers'):
        if M in (QQ, RR, CC, S.Rationals, S.Reals, S.Complexes) or str(M) in ('QQ', 'RR', 'CC', 'Rationals', 'Reals', 'Complexes'):
            return False
    if hasattr(R, 'frac_field'):
        try:
            if M == R.frac_field():
                if hasattr(R, 'is_Field') and not R.is_Field:
                    return False
                if R in (ZZ, S.Integers) or str(R) in ('ZZ', 'Integers'):
                    return False
        except Exception:
            pass
    if hasattr(M, 'domain') and M.domain == R:
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            M = witness.get('M', witness.get('module', None))
            if M is None:
                return [False, False, False]
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        elif isinstance(witness, str):
            s = witness.replace(' ', '').replace('(', '').replace(')', '')
            parts = s.split(',')
            if len(parts) == 2:
                mapping = {'ZZ': ZZ, 'QQ': QQ, 'RR': RR, 'CC': CC, 
                           'S.Integers': S.Integers, 'S.Rationals': S.Rationals,
                           'S.Reals': S.Reals, 'S.Complexes': S.Complexes}
                R = mapping.get(parts[0], parts[0])
                M = mapping.get(parts[1], parts[1])
            else:
                R = ZZ
                mapping = {'QQ': QQ, 'RR': RR, 'CC': CC, 
                           'S.Rationals': S.Rationals, 'S.Reals': S.Reals, 'S.Complexes': S.Complexes}
                M = mapping.get(s, s)
        else:
            R = ZZ
            M = witness
            
        try:
            h1 = bool(is_euclidean_domain(R))
        except Exception:
            h1 = False
            
        try:
            h2 = bool(is_torsion_free(R, M))
        except Exception:
            h2 = False
            
        try:
            neg_q = not bool(is_free_module(R, M))
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: M is a torsion-free module",
    "¬Q: M is not a free module"
]

N_HYP = 2
NEG_Q_INDEX = 2