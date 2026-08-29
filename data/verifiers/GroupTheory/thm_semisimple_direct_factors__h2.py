import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (G, H, K) or a dictionary with keys 'G', 'H', 'K'.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            K = witness.get('K')
        else:
            G, H, K = witness
    except Exception:
        return [False, False]

    def get_all_elements(group):
        try:
            return set(group.generate())
        except Exception:
            pass
        try:
            return set(group.elements)
        except Exception:
            pass
        gens = list(group.generators)
        id_elem = gens[0]**0 if gens else None
        if id_elem is None:
            return set()
        elements = {id_elem}
        queue = [id_elem]
        while queue:
            curr = queue.pop(0)
            for g in gens:
                nxt = curr * g
                if nxt not in elements:
                    elements.add(nxt)
                    queue.append(nxt)
        return elements

    def is_semisimple(group):
        """
        A finite group is semisimple iff it has no non-trivial abelian normal subgroups.
        This is equivalent to saying that no non-identity element has an abelian normal closure.
        We check this by verifying that no non-identity conjugacy class consists of pairwise commuting elements.
        """
        try:
            if not hasattr(group, 'order'):
                return False
            order = group.order() if callable(group.order) else group.order
            if order > 10000:
                return False
            if order == 1:
                return True
                
            gens = list(group.generators)
            if not gens:
                return True
            id_elem = gens[0]**0
            
            elements = get_all_elements(group)
            checked = {id_elem}
            
            for x in elements:
                if x in checked:
                    continue
                
                # Generate the conjugacy class of x
                conj_class = {x}
                queue = [x]
                while queue:
                    curr = queue.pop(0)
                    for g in gens:
                        conj = (g**-1) * curr * g
                        if conj not in conj_class:
                            conj_class.add(conj)
                            queue.append(conj)
                
                checked.update(conj_class)
                
                # Check if the conjugacy class consists of pairwise commuting elements
                is_abelian = True
                conj_list = list(conj_class)
                for i in range(len(conj_list)):
                    for j in range(i + 1, len(conj_list)):
                        if conj_list[i] * conj_list[j] != conj_list[j] * conj_list[i]:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
                
                # If we found a non-identity element whose conjugacy class commutes pairwise,
                # it generates a non-trivial abelian normal subgroup.
                if is_abelian:
                    return False
                    
            return True
        except Exception:
            return False

    # H_1: G is a finite semisimple group
    try:
        h1_ok = is_semisimple(G)
    except Exception:
        h1_ok = False

    # ¬Q: Both H and K are semisimple groups (Negation: At least one is NOT semisimple)
    try:
        neg_q_ok = not (is_semisimple(H) and is_semisimple(K))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "¬Q: At least one of H or K is not a semisimple group"
]

N_HYP = 1
NEG_Q_INDEX = 1