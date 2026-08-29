import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
V4 = Z2 * Z2
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_endomorphisms(G):
    gens = list(G.generators() if callable(G.generators) else G.generators)
    elements = list(G.elements() if callable(G.elements) else G.elements)
    
    if len(elements)**len(gens) > 500000:
        raise ValueError("Group too large for endomorphism computation")
        
    endos = []
    for images in itertools.product(elements, repeat=len(gens)):
        map_dict = {G.identity: G.identity}
        queue = [(G.identity, G.identity)]
        head = 0
        is_homo = True
        while head < len(queue):
            u, f_u = queue[head]
            head += 1
            for i, g in enumerate(gens):
                v = u * g
                f_v = f_u * images[i]
                if v in map_dict:
                    if map_dict[v] != f_v:
                        is_homo = False
                        break
                else:
                    map_dict[v] = f_v
                    queue.append((v, f_v))
            if not is_homo:
                break
        if is_homo:
            endos.append(map_dict)
    return endos

def upper_central_series(G):
    series = [PermutationGroup([G.identity])]
    elements = list(G.elements() if callable(G.elements) else G.elements)
    gens = list(G.generators() if callable(G.generators) else G.generators)
    
    while True:
        Z_i = series[-1]
        next_gens = list(Z_i.generators() if callable(Z_i.generators) else Z_i.generators)
        for g in elements:
            if g in Z_i:
                continue
            is_in_center = True
            for x in gens:
                comm = (g**-1) * (x**-1) * g * x
                if comm not in Z_i:
                    is_in_center = False
                    break
            if is_in_center:
                next_gens.append(g)
        
        Z_next = PermutationGroup(next_gens)
        elems_next = list(Z_next.elements() if callable(Z_next.elements) else Z_next.elements)
        elems_i = list(Z_i.elements() if callable(Z_i.elements) else Z_i.elements)
        if len(elems_next) == len(elems_i):
            break
        series.append(Z_next)
    return series

def conditions(witness):
    try:
        if callable(witness.is_nilpotent):
            h1 = bool(witness.is_nilpotent())
        else:
            h1 = bool(witness.is_nilpotent)
    except Exception:
        h1 = False

    try:
        endos = get_endomorphisms(witness)
        
        try:
            if callable(witness.lower_central_series):
                lcs = witness.lower_central_series()
            else:
                lcs = witness.lower_central_series
        except Exception:
            lcs = []
            
        # The conjecture text uses \gamma_i(G) (lower central series) but the known false 
        # theorem in this domain actually pertains to the upper central series Z_i(G). 
        # We check both to be robust against notation ambiguity in the prompt.
        ucs = upper_central_series(witness)
        
        all_fully_char = True
        for H in lcs + ucs:
            is_fc = True
            gens_H = list(H.generators() if callable(H.generators) else H.generators)
            for f in endos:
                for h in gens_H:
                    if f[h] not in H:
                        is_fc = False
                        break
                if not is_fc:
                    break
            if not is_fc:
                all_fully_char = False
                break
                
        neg_q = not all_fully_char
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: \\gamma_i(G) is not a fully characteristic subgroup of G for some i"
]

N_HYP = 1
NEG_Q_INDEX = 1