"""
Pytest конфигурация и фикстуры для всего проекта
"""
import pytest
import sqlite3
from pathlib import Path
from fastapi.testclient import TestClient
from typing import Generator, Dict, Any

# Добавляем путь к backend в sys.path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from backend.app.main import app
from backend.app.database import get_db, init_db
from backend.app.models import CalculationRequest, Material, WeldMethod


@pytest.fixture
def client() -> Generator:
    """
    Фикстура для тестирования API клиента
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_db():
    """
    Фикстура для временной тестовой БД
    """
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    yield conn
    conn.close()


@pytest.fixture
def sample_rds_request() -> CalculationRequest:
    """
    Пример запроса для РДС
    """
    return CalculationRequest(
        method=WeldMethod.RDS,
        material=Material.CARBON_STEEL,
        thickness=6.0,
        joint_group="C",
        joint_type="C1",
        length=500,
        position="lower",
        electrode_brand="УОНИ 13/45"
    )


@pytest.fixture
def sample_tig_aluminum_request() -> CalculationRequest:
    """
    Пример запроса для TIG + Алюминий (ГОСТ 14806-80)
    """
    return CalculationRequest(
        method=WeldMethod.TIG,
        material=Material.ALUMINUM,
        thickness=8.0,
        joint_group="C",
        joint_type="C4",
        length=500,
        position="lower",
        with_filler=True,
        gost_standard="ГОСТ 14806-80"
    )


@pytest.fixture
def sample_mig_request() -> CalculationRequest:
    """
    Пример запроса для MIG-MAG
    """
    return CalculationRequest(
        method=WeldMethod.MIG,
        material=Material.CARBON_STEEL,
        thickness=4.0,
        joint_group="T",
        joint_type="T1",
        length=300,
        position="lower",
        gas_mixture="80%Ar+20%CO₂"
    )
