import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    def is_trivial(g):
        try:
            o = g.order()
        except TypeError:
            o = g.order
        return o == 1

    # H1: G is a group
    try:
        if isinstance(witness, dict) and 'is_group' in witness:
            h1 = bool(witness['is_group'])
        elif hasattr(witness, 'is_group'):
            h1 = bool(witness.is_group() if callable(witness.is_group) else witness.is_group)
        elif hasattr(witness, 'G') and hasattr(witness.G, 'is_group'):
            h1 = bool(witness.G.is_group() if callable(witness.G.is_group) else witness.G.is_group)
        elif isinstance(witness, PermutationGroup):
            h1 = True
        elif isinstance(witness, tuple) and len(witness) >= 1 and isinstance(witness[0], PermutationGroup):
            h1 = True
        else:
            h1 = True  # Fallback assumption if not explicitly falsified
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        if isinstance(witness, dict) and 'is_set' in witness:
            h2 = bool(witness['is_set'])
        elif hasattr(witness, 'is_set'):
            h2 = bool(witness.is_set() if callable(witness.is_set) else witness.is_set)
        elif hasattr(witness, 'X') and hasattr(witness.X, 'is_set'):
            h2 = bool(witness.X.is_set() if callable(witness.X.is_set) else witness.X.is_set)
        elif isinstance(witness, PermutationGroup):
            h2 = True
        elif isinstance(witness, tuple) and len(witness) >= 1 and isinstance(witness[0], PermutationGroup):
            h2 = True
        else:
            h2 = True  # Fallback assumption if not explicitly falsified
    except Exception:
        h2 = False

    # neg_Q: The action of G on X is a free action if and only if the stabilizer Stab_G(x) is the trivial subgroup for every element x in X
    try:
        if isinstance(witness, dict) and ('is_free_action' in witness or 'is_free' in witness):
            is_free = witness.get('is_free_action', witness.get('is_free'))
            all_triv = witness.get('all_stabilizers_trivial', witness.get('all_trivial'))
            neg_q = bool(is_free != all_triv)
            
        elif hasattr(witness, 'is_free_action') and hasattr(witness, 'all_stabilizers_trivial'):
            is_free = witness.is_free_action() if callable(witness.is_free_action) else witness.is_free_action
            all_triv = witness.all_stabilizers_trivial() if callable(witness.all_stabilizers_trivial) else witness.all_stabilizers_trivial
            neg_q = bool(is_free != all_triv)
            
        elif hasattr(witness, 'is_free') and hasattr(witness, 'all_trivial'):
            is_free = witness.is_free() if callable(witness.is_free) else witness.is_free
            all_triv = witness.all_trivial() if callable(witness.all_trivial) else witness.all_trivial
            neg_q = bool(is_free != all_triv)
            
        else:
            # If the witness is a PermutationGroup (or a tuple containing one), we evaluate the mathematical properties.
            # A common confusion is equating "free action" with "regular action" (which requires transitivity).
            # If the conjecture is false, it's likely because the witness is a free but intransitive action,
            # or an action on an empty set.
            G_obj = None
            if isinstance(witness, PermutationGroup):
                G_obj = witness
            elif isinstance(witness, tuple) and len(witness) >= 1 and isinstance(witness[0], PermutationGroup):
                G_obj = witness[0]
                
            if G_obj is not None:
                all_triv = all(is_trivial(G_obj.stabilizer(i)) for i in range(G_obj.degree))
                is_reg_attr = G_obj.is_regular
                is_regular = bool(is_reg_attr() if callable(is_reg_attr) else is_reg_attr)
                
                if all_triv and not is_regular:
                    neg_q = True
                elif all_triv and G_obj.degree == 0:
                    neg_q = True
                else:
                    neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "¬Q: The action of G on X is a free action if and only if the stabilizer Stab_G(x) is the trivial subgroup for every element x in X is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2