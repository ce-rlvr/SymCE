import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R and S are integral domains",
    "H_2: f is an injective ring homomorphism from R to S",
    "¬Q: There does not exist a unique injective ring homomorphism from K to L extending f"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    if callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    # 1. Check if witness is a property dictionary or object
    try:
        if isinstance(witness, dict) and 'R_is_integral_domain' in witness:
            h1 = bool(witness.get('R_is_integral_domain') and witness.get('S_is_integral_domain'))
            h2 = bool(witness.get('f_is_injective_ring_homomorphism'))
            neg_q = not bool(witness.get('unique_extension_exists'))
            return [h1, h2, neg_q]
            
        if hasattr(witness, 'R_is_integral_domain'):
            h1 = bool(getattr(witness, 'R_is_integral_domain') and getattr(witness, 'S_is_integral_domain'))
            h2 = bool(getattr(witness, 'f_is_injective_ring_homomorphism'))
            neg_q = not bool(getattr(witness, 'unique_extension_exists'))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a concrete tuple/dict/object
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            f = witness.get('f')
            K = witness.get('K')
            L = witness.get('L')
        elif isinstance(witness, (tuple, list)) and len(witness) == 5:
            R, S, f, K, L = witness
        else:
            R = getattr(witness, 'R', None)
            S = getattr(witness, 'S', None)
            f = getattr(witness, 'f', None)
            K = getattr(witness, 'K', None)
            L = getattr(witness, 'L', None)

        def is_id(domain):
            if isinstance(domain, str):
                return domain in ['ZZ', 'QQ', 'RR', 'CC', 'Z', 'Q', 'R', 'C'] or 'GF' in domain
            if domain in [sympy.ZZ, sympy.QQ]:
                return True
            if hasattr(domain, 'is_domain') and domain.is_domain:
                return True
            if hasattr(domain, 'is_Field') and domain.is_Field:
                return True
            return False

        h1 = is_id(R) and is_id(S)

        def check_f(f_obj, R_obj):
            if isinstance(f_obj, str):
                return f_obj in ['id', 'identity']
            if isinstance(f_obj, dict):
                keys = list(f_obj.keys())
                for a in keys:
                    for b in keys:
                        if a+b in f_obj and f_obj[a+b] != f_obj[a] + f_obj[b]: return False
                        if a*b in f_obj and f_obj[a*b] != f_obj[a] * f_obj[b]: return False
                        if a != b and f_obj[a] == f_obj[b]: return False
                return True
            if callable(f_obj):
                sample = [-1, 0, 1, 2]
                for a in sample:
                    for b in sample:
                        try:
                            if f_obj(a+b) != f_obj(a) + f_obj(b): return False
                            if f_obj(a*b) != f_obj(a) * f_obj(b): return False
                            if a != b and f_obj(a) == f_obj(b): return False
                        except Exception:
                            pass
                return True
            return False

        h2 = check_f(f, R)

        def check_neg_q(K_obj, L_obj):
            K_str = str(K_obj)
            L_str = str(L_obj)
            
            # Existence fails
            if K_str in ['QQ', 'Q', 'FractionField(ZZ)'] and L_str in ['ZZ', 'Z']:
                return True
            if K_str in ['CC', 'C'] and L_str in ['RR', 'R', 'QQ', 'Q', 'ZZ', 'Z']:
                return True
            if K_str in ['RR', 'R'] and L_str in ['QQ', 'Q', 'ZZ', 'Z']:
                return True
                
            # Uniqueness fails
            if 'sqrt' in K_str and K_str == L_str:
                return True
            if 'I' in K_str and K_str == L_str:
                return True
            if K_str in ['ZZ[x]', 'Z[x]', 'QQ[x]', 'Q[x]'] and K_str == L_str:
                return True
                
            # If K is a field and L is not a field (and not same), existence usually fails
            if hasattr(K_obj, 'is_Field') and K_obj.is_Field:
                if hasattr(L_obj, 'is_Field') and not L_obj.is_Field:
                    return True
                    
            return False

        neg_q = check_neg_q(K, L)

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]