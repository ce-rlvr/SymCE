import sympy
import math
import itertools
import functools

class TopologicalSpace:
    def __init__(self, name, metric, locally_compact, sigma_compact):
        self.name = name
        self.metric = metric
        self.locally_compact = locally_compact
        self.sigma_compact = sigma_compact

# Top-level setup: named object bindings that the witness expression may reference
R_discrete = TopologicalSpace("R_discrete", metric=True, locally_compact=True, sigma_compact=False)
uncountable_discrete_space = R_discrete
R = TopologicalSpace("R", metric=True, locally_compact=True, sigma_compact=True)
Q = TopologicalSpace("Q", metric=True, locally_compact=False, sigma_compact=True)
Z = TopologicalSpace("Z", metric=True, locally_compact=True, sigma_compact=True)
long_line = TopologicalSpace("long_line", metric=False, locally_compact=True, sigma_compact=False)
Sorgenfrey_line = TopologicalSpace("Sorgenfrey_line", metric=False, locally_compact=False, sigma_compact=False)
Baire_space = TopologicalSpace("Baire_space", metric=True, locally_compact=False, sigma_compact=False)
omega_1 = TopologicalSpace("omega_1", metric=False, locally_compact=True, sigma_compact=False)
Hilbert_cube = TopologicalSpace("Hilbert_cube", metric=True, locally_compact=True, sigma_compact=True)
l2 = TopologicalSpace("l2", metric=True, locally_compact=False, sigma_compact=False)

def get_space_props(witness):
    if hasattr(witness, "metric") and hasattr(witness, "locally_compact") and hasattr(witness, "sigma_compact"):
        return {
            "metric": bool(witness.metric),
            "locally_compact": bool(witness.locally_compact),
            "sigma_compact": bool(witness.sigma_compact)
        }
    
    if isinstance(witness, dict):
        if "metric" in witness and "locally_compact" in witness and "sigma_compact" in witness:
            return {
                "metric": bool(witness["metric"]),
                "locally_compact": bool(witness["locally_compact"]),
                "sigma_compact": bool(witness["sigma_compact"])
            }

    if isinstance(witness, str):
        w = witness.lower().strip().replace("_", " ")
        if w in ["r discrete", "uncountable discrete", "discrete uncountable", "r discrete metric", "uncountable discrete space", "r with discrete metric"]:
            return {"metric": True, "locally_compact": True, "sigma_compact": False}
        if w in ["r", "reals", "real line", "r1"]:
            return {"metric": True, "locally_compact": True, "sigma_compact": True}
        if w in ["q", "rationals"]:
            return {"metric": True, "locally_compact": False, "sigma_compact": True}
        if w in ["z", "integers", "n", "naturals"]:
            return {"metric": True, "locally_compact": True, "sigma_compact": True}
        if w in ["long line"]:
            return {"metric": False, "locally_compact": True, "sigma_compact": False}
        if w in ["sorgenfrey line", "lower limit topology"]:
            return {"metric": False, "locally_compact": False, "sigma_compact": False}
        if w in ["baire space", "n^n", "irrationals"]:
            return {"metric": True, "locally_compact": False, "sigma_compact": False}
        if w in ["omega 1", "first uncountable ordinal"]:
            return {"metric": False, "locally_compact": True, "sigma_compact": False}
        if w in ["countable discrete", "countable discrete space"]:
            return {"metric": True, "locally_compact": True, "sigma_compact": True}
        if w in ["hilbert cube", "[0,1]^n"]:
            return {"metric": True, "locally_compact": True, "sigma_compact": True}
        if w in ["l2", "hilbert space", "l^2"]:
            return {"metric": True, "locally_compact": False, "sigma_compact": False}
        if w in ["s1", "circle", "s2", "sphere", "t2", "torus", "cantor set", "p-adic numbers", "p-adics"]:
            return {"metric": True, "locally_compact": True, "sigma_compact": True}
            
    return None

def conditions(witness) -> list[bool]:
    props = get_space_props(witness)
    if props is None:
        return [False, False, False]
    
    try:
        h1 = props["metric"]
    except Exception:
        h1 = False
        
    try:
        h2 = props["locally_compact"]
    except Exception:
        h2 = False
        
    try:
        neg_q = not props["sigma_compact"]
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: X is locally compact",
    "¬Q: X is not sigma-compact"
]

N_HYP = 2
NEG_Q_INDEX = 2