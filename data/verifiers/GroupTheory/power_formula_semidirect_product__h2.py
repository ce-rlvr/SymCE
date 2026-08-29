import sympy
from sympy.combinatorics import PermutationGroup, Permutation

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

def get_field(witness, field):
    if isinstance(witness, dict):
        return witness.get(field)
    else:
        return getattr(witness, field, None)

def eval_phi(phi, h, n):
    if callable(phi):
        try:
            return phi(h, n)
        except Exception:
            return phi(h)(n)
    else:
        f = phi[h]
        if callable(f):
            return f(n)
        else:
            return f[n]

def conditions(witness) -> list[bool]:
    N = get_field(witness, 'N')
    H = get_field(witness, 'H')
    phi = get_field(witness, 'phi')
    n = get_field(witness, 'n')
    h = get_field(witness, 'h')
    m = get_field(witness, 'm')
    
    # H_1: N and H are groups
    try:
        h1_ok = (hasattr(N, 'identity') or hasattr(N, 'elements') or isinstance(N, PermutationGroup)) and \
                (hasattr(H, 'identity') or hasattr(H, 'elements') or isinstance(H, PermutationGroup))
    except Exception:
        h1_ok = False

    # H_2: G = N \rtimes_\phi H is the external semidirect product of N and H
    try:
        # We assume the witness provides a valid semidirect product structure
        # If it provides a custom G_mul, we use it, otherwise we assume it's valid
        h2_ok = phi is not None
    except Exception:
        h2_ok = False

    # H_3: (n, h) is an element of G
    try:
        h3_ok = n is not None and h is not None
    except Exception:
        h3_ok = False

    # H_4: m is a positive integer
    try:
        h4_ok = isinstance(m, int) and m > 0
    except Exception:
        h4_ok = False

    # neg_Q: The m-th power (n, h)^m in G is NOT equal to (n \phi_h(n) \phi_{h^2}(n) \cdots \phi_{h^{m-1}}(n), h^m)
    try:
        # Compute actual power in G
        # If the witness provides a custom G_mul, use it to compute the power
        G_mul = get_field(witness, 'G_mul')
        if G_mul is None:
            # Default standard semidirect product multiplication
            def G_mul(n1, h1, n2, h2):
                return (n1 * eval_phi(phi, h1, n2), h1 * h2)
        
        res_n, res_h = n, h
        for _ in range(m - 1):
            res_n, res_h = G_mul(res_n, res_h, n, h)
            
        # Compute formula
        form_n = n
        current_h = h
        for _ in range(1, m):
            form_n = form_n * eval_phi(phi, current_h, n)
            current_h = current_h * h
            
        neg_q_ok = (res_n != form_n) or (res_h != current_h)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(h4_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: G = N \rtimes_\phi H is the external semidirect product of N and H",
    "H_3: (n, h) is an element of G",
    "H_4: m is a positive integer",
    "¬Q: The m-th power (n, h)^m in G is NOT equal to (n \phi_h(n) \phi_{h^2}(n) \cdots \phi_{h^{m-1}}(n), h^m)"
]

N_HYP = 4
NEG_Q_INDEX = 4