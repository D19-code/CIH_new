"""
Hospital Management Router

Endpoints:
- POST /api/hospitals - Create a new hospital
- GET /api/hospitals - List all hospitals
- GET /api/hospitals/{hospital_id} - Get specific hospital details
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.hospital import HospitalCreate, HospitalResponse

router = APIRouter()

# =========================================================
# MOCK DATABASE (used for deployment/demo – no PostgreSQL)
# =========================================================

HOSPITALS_DB = [
    {
        "id": 1,
        "name": "City General Hospital",
        "location": "Delhi",
        "total_beds": 250,
        "icu_beds": 50
    },
    {
        "id": 2,
        "name": "Metro Care Hospital",
        "location": "Mumbai",
        "total_beds": 180,
        "icu_beds": 30
    }
]


@router.post(
    "/hospitals",
    response_model=HospitalResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_hospital(hospital: HospitalCreate):
    """
    Create a new hospital in the system

    Args:
        hospital: Hospital data including name, location, and bed capacity

    Returns:
        Created hospital with assigned ID
    """
    # Validate ICU beds don't exceed total beds
    if hospital.icu_beds > hospital.total_beds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ICU beds cannot exceed total beds"
        )

    new_hospital = hospital.model_dump()
    new_hospital["id"] = len(HOSPITALS_DB) + 1

    HOSPITALS_DB.append(new_hospital)
    return new_hospital


@router.get(
    "/hospitals",
    response_model=List[HospitalResponse]
)
async def get_hospitals(
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all hospitals with pagination

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List of hospitals
    """
    return HOSPITALS_DB[skip : skip + limit]


@router.get(
    "/hospitals/{hospital_id}",
    response_model=HospitalResponse
)
async def get_hospital(hospital_id: int):
    """
    Get specific hospital by ID

    Args:
        hospital_id: Hospital ID

    Returns:
        Hospital details

    Raises:
        404: Hospital not found
    """
    for hospital in HOSPITALS_DB:
        if hospital["id"] == hospital_id:
            return hospital

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Hospital with ID {hospital_id} not found"
    )
