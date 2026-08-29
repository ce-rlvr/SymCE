import sympy as sp
from sympy import Symbol, oo
import math
import itertools
import functools

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Wrap single random variable or dict into a list to treat as a family of size 1
        if hasattr(witness, 'pspace') or (isinstance(witness, dict) and 'support' in witness):
            witness = [witness]

        # Format 4: Infinite family represented by (pdf_expr, x_sym, n_sym, a, b)
        if isinstance(witness, tuple) and len(witness) == 5 and isinstance(witness[1], sp.Symbol) and isinstance(witness[2], sp.Symbol):
            pdf, x, n, a, b = witness
            h1 = True
            if a == -oo or b == oo:
                h2 = False
            else:
                a_sym = sp.sympify(a)
                b_sym = sp.sympify(b)
                if n in a_sym.free_symbols or n in b_sym.free_symbols:
                    h2 = False
                else:
                    h2 = True
            
            if h2:
                neg_q = False
            else:
                neg_q = True
                
        # Format 1: list of tuples (pdf, a, b)
        elif isinstance(witness, (list, tuple)) and len(witness) > 0 and all(isinstance(w, (list, tuple)) and len(w) == 3 for w in witness):
            h1 = True
            is_bounded = True
            for w in witness:
                _, a, b = w
                if a == -oo or b == oo:
                    is_bounded = False
                    break
                try:
                    float(abs(a))
                    float(abs(b))
                except Exception:
                    is_bounded = False
                    break
            if is_bounded:
                h2 = True
            neg_q = False

        # Format 2: list of dicts
        elif isinstance(witness, (list, tuple)) and len(witness) > 0 and all(isinstance(w, dict) and 'support' in w for w in witness):
            h1 = True
            is_bounded = True
            for w in witness:
                a, b = w['support']
                if a == -oo or b == oo:
                    is_bounded = False
                    break
                try:
                    float(abs(a))
                    float(abs(b))
                except Exception:
                    is_bounded = False
                    break
            if is_bounded:
                h2 = True
            neg_q = False

        # Format 3: list of sympy.stats RVs
        elif isinstance(witness, (list, tuple)) and len(witness) > 0 and all(hasattr(w, 'pspace') for w in witness):
            h1 = True
            is_bounded = True
            try:
                from sympy.stats import density
                for w in witness:
                    try:
                        d = density(w)
                        if hasattr(d, 'domain') and hasattr(d.domain, 'set'):
                            s = d.domain.set
                            if s.inf == -oo or s.sup == oo:
                                is_bounded = False
                                break
                        elif hasattr(d, 'dict'):
                            pass
                        else:
                            is_bounded = False
                            break
                    except Exception:
                        is_bounded = False
                        break
                if is_bounded:
                    h2 = True
            except Exception:
                pass
            neg_q = False

        # Format 5: list of sympy expressions (e.g., characteristic functions)
        elif isinstance(witness, (list, tuple)) and len(witness) > 0 and all(isinstance(w, sp.Expr) for w in witness):
            h1 = True
            h2 = False
            neg_q = False

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: \\mathcal{X} is a family of real-valued random variables",
    "H_2: There exists a constant M > 0 such that for all X \\in \\mathcal{X}, \\mathbb{P}(|X| \\le M) = 1",
    "¬Q: The family of functions \\Phi is not uniformly equicontinuous on \\mathbb{R}"
]

N_HYP = 2
NEG_Q_INDEX = 2