import sympy
from sympy import QQ, ZZ, RR, CC
import sympy.abc

# Top-level setup for FieldTheory
x, y, z = sympy.abc.x, sympy.abc.y, sympy.abc.z

CONDITION_LABELS = [
    "H_1: K and L are algebraically closed",
    "H_2: F is a common subfield of K and L",
    "H_3: F is a perfect field",
    "¬Q: The tensor product K \\otimes_F L is not a reduced ring"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        K = L = F = tp = None
        if isinstance(witness, dict):
            K = witness.get('K')
            L = witness.get('L')
            F = witness.get('F')
            tp = witness.get('tensor_product')
        elif isinstance(witness, tuple):
            if len(witness) >= 3:
                K, L, F = witness[0], witness[1], witness[2]
            if len(witness) >= 4:
                tp = witness[3]
        else:
            K = getattr(witness, 'K', None)
            L = getattr(witness, 'L', None)
            F = getattr(witness, 'F', None)
            tp = getattr(witness, 'tensor_product', None)

        # H_1: K and L are algebraically closed
        def is_alg_closed(obj):
            if obj is None: return False
            if obj == CC: return True
            if isinstance(obj, dict):
                return bool(obj.get('is_algebraically_closed', obj.get('algebraically_closed', False)))
            for attr in ['is_algebraically_closed', 'algebraically_closed']:
                if hasattr(obj, attr):
                    v = getattr(obj, attr)
                    return bool(v() if callable(v) else v)
            return False
            
        h1 = is_alg_closed(K) and is_alg_closed(L)

        # H_2: F is a common subfield of K and L
        def is_subfield(sub, sup):
            if sub is None or sup is None: return False
            if sub == RR and sup == CC: return True
            if sub == QQ and sup in (RR, CC): return True
            if hasattr(sub, 'is_subfield_of'):
                return sub.is_subfield_of(sup)
            if hasattr(sup, 'has_subfield'):
                return sup.has_subfield(sub)
            if isinstance(sub, dict) and 'subfield_of' in sub:
                return sup in sub['subfield_of'] or sup == sub['subfield_of']
            return False

        if isinstance(witness, dict) and 'F_is_common_subfield' in witness:
            h2 = bool(witness['F_is_common_subfield'])
        elif hasattr(witness, 'F_is_common_subfield'):
            v = witness.F_is_common_subfield
            h2 = bool(v() if callable(v) else v)
        elif F is not None and K is not None and L is not None:
            h2 = is_subfield(F, K) and is_subfield(F, L)

        # H_3: F is a perfect field
        def is_perf(obj):
            if obj is None: return False
            if obj in (QQ, RR, CC): return True
            if hasattr(obj, 'is_FiniteField') and obj.is_FiniteField: return True
            if isinstance(obj, dict):
                return bool(obj.get('is_perfect', obj.get('perfect', False)))
            for attr in ['is_perfect', 'perfect']:
                if hasattr(obj, attr):
                    v = getattr(obj, attr)
                    return bool(v() if callable(v) else v)
            return False

        if F is not None:
            h3 = is_perf(F)
        else:
            if isinstance(witness, dict) and 'F_is_perfect' in witness:
                h3 = bool(witness['F_is_perfect'])
            elif hasattr(witness, 'F_is_perfect'):
                v = witness.F_is_perfect
                h3 = bool(v() if callable(v) else v)

        # ¬Q: The tensor product K \otimes_F L is not a reduced ring
        def is_red(obj):
            if obj is None: return None
            if isinstance(obj, dict):
                if 'is_reduced' in obj: return bool(obj['is_reduced'])
                if 'reduced' in obj: return bool(obj['reduced'])
                return None
            for attr in ['is_reduced', 'reduced']:
                if hasattr(obj, attr):
                    v = getattr(obj, attr)
                    return bool(v() if callable(v) else v)
            return None

        if tp is not None:
            res = is_red(tp)
            if res is not None:
                neg_q = not res
        
        if not neg_q:
            if isinstance(witness, dict):
                if 'tensor_product_is_reduced' in witness:
                    neg_q = not bool(witness['tensor_product_is_reduced'])
                elif 'is_reduced' in witness:
                    neg_q = not bool(witness['is_reduced'])
            else:
                if hasattr(witness, 'tensor_product_is_reduced'):
                    v = witness.tensor_product_is_reduced
                    neg_q = not bool(v() if callable(v) else v)
                elif hasattr(witness, 'is_reduced'):
                    v = witness.is_reduced
                    neg_q = not bool(v() if callable(v) else v)

    except Exception:
        pass

    return [h1, h2, h3, neg_q]