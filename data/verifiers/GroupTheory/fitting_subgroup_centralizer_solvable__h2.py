import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def intersect_groups(H, K):
    if H.order() > K.order():
        H, K = K, H
    common = [g for g in H.elements if g in K]
    return PermutationGroup(common)

def normal_core(H, G):
    core = H
    while True:
        prev_order = core.order()
        for g in G.generators:
            conj_gens = [g**-1 * c * g for c in core.generators]
            conj_group = PermutationGroup(conj_gens)
            core = intersect_groups(core, conj_group)
            if core.order() == 1:
                return core
        if core.order() == prev_order:
            break
    return core

def fitting_subgroup(G):
    order = G.order()
    primes = factorint(order).keys()
    
    F_gens = []
    for p in primes:
        sylow = G.sylow_subgroup(p)
        core = normal_core(sylow, G)
        F_gens.extend(core.generators)
        
    if not F_gens:
        id_elem = list(G.elements)[0]**0
        return PermutationGroup([id_elem])
    return PermutationGroup(F_gens)

def conditions(witness):
    # H_1: G is a finite solvable group
    try:
        if not isinstance(witness, PermutationGroup):
            h1 = False
        else:
            h1 = bool(witness.is_solvable)
    except Exception:
        h1 = False

    # ¬Q: The centralizer of F(G) in G is NOT a subgroup of F(G)
    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            F = fitting_subgroup(witness)
            F_gens = F.generators
            if not F_gens:
                F_gens = [list(witness.elements)[0]**0]
                
            neg_q = False
            # Check if there is any element in G that centralizes F(G) but is not in F(G)
            for g in witness.elements:
                commutes = True
                for h in F_gens:
                    if g * h != h * g:
                        commutes = False
                        break
                if commutes:
                    if g not in F:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite solvable group",
    "¬Q: The centralizer of F(G) in G is not a subgroup of F(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1