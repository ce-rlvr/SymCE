import sympy
from sympy import groebner, sympify, Expr
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness):
    # H1: I is a finitely generated ideal of R
    # We accept the witness as a finite collection of generators (expressions).
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and hasattr(witness[0], 'domain'):
            # Handle case where witness is (Ring, Ideal_gens)
            gens = witness[1]
        else:
            gens = witness
            
        if type(gens).__name__ == 'PolyIdeal':
            gens = gens.gens
            h1 = True
        elif isinstance(gens, (list, tuple, set)):
            gens = list(gens)
            h1 = all(isinstance(sympify(w), Expr) for w in gens)
        else:
            gens = []
            h1 = False
    except Exception:
        h1 = False
        gens = []

    # neg_Q: I is not a principal ideal of R
    # We check if the ideal requires more than one generator by computing its Groebner basis.
    try:
        if not h1:
            neg_q = False
        elif not gens:
            neg_q = False
        elif len(gens) == 1:
            neg_q = False
        else:
            symbols = set()
            for w in gens:
                w_sym = sympify(w)
                if hasattr(w_sym, 'free_symbols'):
                    symbols.update(w_sym.free_symbols)
            symbols = list(symbols)
            
            if not symbols:
                # If all generators are constants, the ideal is principal (e.g., in ZZ or QQ).
                neg_q = False
            else:
                # Try computing the Groebner basis over ZZ first to catch non-principal ideals in ZZ[x]
                try:
                    gb = groebner(gens, *symbols, domain='ZZ')
                except Exception:
                    # Fallback to QQ if ZZ fails or is unsupported for the given expressions
                    gb = groebner(gens, *symbols, domain='QQ')
                
                # If the reduced Groebner basis has more than 1 element, it is not a principal ideal.
                neg_q = len(gb) > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: I is a finitely generated ideal of R",
    "¬Q: I is not a principal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1