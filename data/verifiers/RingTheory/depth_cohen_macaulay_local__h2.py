import sympy
from sympy.abc import x, y, z, w

class LocalRing:
    """
    A mock class to represent a local ring with specific properties.
    """
    def __init__(self, is_commutative=True, is_noetherian=True, is_local=True, depth=0, krull_dimension=0):
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian
        self.is_local = is_local
        self.depth = depth
        self.krull_dimension = krull_dimension

def get_ring_properties(witness):
    if isinstance(witness, dict):
        if "depth" in witness and ("dim" in witness or "krull_dimension" in witness):
            return {
                "is_commutative": witness.get("is_commutative", True),
                "is_noetherian": witness.get("is_noetherian", True),
                "is_local": witness.get("is_local", True),
                "depth": witness.get("depth"),
                "dim": witness.get("krull_dimension", witness.get("dim"))
            }
            
    if hasattr(witness, "is_commutative") and hasattr(witness, "depth"):
        try:
            depth = witness.depth() if callable(witness.depth) else witness.depth
            dim_attr = getattr(witness, "krull_dimension", getattr(witness, "dim", None))
            dim = dim_attr() if callable(dim_attr) else dim_attr
            if depth is not None and dim is not None:
                return {
                    "is_commutative": bool(witness.is_commutative),
                    "is_noetherian": bool(witness.is_noetherian),
                    "is_local": bool(getattr(witness, "is_local", True)),
                    "depth": int(depth),
                    "dim": int(dim)
                }
        except Exception:
            pass
            
    if isinstance(witness, (tuple, list)) and len(witness) >= 5:
        if isinstance(witness[0], bool) and isinstance(witness[3], int):
            try:
                return {
                    "is_commutative": bool(witness[0]),
                    "is_noetherian": bool(witness[1]),
                    "is_local": bool(witness[2]),
                    "depth": int(witness[3]),
                    "dim": int(witness[4])
                }
            except Exception:
                pass

    if isinstance(witness, str):
        w_str = witness.replace(" ", "").lower()
        if ("x**2" in w_str or "x^2" in w_str) and ("x*y" in w_str or "xy" in w_str):
            return {"is_commutative": True, "is_noetherian": True, "is_local": True, "depth": 0, "dim": 1}
        if ("xz" in w_str or "x*z" in w_str) and ("yz" in w_str or "y*z" in w_str):
            return {"is_commutative": True, "is_noetherian": True, "is_local": True, "depth": 1, "dim": 2}

    try:
        if hasattr(witness, "base_ideal"):
            gens_list = witness.base_ideal.gens
        elif hasattr(witness, "gens"):
            gens_list = witness.gens
        else:
            gens_list = witness
            
        gens = set(str(g).replace(" ", "") for g in gens_list)
        if gens == {"x**2", "x*y"} or gens == {"x^2", "xy"}:
            return {"is_commutative": True, "is_noetherian": True, "is_local": True, "depth": 0, "dim": 1}
        if gens == {"x*z", "y*z"} or gens == {"xz", "yz"}:
            return {"is_commutative": True, "is_noetherian": True, "is_local": True, "depth": 1, "dim": 2}
        if gens == {"x*z", "x*w", "y*z", "y*w"}:
            return {"is_commutative": True, "is_noetherian": True, "is_local": True, "depth": 1, "dim": 2}
    except Exception:
        pass

    return None

def conditions(witness) -> list[bool]:
    props = get_ring_properties(witness)
    if props is None:
        return [False, False]
    
    try:
        h1 = bool(props["is_commutative"] and props["is_noetherian"] and props["is_local"])
    except Exception:
        h1 = False
        
    try:
        depth = props["depth"]
        dim = props["dim"]
        if depth is not None and dim is not None:
            neg_q = (depth != dim)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian local ring",
    "¬Q: The depth of R is not equal to the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1