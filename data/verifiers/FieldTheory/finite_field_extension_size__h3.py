import sympy
from sympy.ntheory import factorint
from sympy import oo

# Top-level setup
# No specific named bindings required for Field Theory sizes, 
# but we provide oo for infinite field extensions.

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    Expected witness format: tuple (q, size_K, n) or dict with these keys.
    size_K can be an integer or sympy.oo for infinite extensions.
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            size_K = witness.get('size_K', witness.get('K'))
            n = witness.get('n')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            q, size_K, n = witness
        else:
            return [False, False, False]

        # Extract order if SymPy Galois Field objects were passed
        if hasattr(q, 'order'):
            q = q.order
        if hasattr(size_K, 'order'):
            size_K = size_K.order

        # H1: F is a finite field containing exactly q elements
        try:
            q_val = int(q)
            # A finite field of size q exists iff q is a prime power
            h1 = (q_val >= 2) and (len(factorint(q_val)) == 1)
        except Exception:
            h1 = False

        # H2: K is a field extension of F
        try:
            if size_K == oo or str(size_K) == 'oo':
                h2 = True
            else:
                size_K_val = int(size_K)
                q_val = int(q)
                if size_K_val < q_val:
                    h2 = False
                else:
                    # K is a finite extension of F iff its size is a power of q
                    temp = 1
                    while temp < size_K_val:
                        temp *= q_val
                    h2 = (temp == size_K_val)
        except Exception:
            h2 = False

        # neg_Q: K is NOT a finite field containing exactly q^n elements
        try:
            if size_K == oo or str(size_K) == 'oo':
                neg_q = True
            else:
                size_K_val = int(size_K)
                q_val = int(q)
                n_val = int(n)
                neg_q = (size_K_val != q_val ** n_val)
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a finite field containing exactly q elements",
    "H_2: K is a field extension of F",
    "¬Q: K is not a finite field containing exactly q^n elements"
]

N_HYP = 2
NEG_Q_INDEX = 2