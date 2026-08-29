import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

I2 = sympy.ImmutableMatrix(sympy.eye(2))
I3 = sympy.ImmutableMatrix(sympy.eye(3))
O2 = sympy.ImmutableMatrix(sympy.zeros(2, 2))
O3 = sympy.ImmutableMatrix(sympy.zeros(3, 3))

def inv(g):
    try:
        return ~g
    except Exception:
        return g**-1

def get_elems_gens(obj):
    if hasattr(obj, 'generate'):
        return set(obj.generate()), obj.generators
    elif hasattr(obj, 'elements'):
        gens = obj.generators if hasattr(obj, 'generators') else obj.elements
        return set(obj.elements), gens
    else:
        return set(obj), obj

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False]
        
    try:
        G_elems, G_gens = get_elems_gens(G)
        N_elems, N_gens = get_elems_gens(N)
        H_elems, H_gens = get_elems_gens(H)
        
        if not N_elems.issubset(G_elems):
            h1 = False
        elif not H_elems.issubset(G_elems):
            h1 = False
        else:
            is_normal = True
            for n in N_gens:
                for g in G_gens:
                    if g * n * inv(g) not in N_elems:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            if not is_normal:
                h1 = False
            else:
                if len(N_elems.intersection(H_elems)) != 1:
                    h1 = False
                else:
                    if len(N_elems) * len(H_elems) != len(G_elems):
                        h1 = False
                    else:
                        h1 = True
    except Exception:
        h1 = False
        
    try:
        core_set = set(H_elems)
        for g in G_elems:
            conj = {g * h * inv(g) for h in H_elems}
            core_set = core_set.intersection(conj)
            
        C_H_N = set()
        for h in H_elems:
            if all(h * n == n * h for n in N_elems):
                C_H_N.add(h)
                
        neg_q = (core_set != C_H_N)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an internal semidirect product of a normal subgroup N and a subgroup H",
    "¬Q: The normal core K of H in G is not equal to the centralizer C_H(N) of N in H"
]

N_HYP = 1
NEG_Q_INDEX = 1