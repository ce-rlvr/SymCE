import sympy
from sympy import symbols
from sympy.polys.domains import QQ, ZZ, RR, CC

try:
    from sympy.polys.domains import GF
except ImportError:
    GF = sympy.GF

# Top-level setup for witness expressions
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: P is the prime subfield of K",
    "¬Q: The transcendence degree of K_bar over P is not equal to the transcendence degree of K over P"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # The witness can be a dictionary or a tuple (K, P, K_bar)
        if isinstance(witness, dict):
            K = witness.get('K')
            P = witness.get('P')
            K_bar = witness.get('K_bar')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            K, P, K_bar = witness
        else:
            return [False, False, False]
            
        # H_1: K is a field
        h1 = bool(getattr(K, 'is_Field', False))
        
        def get_char(domain):
            if hasattr(domain, 'characteristic'):
                c = domain.characteristic
                if callable(c):
                    return c()
                return c
            if hasattr(domain, 'domain'):
                return get_char(domain.domain)
            return None

        # H_2: P is the prime subfield of K
        char = get_char(K)
        if char == 0:
            expected_P = QQ
        elif char is not None and char > 0:
            expected_P = GF(char)
        else:
            expected_P = None
            
        h2 = (P == expected_P) and bool(getattr(P, 'is_Field', False))
        
        # neg_Q: trdeg(K_bar / P) != trdeg(K / P)
        def get_trdeg(domain):
            if hasattr(domain, 'trdeg'):
                t = domain.trdeg
                return t() if callable(t) else t
            if domain in (QQ, ZZ, RR, CC):
                return 0
            c = get_char(domain)
            if c is not None and c > 0 and not hasattr(domain, 'gens'):
                return 0
            if hasattr(domain, 'gens'):
                if hasattr(domain, 'ext'):
                    return get_trdeg(domain.domain)
                return len(domain.gens) + get_trdeg(getattr(domain, 'domain', QQ))
            return 0
            
        trdeg_K = get_trdeg(K)
        trdeg_K_bar = get_trdeg(K_bar)
        
        # K_bar should be a field (or at least not explicitly marked as a non-field like a PolyRing)
        k_bar_is_field = getattr(K_bar, 'is_Field', True)
        neg_q = bool(k_bar_is_field) and (trdeg_K_bar != trdeg_K)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]