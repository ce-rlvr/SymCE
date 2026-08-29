import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.ntheory

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

def is_subgroup(H, G):
    for g in H.generators:
        if g not in G:
            return False
    return True

def normal_closure(G, elements):
    gens = list(elements)
    if not gens:
        return PermutationGroup([G.identity])
    subgroup = PermutationGroup(gens)
    changed = True
    while changed:
        changed = False
        for g in G.generators:
            for h in subgroup.generators:
                conj = g * h * ~g
                if conj not in subgroup:
                    gens.append(conj)
                    subgroup = PermutationGroup(gens)
                    changed = True
    return subgroup

def conjugacy_class(G, x):
    class_elements = {x}
    queue = [x]
    gens = list(G.generators)
    gens_inv = [~g for g in gens]
    while queue:
        curr = queue.pop(0)
        for g, g_inv in zip(gens, gens_inv):
            conj = g * curr * g_inv
            if conj not in class_elements:
                class_elements.add(conj)
                queue.append(conj)
    return class_elements

def is_semisimple(G):
    # A finite group is semisimple if it is perfect and G/Z(G) is a direct product of non-abelian simple groups.
    if G.order() == 1:
        return False
    
    if G.derived_subgroup().order() != G.order():
        return False
        
    Z = G.center()
    Z_els = set(Z.generate())
    
    P_list = []
    G_els = list(G.generate())
    covered = set(Z_els)
    
    for x in G_els:
        if x not in covered:
            N = normal_closure(G, [x])
            gens = list(N.generators) + list(Z.generators)
            if not gens:
                gens = [G.identity]
            NZ = PermutationGroup(gens)
            
            already = False
            for P in P_list:
                if P.order() == NZ.order() and is_subgroup(P, NZ):
                    already = True
                    break
            if not already:
                P_list.append(NZ)
                
            cclass = conjugacy_class(G, x)
            covered.update(cclass)
            
    minimals = []
    for P in P_list:
        is_min = True
        for Q in P_list:
            if Q.order() < P.order() and is_subgroup(Q, P):
                is_min = False
                break
        if is_min:
            already = any(M.order() == P.order() and is_subgroup(M, P) for M in minimals)
            if not already:
                minimals.append(P)
                
    for M in minimals:
        M_els = list(M.generate())
        covered_M = set(Z_els)
        for y in M_els:
            if y not in covered_M:
                N_y = normal_closure(M, [y])
                gens = list(N_y.generators) + list(Z.generators)
                if not gens:
                    gens = [G.identity]
                N_yZ = PermutationGroup(gens)
                if N_yZ.order() < M.order():
                    return False
                cclass = conjugacy_class(M, y)
                covered_M.update(cclass)
                
    all_min_gens = []
    for M in minimals:
        all_min_gens.extend(M.generators)
    if len(all_min_gens) == 0:
        return False
    gen_by_min = PermutationGroup(all_min_gens)
    if gen_by_min.order() != G.order():
        return False
        
    return True

def p_core(G, p):
    # The p-core O_p(G) is the intersection of all Sylow p-subgroups of G.
    if G.order() % p != 0:
        return PermutationGroup([G.identity])
    P = G.sylow_subgroup(p)
    core = P
    changed = True
    while changed:
        changed = False
        for g in G.generators:
            conj_gens = [g * h * ~g for h in core.generators]
            if not conj_gens:
                conj_gens = [G.identity]
            conj = PermutationGroup(conj_gens)
            try:
                new_core = core.intersection(conj)
            except AttributeError:
                try:
                    new_core = core.intersect(conj)
                except AttributeError:
                    els1 = set(core.generate())
                    els2 = set(conj.generate())
                    common = els1.intersection(els2)
                    new_core = PermutationGroup(list(common))
            if new_core.order() < core.order():
                core = new_core
                changed = True
    return core

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness can be a tuple (G, p) or just a group G.
    """
    if isinstance(witness, tuple):
        G, p = witness
    else:
        G = witness
        p = None

    # H_1: G is a semisimple finite group
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            h1 = is_semisimple(G)
    except Exception:
        h1 = False

    # neg_Q: The intersection of all Sylow p-subgroups of G is NOT the trivial subgroup
    try:
        if not isinstance(G, PermutationGroup):
            neg_q_ok = False
        elif p is not None:
            if not sympy.ntheory.isprime(p):
                neg_q_ok = False
            else:
                core = p_core(G, p)
                neg_q_ok = core.order() > 1
        else:
            primes = sympy.ntheory.primefactors(G.order())
            neg_q_ok = False
            for pr in primes:
                core = p_core(G, pr)
                if core.order() > 1:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "¬Q: The intersection of all Sylow p-subgroups of G is not the trivial subgroup"
]
N_HYP = 1
NEG_Q_INDEX = 1