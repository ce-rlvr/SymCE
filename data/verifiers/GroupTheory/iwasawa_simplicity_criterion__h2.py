import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup: named object bindings
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

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            return witness[0], witness[1], witness[2]
        elif len(witness) == 2:
            return witness[0], 0, witness[1]
    return witness, 0, None

def get_identity(G):
    if hasattr(G, 'identity'):
        return G.identity
    gens = list(G.generators)
    if gens:
        return gens[0] * ~gens[0]
    return Permutation()

def normal_closure(G, gens):
    if not gens:
        return PermutationGroup([get_identity(G)])
    closure_gens = list(gens)
    H = PermutationGroup(closure_gens)
    G_gens = list(G.generators)
    
    queue = list(gens)
    while queue:
        h = queue.pop(0)
        for g in G_gens:
            conj = g * h * ~g
            if not H.contains(conj):
                closure_gens.append(conj)
                H = PermutationGroup(closure_gens)
                queue.append(conj)
            
            conj_inv = (~g) * h * g
            if not H.contains(conj_inv):
                closure_gens.append(conj_inv)
                H = PermutationGroup(closure_gens)
                queue.append(conj_inv)
    return H

def check_H3(G, x, A):
    if A is None:
        return True
    Gx = G.stabilizer(x)
    for gen in A.generators:
        if not Gx.contains(gen):
            return False
    if not A.is_abelian:
        return False
    for g in Gx.generators:
        for a in A.generators:
            if not A.contains(g * a * ~g):
                return False
            if not A.contains((~g) * a * g):
                return False
    return True

def check_H4(G, A):
    if A is None:
        return False
    N = normal_closure(G, A.generators)
    return N.order() == G.order()

def find_valid_A(G):
    x = 0
    try:
        Gx = G.stabilizer(x)
    except Exception:
        return None
    
    try:
        Z = Gx.center()
        if Z.order() > 1:
            if normal_closure(G, Z.generators).order() == G.order():
                return Z
    except Exception:
        pass
            
    try:
        if Gx.order() > 5000:
            return None
    except Exception:
        return None
        
    N_gs = []
    try:
        for g in Gx.generate():
            if getattr(g, 'is_Identity', False):
                continue
            N = normal_closure(Gx, [g])
            if N.is_abelian:
                is_new = True
                for M in N_gs:
                    if N.order() == M.order():
                        if all(M.contains(gen) for gen in N.generators):
                            is_new = False
                            break
                if is_new:
                    N_gs.append(N)
    except Exception:
        pass
                
    try:
        for r in range(1, len(N_gs) + 1):
            for combo in itertools.combinations(N_gs, r):
                gens = []
                for N in combo:
                    gens.extend(N.generators)
                if not gens:
                    continue
                A = PermutationGroup(gens)
                if A.is_abelian:
                    if normal_closure(G, A.generators).order() == G.order():
                        return A
    except Exception:
        pass
        
    return None

def is_simple_group(G):
    try:
        order = G.order()
    except Exception:
        return True
        
    if order == 1:
        return False
    if order in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        return True
        
    try:
        D = G.derived_subgroup()
        if 1 < D.order() < order:
            return False
    except Exception:
        pass
        
    try:
        strong_gens = getattr(G, 'strong_gens', [])
        for g in strong_gens:
            if getattr(g, 'is_Identity', False):
                continue
            N = normal_closure(G, [g])
            if 1 < N.order() < order:
                return False
    except Exception:
        pass
            
    try:
        gens = list(G.generators)
        for i in range(len(gens)):
            for j in range(i+1, len(gens)):
                g = gens[i] * gens[j] * (~gens[i]) * (~gens[j])
                if not getattr(g, 'is_Identity', False):
                    N = normal_closure(G, [g])
                    if 1 < N.order() < order:
                        return False
    except Exception:
        pass
                    
    try:
        count = 0
        for g in G.generate():
            if getattr(g, 'is_Identity', False):
                continue
            N = normal_closure(G, [g])
            if 1 < N.order() < order:
                return False
            count += 1
            if count > 500:
                break
    except Exception:
        pass
        
    return True

def conditions(witness):
    G, x, A = parse_witness(witness)
    
    try:
        h1 = bool(G.derived_subgroup().order() == G.order())
    except Exception:
        h1 = False
        
    try:
        h2 = bool(G.is_primitive())
    except Exception:
        h2 = False
        
    try:
        if A is not None:
            h3 = bool(check_H3(G, x, A))
            h4 = bool(check_H4(G, A))
        else:
            found_A = find_valid_A(G)
            if found_A is not None:
                h3 = True
                h4 = True
            else:
                h3 = True
                h4 = False
    except Exception:
        h3 = False
        h4 = False
        
    try:
        neg_q = not is_simple_group(G)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a perfect group",
    "H_2: G acts faithfully and primitively on X",
    "H_3: There exists an element x in X such that the stabilizer G_x contains an abelian normal subgroup A of G_x",
    "H_4: The conjugates of A in G generate the group G",
    "¬Q: G is not a simple group"
]

N_HYP = 4
NEG_Q_INDEX = 4