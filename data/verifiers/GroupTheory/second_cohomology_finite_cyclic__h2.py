import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_group_props(g):
    """Helper to safely extract is_cyclic and order from a group object."""
    order_attr = getattr(g, 'order', None)
    if order_attr is None:
        return False, None
    if callable(order_attr):
        order = order_attr()
    else:
        order = order_attr

    cyclic_attr = getattr(g, 'is_cyclic', None)
    if cyclic_attr is not None:
        if callable(cyclic_attr):
            is_cyclic = cyclic_attr()
        else:
            is_cyclic = cyclic_attr
        return is_cyclic, order

    # Fallback: check if there is an element of order equal to group order
    if hasattr(g, 'elements'):
        for elem in g.elements:
            elem_order = getattr(elem, 'order')
            o = elem_order() if callable(elem_order) else elem_order
            if o == order:
                return True, order
        return False, order
        
    return False, order

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The conjecture states that for a finite cyclic group G, H^2(G; Z) is isomorphic to G.
    This is true for the trivial action, but fails if G acts non-trivially on Z.
    A non-trivial action requires G to have even order, and the generator acts by multiplication by -1.
    """
    try:
        n = None
        action = None
        
        # Parse witness
        if isinstance(witness, int):
            n = witness
            action = -1 if n % 2 == 0 else 1
        elif isinstance(witness, tuple) and len(witness) == 2:
            g, act = witness
            if isinstance(g, int):
                n = g
            else:
                is_cyclic, order = get_group_props(g)
                if not is_cyclic:
                    return [False, False]
                n = order
            action = act
        elif isinstance(witness, dict):
            n = witness.get('n')
            if n is None:
                g = witness.get('G')
                if g is not None:
                    is_cyclic, order = get_group_props(g)
                    if not is_cyclic:
                        return [False, False]
                    n = order
            action = witness.get('action')
            if action is None and n is not None:
                action = -1 if n % 2 == 0 else 1
        else:
            is_cyclic, order = get_group_props(witness)
            if not is_cyclic:
                return [False, False]
            n = order
            action = -1 if n % 2 == 0 else 1
            
        # H_1: G is a finite cyclic group of order n
        # The action must be a valid homomorphism G -> Aut(Z) = {1, -1}
        if not isinstance(n, int) or n < 1:
            return [False, False]
        if action not in (1, -1):
            return [False, False]
        if action == -1 and n % 2 != 0:
            return [False, False]
            
        h1 = True
        
        # Conclusion: H^2(G; Z) is isomorphic to G
        # If action == 1 (trivial), H^2(G; Z) = Z_n, which has order n.
        # If action == -1 (non-trivial), H^2(G; Z) = 0, which has order 1.
        h2_order = n if action == 1 else 1
        
        # The conclusion fails if the orders do not match
        neg_q = (h2_order != n)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group of order n",
    "¬Q: H^2(G; Z) is not isomorphic to G"
]

N_HYP = 1
NEG_Q_INDEX = 1