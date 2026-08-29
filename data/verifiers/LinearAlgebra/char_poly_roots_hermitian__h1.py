import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: Suppose A is Hermitian, meaning A = A*
    try:
        if hasattr(witness, 'H'):
            h1 = (witness == witness.H)
        elif hasattr(witness, 'conjugate') and hasattr(witness, 'transpose'):
            h1 = (witness == witness.conjugate().transpose())
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: Let p(x) be the characteristic polynomial of A
    try:
        p = witness.charpoly()
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: All roots of p(x) are real numbers
    # We want this to FAIL at the witness, so we return True if NOT all roots are real numbers.
    neg_q = False
    try:
        if h2:
            n = witness.shape[0]
            try:
                eigenvalues = witness.eigenvals()
                for val in eigenvalues:
                    # A root is not a real number if it's not a numeric value (e.g. a symbol)
                    if not val.is_number:
                        neg_q = True
                        break
                    # Or if it is explicitly not real
                    if val.is_real is False:
                        neg_q = True
                        break
                    # Or if SymPy cannot trivially determine it is real, check its imaginary part
                    if val.is_real is None:
                        im = sp.im(val).simplify()
                        if not im.is_zero:
                            neg_q = True
                            break
                found_all = (sum(eigenvalues.values()) == n)
            except Exception:
                found_all = False

            # If eigenvals didn't find all roots and we haven't found a non-real one yet, fallback to all_roots
            if not neg_q and not found_all:
                roots = witness.charpoly().all_roots()
                for r in roots:
                    if not r.is_number:
                        neg_q = True
                        break
                    if r.is_real is False:
                        neg_q = True
                        break
                    if r.is_real is None:
                        im = sp.im(r).simplify()
                        if not im.is_zero:
                            neg_q = True
                            break
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is Hermitian, meaning A = A*",
    "H_2: p(x) is the characteristic polynomial of A",
    "¬Q: Not all roots of p(x) are real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2