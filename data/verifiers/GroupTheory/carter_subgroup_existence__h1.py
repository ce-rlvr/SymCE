import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "¬Q: G does not contain a nilpotent self-normalizing subgroup"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, PermutationGroup):
            return [False]
            
        elements = []
        for i, g in enumerate(witness.generate()):
            if i > 500:  # Prevent timeouts on unreasonably large witnesses
                return [False]
            elements.append(g)
            
        if not elements:
            return [False]
            
        identity = elements[0]**0
        triv_els = frozenset([identity])
        
        # Map from frozenset of elements to a list of generators
        subgroups_by_elements = {triv_els: [identity]}
        queue = [triv_els]
        
        # BFS to find all subgroups
        while queue:
            H_els = queue.pop(0)
            H_gens = subgroups_by_elements[H_els]
            
            for g in elements:
                if g not in H_els:
                    new_gens = H_gens + [g]
                    closure = set(H_els)
                    q2 = list(H_els)
                    
                    # Compute the closure of H_els under the new generator
                    while q2:
                        x = q2.pop(0)
                        for y in new_gens:
                            xy = x * y
                            if xy not in closure:
                                closure.add(xy)
                                q2.append(xy)
                    
                    K_els = frozenset(closure)
                    if K_els not in subgroups_by_elements:
                        subgroups_by_elements[K_els] = new_gens
                        queue.append(K_els)
                        
        has_carter = False
        
        # Check each subgroup for nilpotency and self-normalization
        for K_els, K_gens in subgroups_by_elements.items():
            K = PermutationGroup(K_gens)
            
            nilp = False
            if hasattr(K, 'is_nilpotent'):
                val = K.is_nilpotent
                if callable(val):
                    nilp = val()
                else:
                    nilp = val
                    
            if nilp:
                is_self_norm = True
                for g in elements:
                    if g not in K_els:
                        normalizes = True
                        g_inv = g**-1
                        for k in K_gens:
                            if (g * k * g_inv) not in K_els:
                                normalizes = False
                                break
                        if normalizes:
                            is_self_norm = False
                            break
                
                if is_self_norm:
                    has_carter = True
                    break
                    
        neg_q = not has_carter
        return [neg_q]
        
    except Exception:
        return [False]