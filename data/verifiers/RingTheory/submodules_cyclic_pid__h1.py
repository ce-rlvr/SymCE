import sympy
from sympy import gcd, GroebnerBasis, eye, zeros
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_gcd(gens):
    if not gens:
        return sympy.S.Zero
    return functools.reduce(gcd, gens)

def in_ideal(f, gens, vars, domain):
    if not gens:
        return f == 0
    if not vars:
        from sympy import igcd
        g = functools.reduce(igcd, [int(c) for c in gens])
        return int(f) % g == 0
    
    try:
        gb = GroebnerBasis(gens, *vars, domain=domain)
        rem = gb.reduce(f)[1]
        return rem == 0
    except Exception:
        return False

def is_principal(gens, vars, domain):
    if not gens:
        return True
    if len(gens) == 1:
        return True
    g = get_gcd(gens)
    return in_ideal(g, gens, vars, domain)

def conditions(witness):
    """
    witness: A tuple (vars, M_gens, N_gens, domain) or a dict with these keys.
    Represents ideals in a polynomial ring or Z.
    - vars: tuple of SymPy symbols (e.g., (x, y)). Empty for Z.
    - M_gens: list of generators for the module M (ideal of R).
    - N_gens: list of generators for the submodule N (ideal of R).
    - domain: string, e.g., 'QQ' or 'ZZ'.
    """
    try:
        if isinstance(witness, dict):
            vars = witness.get('vars', [])
            M_gens = witness.get('M_gens', [])
            N_gens = witness.get('N_gens', [])
            domain = witness.get('domain', 'QQ')
        elif isinstance(witness, tuple):
            vars = witness[0]
            M_gens = witness[1]
            N_gens = witness[2]
            domain = witness[3] if len(witness) > 3 else 'QQ'
        else:
            return [False, False, False]
            
        if not isinstance(vars, (list, tuple)):
            vars = (vars,) if vars else ()
        if not isinstance(M_gens, (list, tuple)):
            M_gens = (M_gens,) if M_gens else ()
        if not isinstance(N_gens, (list, tuple)):
            N_gens = (N_gens,) if N_gens else ()
            
        # H1: M is a cyclic R-module
        try:
            h1 = bool(is_principal(M_gens, vars, domain))
        except Exception:
            h1 = False
            
        # H2: N is a submodule of M
        try:
            h2 = bool(all(in_ideal(f, M_gens, vars, domain) for f in N_gens))
        except Exception:
            h2 = False
            
        # neg_Q: N is NOT a cyclic R-module
        try:
            neg_q = not bool(is_principal(N_gens, vars, domain))
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is a cyclic R-module",
    "H_2: N is a submodule of M",
    "¬Q: N is not a cyclic R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2