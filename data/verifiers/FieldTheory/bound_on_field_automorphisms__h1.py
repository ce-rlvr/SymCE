import sympy
from sympy import S
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

Aleph0 = S.Aleph(0)
Aleph1 = S.Aleph(1)
Aleph2 = S.Aleph(2)
c = 2**Aleph0

def conditions(witness) -> list[bool]:
    try:
        # Handle string witnesses of known counterexamples
        if isinstance(witness, str):
            w_clean = witness.replace(" ", "").lower()
            if w_clean in ["c/q", "q_bar/q", "qbar/q", "c/r(x)", "c(x)/c"]:
                return [True]
            return [False]
            
        # Extract automorphism group cardinality and extension degree
        if isinstance(witness, dict):
            aut_card = witness.get('aut_cardinality', witness.get('Aut', witness.get('aut_group_size')))
            ext_deg = witness.get('degree', witness.get('deg', witness.get('extension_degree')))
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            aut_card, ext_deg = witness
        else:
            aut_card = getattr(witness, 'aut_cardinality', getattr(witness, 'Aut', None))
            ext_deg = getattr(witness, 'degree', getattr(witness, 'deg', None))
            
        if aut_card is not None and ext_deg is not None:
            # If aut_card is a group object or a collection, get its size
            if hasattr(aut_card, 'order') and callable(aut_card.order):
                try:
                    aut_card = aut_card.order()
                except Exception:
                    pass
            elif hasattr(aut_card, '__len__') and not isinstance(aut_card, str):
                try:
                    aut_card = len(aut_card)
                except Exception:
                    pass

            # Parse string representations of cardinals if necessary
            if isinstance(aut_card, str):
                aut_card = sympy.sympify(aut_card, locals={'c': 2**S.Aleph(0), 'Aleph0': S.Aleph(0), 'Aleph1': S.Aleph(1)})
            if isinstance(ext_deg, str):
                ext_deg = sympy.sympify(ext_deg, locals={'c': 2**S.Aleph(0), 'Aleph0': S.Aleph(0), 'Aleph1': S.Aleph(1)})
            
            # Evaluate if |Aut(E/F)| > degree of E over F
            try:
                neg_q = bool(aut_card > ext_deg)
            except TypeError:
                # Fallback for sympy relationals that cannot be evaluated to bool directly
                s_aut = str(aut_card).replace(" ", "")
                s_ext = str(ext_deg).replace(" ", "")
                if s_aut == "2**Aleph(0)" and s_ext == "Aleph(0)":
                    neg_q = True
                elif s_aut == "2**(2**Aleph(0))" and s_ext == "2**Aleph(0)":
                    neg_q = True
                else:
                    neg_q = False
        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = ["¬Q: The cardinality of the automorphism group Aut(E/F) is strictly greater than the degree of E over F"]
N_HYP = 0
NEG_Q_INDEX = 0