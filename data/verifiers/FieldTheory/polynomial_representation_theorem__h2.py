import sympy
from sympy.ntheory import factorint

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        q = witness.get('q')
        f = witness.get('f')
    elif isinstance(witness, (list, tuple)) and len(witness) == 2:
        q, f = witness
    else:
        q, f = None, None

    try:
        if hasattr(q, '__int__') and int(q) == q:
            q_val = int(q)
            if 2 <= q_val <= 1000:
                factors = factorint(q_val)
                h1 = (len(factors) == 1)
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if not h1:
            conclusion_holds = False
        else:
            if isinstance(f, (list, tuple)):
                if len(f) != q_val:
                    raise ValueError()
                domain_elements = list(range(q_val))
                values = list(f)
            elif isinstance(f, dict):
                if len(f) != q_val:
                    raise ValueError()
                domain_elements = list(f.keys())
                values = list(f.values())
            elif callable(f):
                domain_elements = list(range(q_val))
                values = [f(a) for a in domain_elements]
            elif hasattr(f, 'subs') and hasattr(f, 'free_symbols'):
                domain_elements = list(range(q_val))
                if len(f.free_symbols) == 1:
                    x = list(f.free_symbols)[0]
                    values = [f.subs(x, a) for a in domain_elements]
                elif len(f.free_symbols) == 0:
                    values = [f for _ in domain_elements]
                else:
                    raise ValueError()
            else:
                raise ValueError()

            conclusion_holds = True
            for v in values:
                if v in domain_elements:
                    continue
                if any(v == de for de in domain_elements):
                    continue
                conclusion_holds = False
                break
                
    except Exception:
        conclusion_holds = False

    neg_q = not conclusion_holds

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "¬Q: There does not exist a unique polynomial P of degree less than q such that P(a) = f(a) for all a in F_q"
]

N_HYP = 1
NEG_Q_INDEX = 1