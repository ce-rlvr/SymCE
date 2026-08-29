import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z, t
from sympy.ntheory import is_square_free
from sympy import sqf_list

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

CONDITION_LABELS = [
    "H_1: R is integrally closed in its field of fractions",
    "¬Q: The polynomial ring over R is not integrally closed in its field of fractions"
]

N_HYP = 1
NEG_Q_INDEX = 1

def check_witness(witness):
    n = None
    if isinstance(witness, int):
        n = witness
    elif hasattr(witness, 'is_Integer') and witness.is_Integer:
        n = int(witness)
    elif isinstance(witness, str):
        s = witness.strip().replace(' ', '')
        try:
            if s.startswith('Z/') and s.endswith('Z'):
                n = int(s[2:-1])
            elif s.startswith('Z_'):
                n = int(s[2:])
            elif s.startswith('Z'):
                n = int(s[1:])
        except Exception:
            pass
            
    if hasattr(witness, 'mod'):
        try:
            n = int(witness.mod)
        except Exception:
            pass
            
    if n is not None:
        if n == 0 or n == 1 or n == -1:
            return True, False
        if n < 0:
            n = -n
        return True, not is_square_free(n)
        
    if hasattr(witness, 'base') and hasattr(witness, 'ideal'):
        try:
            gens = witness.ideal.gens
            if len(gens) == 1:
                gen = gens[0]
                if isinstance(gen, int) or (hasattr(gen, 'is_Integer') and gen.is_Integer):
                    n = int(gen)
                    if n == 0 or n == 1 or n == -1: return True, False
                    if n < 0: n = -n
                    return True, not is_square_free(n)
                if hasattr(gen, 'free_symbols') and len(gen.free_symbols) <= 1:
                    if gen == 0:
                        return True, False
                    factors = sqf_list(gen)
                    is_sqf = all(exp == 1 for f, exp in factors[1])
                    return True, not is_sqf
        except Exception:
            pass
            
    if isinstance(witness, tuple) and len(witness) == 2:
        ring, ideal_gen = witness
        if isinstance(ideal_gen, int) or (hasattr(ideal_gen, 'is_Integer') and ideal_gen.is_Integer):
            n = int(ideal_gen)
            if n == 0 or n == 1 or n == -1: return True, False
            if n < 0: n = -n
            return True, not is_square_free(n)
        try:
            if hasattr(ideal_gen, 'free_symbols') and len(ideal_gen.free_symbols) <= 1:
                if ideal_gen == 0:
                    return True, False
                factors = sqf_list(ideal_gen)
                is_sqf = all(exp == 1 for f, exp in factors[1])
                return True, not is_sqf
        except Exception:
            pass

    try:
        if hasattr(witness, 'free_symbols') and len(witness.free_symbols) == 1:
            if witness == 0:
                return True, False
            factors = sqf_list(witness)
            is_sqf = all(exp == 1 for f, exp in factors[1])
            return True, not is_sqf
    except Exception:
        pass

    return False, False

def conditions(witness):
    try:
        h1, neg_q = check_witness(witness)
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]