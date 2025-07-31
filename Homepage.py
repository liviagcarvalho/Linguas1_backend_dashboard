import pandas as pd
from fastapi import APIRouter

router = APIRouter()

@router.get("/faturamento")
def get_faturamento_total():
    try:
        df = pd.read_csv("Aulas.csv")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        faturamento_total = df["price"].sum()

        # CONVERTER para tipo nativo (int ou float) para evitar erro de serialização
        return {"faturamento_total": float(faturamento_total)}
    
    except Exception as e:
        return {"erro": str(e)}

