import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_transitive_on(G, Omega):
    try:
        if not Omega:
            return False
        Omega_set = set(Omega)
        x_val = list(Omega_set)[0]
        orbit_x = {x_val}
        queue = [x_val]
        while queue:
            curr = queue.pop(0)
            for g in G.generators:
                nxt = g(curr)
                if nxt not in orbit_x:
                    orbit_x.add(nxt)
                    queue.append(nxt)
        return orbit_x == Omega_set
    except Exception:
        return False

def safe_stabilizer(G, pt):
    if pt >= G.degree:
        return G
    return G.stabilizer(pt)

def are_conjugate_subgroups(G, H, K):
    try:
        if H.order() != K.order():
            return False
        for g in G.generate():
            is_conj = True
            for h in H.generators:
                conj = g * h * (~g)
                if conj not in K:
                    is_conj = False
                    break
            if is_conj:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            Omega = witness.get('Omega')
            alpha = witness.get('alpha')
            beta = witness.get('beta')
        else:
            G, Omega, alpha, beta = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a permutation group acting transitively on Omega
    try:
        h1 = isinstance(G, PermutationGroup) and is_transitive_on(G, Omega)
    except Exception:
        h1 = False
        
    # H_2: alpha and beta are valid points (non-negative integers)
    try:
        h2 = (isinstance(alpha, (int, sympy.Integer)) and 
              isinstance(beta, (int, sympy.Integer)) and 
              alpha >= 0 and beta >= 0)
    except Exception:
        h2 = False
        
    # ¬Q: G_alpha and G_beta are NOT conjugate subgroups in G
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            G_alpha = safe_stabilizer(G, alpha)
            G_beta = safe_stabilizer(G, beta)
            neg_q = not are_conjugate_subgroups(G, G_alpha, G_beta)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group acting transitively on Omega",
    "H_2: alpha and beta are valid points",
    "¬Q: G_alpha and G_beta are not conjugate subgroups in G"
]

N_HYP = 2
NEG_Q_INDEX = 2