import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import AlternatingGroup, SymmetricGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G, H = witness.G, witness.H
    except Exception:
        return [False, False, False]

    def get_op(obj):
        if hasattr(obj, 'op'):
            return obj.op
        if hasattr(obj, 'operation'):
            return obj.operation
        def default_op(x, y):
            try:
                return x * y
            except Exception:
                return x + y
        return default_op

    op = get_op(G)

    # H1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        elif hasattr(G, 'is_subgroup'):
            h1 = bool(G.is_subgroup(H))
        else:
            H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
            G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
            
            is_subset = all(x in G_elems for x in H_elems)
            if not is_subset:
                h1 = False
            else:
                is_closed = True
                for x in H_elems:
                    for y in H_elems:
                        try:
                            if op(x, y) not in H_elems:
                                is_closed = False
                                break
                        except Exception:
                            is_closed = False
                            break
                    if not is_closed:
                        break
                # For finite sets, non-empty and closed implies subgroup
                h1 = is_closed and len(H_elems) > 0
    except Exception:
        h1 = False

    # H2: The index of H in G is exactly 2
    try:
        if hasattr(G, 'index'):
            h2 = (G.index(H) == 2)
        elif hasattr(G, 'order') and hasattr(H, 'order'):
            h2 = (G.order() / H.order() == 2)
        else:
            H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
            G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
            h2 = (len(G_elems) / len(H_elems) == 2)
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist a surjective group homomorphism from G to C2 with kernel H
    try:
        is_group = False
        if hasattr(G, 'is_group') and G.is_group:
            is_group = True
        elif isinstance(G, PermutationGroup):
            is_group = True
        elif type(G).__name__ == 'MatrixGroup':
            is_group = True
            
        if is_group:
            # For any group, an index 2 subgroup is always normal, and the quotient is isomorphic to C2.
            # Thus, the canonical projection is a surjective homomorphism to C2 with kernel H.
            neg_q = False
        else:
            # If G is not a group (e.g. a semigroup or loop), we manually check if the unique 
            # candidate map f(x) = 1 if x in H else -1 is a valid homomorphism.
            G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
            H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
            
            H_set = set(H_elems)
            is_homo = True
            
            for x in G_elems:
                for y in G_elems:
                    try:
                        xy = op(x, y)
                    except Exception:
                        is_homo = False
                        break
                    fx = 1 if x in H_set else -1
                    fy = 1 if y in H_set else -1
                    fxy = 1 if xy in H_set else -1
                    if fxy != fx * fy:
                        is_homo = False
                        break
                if not is_homo:
                    break
            neg_q = not is_homo
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is exactly 2",
    "¬Q: There does not exist a surjective group homomorphism from G to the cyclic group of order 2 such that H is the kernel"
]

N_HYP = 2
NEG_Q_INDEX = 2