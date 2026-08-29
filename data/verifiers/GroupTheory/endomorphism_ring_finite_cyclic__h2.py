import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    # The witness can be a group G, or a tuple (G, n)
    if isinstance(witness, tuple) and len(witness) == 2:
        G, n = witness
    else:
        G = witness
        try:
            n = G.order()
        except Exception:
            n = None

    # H_1: G is a finite cyclic group of order n
    try:
        if isinstance(G, PermutationGroup):
            h1 = getattr(G, 'is_finite', True) and getattr(G, 'is_cyclic', False) and G.order() == n
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: End(G) is NOT isomorphic to the ring Z_n
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        elif not getattr(G, 'is_abelian', False):
            # If G is not abelian, End(G) is not a ring, so it cannot be isomorphic to Z_n
            neg_q = True
        else:
            # For an abelian group, End(G) is a ring.
            # We count the number of endomorphisms by finding all valid mappings of the generators.
            gens = G.generators
            elements = list(G.elements)
            identity = G.identity
            
            count = 0
            for target in itertools.product(elements, repeat=len(gens)):
                gen_map = dict(zip(gens, target))
                mapping = {identity: identity}
                valid = True
                queue = [identity]
                
                # BFS to extend the homomorphism to all elements
                while queue:
                    curr = queue.pop(0)
                    for g in gens:
                        nxt = curr * g
                        val = mapping[curr] * gen_map[g]
                        if nxt in mapping:
                            if mapping[nxt] != val:
                                valid = False
                                break
                        else:
                            mapping[nxt] = val
                            queue.append(nxt)
                    if not valid:
                        break
                        
                if valid and len(mapping) == len(elements):
                    count += 1
            
            # End(G) is isomorphic to Z_n iff G is cyclic and |End(G)| == n and |G| == n
            if count == n and getattr(G, 'is_cyclic', False) and G.order() == n:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group of order n",
    "¬Q: End(G) is not isomorphic to the ring Z_n"
]

N_HYP = 1
NEG_Q_INDEX = 1