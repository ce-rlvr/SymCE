import sympy as sp
from sympy import Symbol, solveset, S, limit, oo

# Top-level setup for potential witness expressions
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: f in C(X, R)",
    "¬Q: f(x) != 0 for all x in X, but f is not a unit in C(X, R)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "f is a unit in C(X, R) if and only if f(x) != 0 for all x in X"
    
    The dropped hypothesis from the true theorem is that X is compact.
    Without compactness, C(X, R) (often denoting the ring of bounded continuous functions)
    can contain a function f that never vanishes, but whose inverse 1/f is unbounded,
    meaning 1/f is not in C(X, R) and thus f is not a unit.
    """
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 2:
            domain, f = witness
        elif hasattr(witness, 'domain') and hasattr(witness, 'f'):
            domain = witness.domain
            f = witness.f
        else:
            domain = S.Reals
            f = witness

        if not isinstance(f, sp.Basic):
            f = sp.sympify(f)
            
        if not isinstance(domain, sp.Set):
            try:
                domain = sp.sympify(domain)
            except Exception:
                pass
            if not isinstance(domain, sp.Set):
                return [False, False, False]
            
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
        elif len(free_syms) == 0:
            sym = Symbol('x', real=True)
        else:
            return [True, False, False]

        # H_1: X is a topological space
        # Any valid sympy Set represents a topological space (subspace of R)
        h1 = True

        # H_2: f in C(X, R)
        # In this context, f must be continuous and bounded on the domain
        try:
            sings = sp.calculus.singularities(f, sym)
            continuous = sings.intersect(domain) == S.EmptySet
        except Exception:
            continuous = False

        try:
            if domain == S.Reals:
                l1 = limit(f, sym, oo)
                l2 = limit(f, sym, -oo)
                bounded = l1.is_finite and l2.is_finite
            elif isinstance(domain, sp.Interval):
                if domain.start == -oo:
                    l1 = limit(f, sym, -oo)
                else:
                    l1 = limit(f, sym, domain.start, dir='+')
                    
                if domain.end == oo:
                    l2 = limit(f, sym, oo)
                else:
                    l2 = limit(f, sym, domain.end, dir='-')
                bounded = l1.is_finite and l2.is_finite
            else:
                bounded = False
        except Exception:
            bounded = False

        h2 = continuous and bounded

        # ¬Q: f(x) != 0 for all x in X, but f is not a unit (i.e., 1/f is not bounded)
        try:
            zeros = solveset(f, sym, domain=domain)
            no_zeros = (zeros == S.EmptySet)
        except Exception:
            no_zeros = False

        try:
            inv_f = 1 / f
            if domain == S.Reals:
                l1 = limit(inv_f, sym, oo)
                l2 = limit(inv_f, sym, -oo)
                inv_bounded = l1.is_finite and l2.is_finite
            elif isinstance(domain, sp.Interval):
                if domain.start == -oo:
                    l1 = limit(inv_f, sym, -oo)
                else:
                    l1 = limit(inv_f, sym, domain.start, dir='+')
                    
                if domain.end == oo:
                    l2 = limit(inv_f, sym, oo)
                else:
                    l2 = limit(inv_f, sym, domain.end, dir='-')
                inv_bounded = l1.is_finite and l2.is_finite
            else:
                inv_bounded = False
        except Exception:
            inv_bounded = False

        neg_q = no_zeros and not inv_bounded

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]