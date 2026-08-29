import sympy
from sympy import roots, Poly, I, sqrt, simplify
from sympy.abc import x
from sympy.polys.domains import QQ

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        p = Poly(witness, x)
        if (p.domain.is_QQ or p.domain.is_ZZ) and not (p.free_symbols - {x}):
            if p.degree() > 0:
                h1_ok = True
    except Exception:
        h1_ok = False

    if h1_ok:
        try:
            f_roots_dict = roots(p, x)
            if sum(f_roots_dict.values()) != p.degree():
                neg_q_ok = True
            else:
                f_roots = list(f_roots_dict.keys())
                K_target = QQ.algebraic_field(I, sqrt(2))
                
                all_in_target = True
                for r in f_roots:
                    try:
                        K_target.from_sympy(simplify(r))
                    except Exception:
                        all_in_target = False
                        break
                
                if not all_in_target:
                    neg_q_ok = True
                else:
                    K_sub1 = QQ.algebraic_field(I)
                    K_sub2 = QQ.algebraic_field(sqrt(2))
                    K_sub3 = QQ.algebraic_field(I*sqrt(2))
                    
                    def all_in_sub(K_sub):
                        for r in f_roots:
                            try:
                                K_sub.from_sympy(simplify(r))
                            except Exception:
                                return False
                        return True
                    
                    if all_in_sub(K_sub1) or all_in_sub(K_sub2) or all_in_sub(K_sub3):
                        neg_q_ok = True
                    else:
                        neg_q_ok = False
        except Exception:
            neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is the splitting field of f(x) over Q",
    "not Q: K != Q(i, sqrt(2)) or degree of K over Q != 4"
]

N_HYP = 1
NEG_Q_INDEX = 1