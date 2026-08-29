import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

KNOWN_RINGS = {
    "z": True,
    "z_p": True,
    "q[x]": True,
    "r[x]": True,
    "c[x]": True,
    "f_2[x]": True,
}

KNOWN_MODULES = {
    "z": [
        "z^n", "p-adicintegers", "prod(z/pz)", "q", "z", "z^(n)", "oplus(z/pz)", 
        "z^omega", "z^(omega)", "z^\\mathbb{n}", "z^(\\mathbb{n})", "z^\\omega", "z^(\\omega)"
    ],
    "q[x]": ["q[[x]]", "q(x)"],
}

KNOWN_PAIRS = {
    ("z", "z^n", "z^(n)"): (True, False),
    ("z", "z^\\mathbb{n}", "z^(\\mathbb{n})"): (True, False),
    ("z", "z^omega", "z^(omega)"): (True, False),
    ("z", "z^\\omega", "z^(\\omega)"): (True, False),
    ("z", "p-adicintegers", "z"): (True, False),
    ("z", "prod(z/pz)", "oplus(z/pz)"): (True, False),
    ("z", "q", "z"): (False, False),
    ("z", "z", "2z"): (False, False),
    ("q[x]", "q[[x]]", "q[x]"): (True, False),
}

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, M, N = witness
            if isinstance(R, str) and isinstance(M, str) and isinstance(N, str):
                r_norm = R.replace(" ", "").lower()
                m_norm = M.replace(" ", "").lower()
                n_norm = N.replace(" ", "").lower()
                
                h1 = KNOWN_RINGS.get(r_norm, False)
                h2 = m_norm in KNOWN_MODULES.get(r_norm, [])
                pure, summand = KNOWN_PAIRS.get((r_norm, m_norm, n_norm), (False, True))
                h3 = pure
                neg_q = not summand
            else:
                if isinstance(R, dict):
                    h1 = bool(R.get("is_PID", False))
                else:
                    h1 = bool(getattr(R, "is_PID", False))
                    
                if isinstance(M, dict):
                    h2 = bool(M.get("is_module", False))
                else:
                    h2 = bool(getattr(M, "is_module", False))
                    
                if isinstance(N, dict):
                    h3 = bool(N.get("is_pure_submodule", False))
                    neg_q = not bool(N.get("is_direct_summand", True))
                else:
                    h3 = bool(getattr(N, "is_pure_submodule", False))
                    neg_q = not bool(getattr(N, "is_direct_summand", True))
                    
        elif isinstance(witness, dict):
            h1 = bool(witness.get("is_PID", False))
            h2 = bool(witness.get("is_module", False))
            h3 = bool(witness.get("is_pure_submodule", False))
            neg_q = not bool(witness.get("is_direct_summand", True))
            
        else:
            h1 = bool(getattr(witness, "is_PID", False))
            h2 = bool(getattr(witness, "is_module", False))
            h3 = bool(getattr(witness, "is_pure_submodule", False))
            neg_q = not bool(getattr(witness, "is_direct_summand", True))
            
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is an R-module",
    "H_3: N is a pure submodule of M",
    "¬Q: N is not a direct summand of M"
]

N_HYP = 3
NEG_Q_INDEX = 3