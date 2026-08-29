import math

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard finite commutative rings Z_n for n up to 12.
class Z_n:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
    def __iter__(self):
        return iter(self.elements)
    def __len__(self):
        return self.n
    def __repr__(self):
        return f"Z_{self.n}"

Z2 = Z_n(2)
Z3 = Z_n(3)
Z4 = Z_n(4)
Z5 = Z_n(5)
Z6 = Z_n(6)
Z8 = Z_n(8)
Z9 = Z_n(9)
Z10 = Z_n(10)
Z12 = Z_n(12)

def get_ring_size(R):
    if hasattr(R, 'n'): return R.n
    if isinstance(R, int): return R
    if hasattr(R, '__len__'): return len(R)
    return None

def extract(witness):
    if isinstance(witness, dict):
        R = witness.get('R', witness.get('n'))
        S = witness.get('S', witness.get('m'))
        f = witness.get('f')
        I = witness.get('I')
        J = witness.get('J')
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 5:
            R, S = witness[0], witness[1]
            last_three = witness[2:]
            f_idx = -1
            for i, x in enumerate(last_three):
                if callable(x) or isinstance(x, dict):
                    f_idx = i
                    break
            if f_idx == -1:
                f = witness[2]
                I = witness[3]
                J = witness[4]
            else:
                f = last_three[f_idx]
                others = [x for i, x in enumerate(last_three) if i != f_idx]
                I = others[0]
                J = others[1]
        else:
            raise ValueError("Tuple must have exactly 5 elements")
    else:
        R = getattr(witness, 'R', getattr(witness, 'n', None))
        S = getattr(witness, 'S', getattr(witness, 'm', None))
        f = getattr(witness, 'f', None)
        I = getattr(witness, 'I', None)
        J = getattr(witness, 'J', None)
        
    n = get_ring_size(R)
    m = get_ring_size(S)
    return n, m, f, I, J

def generate_ideal(X, k):
    if not X:
        return {0}
    g = k
    for x in X:
        g = math.gcd(g, int(x) % k)
    return set(i for i in range(k) if i % g == 0)

def is_ideal(I, n):
    try:
        if hasattr(I, 'elements'):
            I_set = set(I.elements)
        else:
            I_set = set(I)
        if not I_set: 
            return False
        if not all(isinstance(x, int) and 0 <= x < n for x in I_set): 
            return False
        return I_set == generate_ideal(I_set, n)
    except Exception:
        return False

def eval_f(f, x):
    if isinstance(f, dict):
        return f[x]
    elif isinstance(f, (list, tuple)):
        if len(f) > 0 and isinstance(f[0], (list, tuple)) and len(f[0]) == 2:
            for k, v in f:
                if k == x: return v
            raise ValueError(f"Mapping for {x} not found")
        return f[x]
    else:
        return f(x)

def conditions(witness) -> list[bool]:
    try:
        n, m, f, I, J = extract(witness)
    except Exception:
        return [False] * 5

    # H_1: R is a commutative ring
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    # H_2: S is a commutative ring
    try:
        h2 = isinstance(m, int) and m >= 1
    except Exception:
        h2 = False

    # H_3: I is an ideal of R
    try:
        h3 = h1 and is_ideal(I, n)
    except Exception:
        h3 = False

    # H_4: J is an ideal of R
    try:
        h4 = h1 and is_ideal(J, n)
    except Exception:
        h4 = False

    # ¬Q: (IJ)^e != I^e J^e
    try:
        if not (h1 and h2 and h3 and h4):
            neg_q = False
        else:
            I_set = set(I.elements) if hasattr(I, 'elements') else set(I)
            J_set = set(J.elements) if hasattr(J, 'elements') else set(J)
            
            # Compute IJ in R
            IJ_gens = [(x * y) % n for x in I_set for y in J_set]
            IJ = generate_ideal(IJ_gens, n)
            
            # Compute images under f
            f_I = [eval_f(f, x) % m for x in I_set]
            f_J = [eval_f(f, x) % m for x in J_set]
            f_IJ = [eval_f(f, x) % m for x in IJ]
            
            # Compute extensions in S
            I_e = generate_ideal(f_I, m)
            J_e = generate_ideal(f_J, m)
            IJ_e = generate_ideal(f_IJ, m)
            
            # Compute I^e J^e in S
            I_e_J_e_gens = [(x * y) % m for x in I_e for y in J_e]
            I_e_J_e = generate_ideal(I_e_J_e_gens, m)
            
            neg_q = (IJ_e != I_e_J_e)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a commutative ring",
    "H_3: I is an ideal of R",
    "H_4: J is an ideal of R",
    "¬Q: (IJ)^e != I^e J^e"
]

N_HYP = 4
NEG_Q_INDEX = 4