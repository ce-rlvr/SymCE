import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    return list(G)

def apply_mult(mult, x, y):
    if callable(mult):
        return mult(x, y)
    try:
        return mult[x][y]
    except (TypeError, KeyError):
        return mult[(x, y)]

def apply_map(f, x):
    if callable(f):
        return f(x)
    return f[x]

def apply_phi(phi, h, n):
    if callable(phi):
        try:
            return phi(h, n)
        except TypeError:
            return phi(h)(n)
    try:
        return phi[h][n]
    except (TypeError, KeyError):
        return phi[(h, n)]

def get_components(witness):
    if isinstance(witness, dict):
        N = get_elements(witness['N'])
        H = get_elements(witness['H'])
        N_mult = witness.get('N_mult', lambda x, y: x * y)
        H_mult = witness.get('H_mult', lambda x, y: x * y)
        phi = witness['phi']
        alpha = witness['alpha']
        beta = witness['beta']
        return N, H, N_mult, H_mult, phi, alpha, beta
    elif isinstance(witness, (tuple, list)):
        N = get_elements(witness[0])
        H = get_elements(witness[1])
        N_mult = witness[2]
        H_mult = witness[3]
        phi = witness[4]
        alpha = witness[5]
        beta = witness[6]
        return N, H, N_mult, H_mult, phi, alpha, beta
    else:
        N = get_elements(witness.N)
        H = get_elements(witness.H)
        N_mult = getattr(witness, 'N_mult', lambda x, y: x * y)
        H_mult = getattr(witness, 'H_mult', lambda x, y: x * y)
        phi = witness.phi
        alpha = witness.alpha
        beta = witness.beta
        return N, H, N_mult, H_mult, phi, alpha, beta

def has_duplicates(lst):
    for i, x in enumerate(lst):
        if x in lst[:i]:
            return True
    return False

def is_group(elements, mult):
    elements = list(elements)
    n = len(elements)
    if n == 0:
        return False
        
    # check closure
    for a in elements:
        for b in elements:
            try:
                c = apply_mult(mult, a, b)
                if c not in elements:
                    return False
            except Exception:
                return False
                
    # check associativity
    for a in elements:
        for b in elements:
            for c in elements:
                try:
                    if apply_mult(mult, apply_mult(mult, a, b), c) != apply_mult(mult, a, apply_mult(mult, b, c)):
                        return False
                except Exception:
                    return False
                    
    # check identity
    identity = None
    for e in elements:
        is_id = True
        for a in elements:
            try:
                if apply_mult(mult, e, a) != a or apply_mult(mult, a, e) != a:
                    is_id = False
                    break
            except Exception:
                is_id = False
                break
        if is_id:
            identity = e
            break
    if identity is None:
        return False
        
    # check inverses
    for a in elements:
        has_inv = False
        for b in elements:
            try:
                if apply_mult(mult, a, b) == identity and apply_mult(mult, b, a) == identity:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv:
            return False
            
    return True

def conditions(witness):
    try:
        N, H, N_mult, H_mult, phi, alpha, beta = get_components(witness)
    except Exception:
        return [False, False, False, False]
        
    def check_H1():
        if not is_group(N, N_mult): return False
        mapped = []
        for n in N:
            m = apply_map(alpha, n)
            if m not in N: return False
            mapped.append(m)
        if has_duplicates(mapped): return False
        for n1 in N:
            for n2 in N:
                if apply_map(alpha, apply_mult(N_mult, n1, n2)) != apply_mult(N_mult, apply_map(alpha, n1), apply_map(alpha, n2)):
                    return False
        return True

    def check_H2():
        if not is_group(H, H_mult): return False
        mapped = []
        for h in H:
            m = apply_map(beta, h)
            if m not in H: return False
            mapped.append(m)
        if has_duplicates(mapped): return False
        for h1 in H:
            for h2 in H:
                if apply_map(beta, apply_mult(H_mult, h1, h2)) != apply_mult(H_mult, apply_map(beta, h1), apply_map(beta, h2)):
                    return False
        return True

    def check_H3():
        for h in H:
            for n in N:
                left = apply_map(alpha, apply_phi(phi, h, n))
                right = apply_phi(phi, apply_map(beta, h), apply_map(alpha, n))
                if left != right:
                    return False
        return True

    def check_neg_Q():
        G = [(n, h) for n in N for h in H]
        def G_mult(x, y):
            n1, h1 = x
            n2, h2 = y
            return (apply_mult(N_mult, n1, apply_phi(phi, h1, n2)), apply_mult(H_mult, h1, h2))
            
        if not is_group(G, G_mult):
            return True
            
        def gamma(x):
            n, h = x
            return (apply_map(alpha, n), apply_map(beta, h))
            
        mapped = []
        for x in G:
            m = gamma(x)
            if m not in G: return True
            mapped.append(m)
        if has_duplicates(mapped): return True
        
        for x in G:
            for y in G:
                if gamma(G_mult(x, y)) != G_mult(gamma(x), gamma(y)):
                    return True
        return False

    try:
        h1 = check_H1()
    except Exception:
        h1 = False

    try:
        h2 = check_H2()
    except Exception:
        h2 = False

    try:
        h3 = check_H3()
    except Exception:
        h3 = False

    try:
        nq = check_neg_Q()
    except Exception:
        nq = False

    return [h1, h2, h3, nq]

CONDITION_LABELS = [
    "H_1: alpha is an automorphism of N",
    "H_2: beta is an automorphism of H",
    "H_3: compatibility condition holds for all h in H",
    "¬Q: gamma is not a group automorphism of G"
]

N_HYP = 3
NEG_Q_INDEX = 3