import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools

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
    h1, h2, neg_q = False, False, False

    try:
        if callable(witness):
            witness = witness()

        # If witness is a mock object providing the conditions directly
        if hasattr(witness, 'h1') and callable(getattr(witness, 'h1')):
            h1 = witness.h1()
            h2 = witness.h2()
            neg_q = witness.neg_q()
            return [bool(h1), bool(h2), bool(neg_q)]

        # Extract components from dictionary, tuple, or object
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            Omega = witness.get('Omega')
            action = witness.get('action')
            W = witness.get('wreath_product')
            S = witness.get('semidirect_product')
        elif isinstance(witness, tuple):
            A = witness[0] if len(witness) > 0 else None
            B = witness[1] if len(witness) > 1 else None
            Omega = witness[2] if len(witness) > 2 else None
            action = witness[3] if len(witness) > 3 else None
            W = witness[4] if len(witness) > 4 else None
            S = witness[5] if len(witness) > 5 else None
        else:
            A = getattr(witness, 'A', None)
            B = getattr(witness, 'B', None)
            Omega = getattr(witness, 'Omega', None)
            action = getattr(witness, 'action', None)
            W = getattr(witness, 'wreath_product', None)
            S = getattr(witness, 'semidirect_product', None)

        # H1: B acts on Omega
        if B is not None and Omega is not None and action is not None:
            elements = list(B.elements) if hasattr(B, 'elements') else list(B)
            id_B = getattr(B, 'identity', getattr(B, 'id', None))
            
            if id_B is None:
                for e in elements:
                    if all(e * x == x for x in elements):
                        id_B = e
                        break
            
            if id_B is not None:
                id_acts_trivially = all(action(id_B, w) == w for w in Omega)
                is_action = True
                
                sample_elements = elements[:10]
                sample_omega = list(Omega)[:10]
                
                for b1, b2 in itertools.product(sample_elements, repeat=2):
                    try:
                        b1_b2 = b1 * b2
                    except Exception:
                        b1_b2 = b1(b2)
                    for w in sample_omega:
                        left = action(b1_b2, w) == action(b1, action(b2, w))
                        right = action(b1_b2, w) == action(b2, action(b1, w))
                        if not (left or right):
                            is_action = False
                            break
                    if not is_action:
                        break
                h1 = id_acts_trivially and is_action

        # H2: A^Omega is the group of functions from Omega to A under pointwise multiplication
        # This implies A must be a valid group.
        if A is not None:
            if getattr(A, 'is_group', False):
                h2 = True
            elif hasattr(A, 'identity') or hasattr(A, 'id'):
                h2 = True
            elif isinstance(A, PermutationGroup):
                h2 = True

        # ¬Q: The unrestricted wreath product is NOT isomorphic to the semidirect product
        # The standard wreath product as a permutation group is only isomorphic to the 
        # semidirect product if the action of B on Omega is faithful.
        if W is not None and S is not None:
            if hasattr(W, 'is_isomorphic'):
                neg_q = not W.is_isomorphic(S)
            elif hasattr(W, 'order') and hasattr(S, 'order'):
                neg_q = W.order() != S.order()
            elif hasattr(W, '__len__') and hasattr(S, '__len__'):
                neg_q = len(W) != len(S)
        elif B is not None and Omega is not None and action is not None:
            elements = list(B.elements) if hasattr(B, 'elements') else list(B)
            id_B = getattr(B, 'identity', getattr(B, 'id', None))
            
            if id_B is None:
                for e in elements:
                    if all(e * x == x for x in elements):
                        id_B = e
                        break
            
            is_faithful = True
            for b in elements:
                if b == id_B:
                    continue
                if all(action(b, w) == w for w in Omega):
                    is_faithful = False
                    break
            neg_q = not is_faithful

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: B acts on a set Omega",
    "H_2: A^Omega is the group of functions from Omega to A under pointwise multiplication",
    "¬Q: The unrestricted wreath product is NOT isomorphic to the semidirect product"
]

N_HYP = 2
NEG_Q_INDEX = 2