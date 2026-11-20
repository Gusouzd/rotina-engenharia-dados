import pandas as pd
from src.validacao import validar

def test_validar_rejeita_nulos():
    df = pd.DataFrame({
        "data": ["2026-01-01", None],
        "nome": ["Confraternização", "Carnaval"],
        "tipo": ["nacional", "nacional"],
    })
    assert validar(df) == False


def test_validar_rejeita_data_invalida():
    df = pd.DataFrame({
        "data": ["2026-01-01", "não é uma data"],
        "nome": ["Confraternização", "Carnaval"],
        "tipo": ["nacional", "nacional"],
    })
    assert validar(df) == False


def test_validar_rejeita_duplicata():
    df = pd.DataFrame({
        "data": ["2026-01-01", "2026-01-01"],
        "nome": ["Confraternização", "Confraternização"],
        "tipo": ["nacional", "nacional"],
    })
    assert validar(df) == False


def test_validar_aceita_dados_corretos():
    df = pd.DataFrame({
        "data": ["2026-01-01", "2026-02-17"],
        "nome": ["Confraternização", "Carnaval"],
        "tipo": ["nacional", "nacional"],
    })
    assert validar(df) == True