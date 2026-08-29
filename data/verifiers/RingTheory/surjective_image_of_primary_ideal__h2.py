import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings for finite rings Z/mZ
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12
Z16 = 16

def extract_mnQ(witness):
    """
    Extracts the moduli m, n and the subset Q from the witness.
    Supports dictionary and tuple formats.
    """
    m, n, Q = None, None, None
    if isinstance(witness, dict):
        m = witness.get('R', witness.get('m'))
        n = witness.get('S', witness.get('n'))
        Q = witness.get('Q')
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            m, n, Q = witness
        elif len(witness) == 4:
            m, n, _, Q = witness
            
    if hasattr(m, 'n'): m = m.n
    if hasattr(n, 'n'): n = n.n
    
    if isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0 and Q is not None:
        try:
            Q_set = set()
            for q in Q:
                if hasattr(q, 'n'):
                    Q_set.add(int(q.n) % m)
                else:
                    Q_set.add(int(q) % m)
            return m, n, Q_set
        except Exception:
            pass
    return None, None, None

def get_f(witness, m, n):
    """
    Extracts the homomorphism f from the witness, defaulting to modulo n projection.
    """
    if isinstance(witness, dict) and 'f' in witness:
        f_val = witness['f']
        return lambda x: f_val(x) if callable(f_val) else f_val[x]
    elif isinstance(witness, tuple) and len(witness) == 4:
        f_val = witness[2]
        return lambda x: f_val(x) if callable(f_val) else f_val[x]
    else:
        return lambda x: x % n

def is_primary_ideal(I, m):
    """
    Checks if a subset I is a primary ideal in the ring Z/mZ.
    """
    I = set(x % m for x in I)
    if not I:
        return False
        
    # Check if I is an ideal
    for a in I:
        for b in I:
            if (a + b) % m not in I:
                return False
    for a in I:
        for r in range(m):
            if (a * r) % m not in I:
                return False
                
    # Check if I is primary
    if len(I) == m:
        return False  # Primary ideal must be a proper ideal
    
    for a in range(m):
        for b in range(m):
            if (a * b) % m in I:
                if a in I:
                    continue
                # check if b^k in I for some k > 0
                b_k = b % m
                found = False
                for _ in range(m):
                    if b_k in I:
                        found = True
                        break
                    b_k = (b_k * b) % m
                if not found:
                    return False
    return True

def conditions(witness) -> list[bool]:
    m, n, Q = extract_mnQ(witness)
    if m is None or n is None or Q is None:
        return [False, False, False]
    
    f = get_f(witness, m, n)
    
    # H1: f is a surjective homomorphism of commutative rings
    try:
        mapped = set()
        h1_ok = True
        for x in range(m):
            fx = f(x)
            if not (isinstance(fx, int) and 0 <= fx < n):
                h1_ok = False
                break
            mapped.add(fx)
            
        if h1_ok:
            if len(mapped) != n:
                h1_ok = False
            elif f(1) != 1 % n:
                h1_ok = False
            else:
                for x in range(m):
                    for y in range(m):
                        if f((x + y) % m) != (f(x) + f(y)) % n:
                            h1_ok = False
                            break
                        if f((x * y) % m) != (f(x) * f(y)) % n:
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
    except Exception:
        h1_ok = False

    # H2: The kernel of f is contained in Q
    try:
        ker = set()
        for x in range(m):
            if f(x) == 0:
                ker.add(x)
        h2_ok = ker.issubset(Q)
    except Exception:
        h2_ok = False

    # Negated Conclusion: Q is a primary ideal in R iff f(Q) is a primary ideal in S
    try:
        q_is_primary = is_primary_ideal(Q, m)
        f_Q = set(f(x) for x in Q)
        fq_is_primary = is_primary_ideal(f_Q, n)
        # The conclusion fails if exactly one of them is a primary ideal
        neg_q_ok = (q_is_primary != fq_is_primary)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a surjective homomorphism of commutative rings",
    "H_2: The kernel of f is contained in Q",
    "¬Q: Exactly one of Q or f(Q) is a primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2