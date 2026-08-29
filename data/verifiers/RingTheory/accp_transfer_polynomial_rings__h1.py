import sympy

class _CounterexampleRing:
    def __init__(self, name, accp, poly_accp):
        self.name = name
        self.accp = accp
        self.poly_accp = poly_accp
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name

RoitmanRing = _CounterexampleRing("RoitmanRing", accp=True, poly_accp=False)
GramsRing = _CounterexampleRing("GramsRing", accp=True, poly_accp=False)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'accp'):
            h1 = witness.accp
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'poly_accp'):
            q = witness.poly_accp
        else:
            q = True
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R satisfies the ascending chain condition on principal ideals",
    "¬Q: The polynomial ring over R does not satisfy the ascending chain condition on principal ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1