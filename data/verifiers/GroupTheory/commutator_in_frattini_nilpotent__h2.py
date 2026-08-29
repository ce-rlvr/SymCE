import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        # H_1: G is a finite group
        try:
            is_group = getattr(witness, 'is_group', False)
            if is_group is not True:
                h1 = False
            else:
                order = witness.order()
                h1 = isinstance(order, (int, sympy.Integer)) and order > 0
        except Exception:
            h1 = False

        if not h1:
            return [False, False]

        # Prevent timeouts for excessively large groups
        if witness.order() > 100:
            return [False, False]

        # neg_Q: Commutator subgroup is NOT contained in Frattini subgroup
        try:
            elements = list(witness.elements)
            id_el = None
            for e in elements:
                if e * e == e:
                    id_el = e
                    break
            
            if id_el is None:
                neg_q = False
            else:
                # Find all subgroups
                subgroups = {frozenset([id_el])}
                queue = [frozenset([id_el])]
                
                while queue:
                    curr = queue.pop(0)
                    for g in elements:
                        if g not in curr:
                            new_sub = set(curr)
                            frontier = {g}
                            while frontier:
                                new_sub.update(frontier)
                                next_frontier = set()
                                for a in new_sub:
                                    for b in frontier:
                                        ab = a * b
                                        if ab not in new_sub:
                                            next_frontier.add(ab)
                                        ba = b * a
                                        if ba not in new_sub:
                                            next_frontier.add(ba)
                                frontier = next_frontier
                            new_sub_frozen = frozenset(new_sub)
                            if new_sub_frozen not in subgroups:
                                subgroups.add(new_sub_frozen)
                                queue.append(new_sub_frozen)
                                if len(subgroups) > 5000:
                                    return [h1, False]
                
                # Find maximal subgroups
                G_set = frozenset(elements)
                proper_subgroups = [H for H in subgroups if H != G_set]
                maximal = []
                for H in proper_subgroups:
                    is_maximal = True
                    for K in proper_subgroups:
                        if H != K and H.issubset(K):
                            is_maximal = False
                            break
                    if is_maximal:
                        maximal.append(H)
                
                # Frattini subgroup is the intersection of all maximal subgroups
                if not maximal:
                    frattini = G_set
                else:
                    frattini = set(maximal[0])
                    for M in maximal[1:]:
                        frattini = frattini.intersection(M)
                    frattini = frozenset(frattini)
                
                # Commutator subgroup
                commutators = set()
                for x in elements:
                    for y in elements:
                        c = (~x) * (~y) * x * y
                        commutators.add(c)
                
                commutator_sub = set([id_el])
                frontier = commutators - {id_el}
                while frontier:
                    commutator_sub.update(frontier)
                    next_frontier = set()
                    for a in commutator_sub:
                        for b in frontier:
                            ab = a * b
                            if ab not in commutator_sub:
                                next_frontier.add(ab)
                            ba = b * a
                            if ba not in commutator_sub:
                                next_frontier.add(ba)
                    frontier = next_frontier
                
                commutator = frozenset(commutator_sub)
                
                neg_q = not commutator.issubset(frattini)
        except Exception:
            neg_q = False

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The commutator subgroup of G is not contained in the Frattini subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1