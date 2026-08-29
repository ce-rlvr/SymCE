import sympy
from sympy import S
from sympy.polys.domains import CC, QQ, RR, ZZ

# Top-level setup
C = S.Complexes
R = S.Reals
Q = S.Rationals
Z = S.Integers

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: The residue field O_v / m_v is not an algebraically closed field"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        K = None
        k = None
        
        if isinstance(witness, dict):
            K = witness.get('K')
            for key in ['residue_field', 'k', 'O_v_mod_m_v', 'O_v_quo_m_v', 'residue', 'O_v/m_v']:
                if key in witness:
                    k = witness[key]
                    break
        elif hasattr(witness, 'K'):
            K = witness.K
            for attr in ['residue_field', 'k', 'O_v_mod_m_v', 'O_v_quo_m_v', 'residue']:
                if hasattr(witness, attr):
                    k = getattr(witness, attr)
                    break
        elif isinstance(witness, (list, tuple)) and len(witness) >= 2:
            K = witness[0]
            k = witness[1]
        elif isinstance(witness, str):
            s = witness.lower()
            if 'complex' in s or 'cc' in s.split() or 'algebraically closed' in s:
                h1 = True
            if 'rational' in s or 'qq' in s.split() or 'real' in s or 'rr' in s.split() or 'not algebraically closed' in s:
                neg_q = True
            return [h1, neg_q]

        # Check K
        if K in (S.Complexes, CC, C) or str(K) in ('C', 'CC', 'Complexes', 'S.Complexes'):
            h1 = True
        elif isinstance(K, bool):
            h1 = K
        elif hasattr(K, 'is_algebraically_closed') and K.is_algebraically_closed:
            h1 = True
            
        # Check k (residue field)
        if k in (S.Reals, S.Rationals, S.Integers, QQ, RR, ZZ, R, Q, Z):
            neg_q = True
        elif isinstance(k, str) and k in ('R', 'RR', 'Reals', 'S.Reals', 'Q', 'QQ', 'Rationals', 'S.Rationals', 'Z', 'ZZ', 'Integers', 'S.Integers', 'F_p', 'Fp'):
            neg_q = True
        elif isinstance(k, bool):
            neg_q = not k
        elif hasattr(k, 'is_algebraically_closed'):
            neg_q = not k.is_algebraically_closed
        elif hasattr(k, 'is_Field') or hasattr(k, 'is_Ring'):
            if k not in (CC, S.Complexes, C):
                neg_q = True
            
    except Exception:
        pass

    return [h1, neg_q]