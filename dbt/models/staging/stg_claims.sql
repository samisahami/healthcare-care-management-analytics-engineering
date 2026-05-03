select
    claim_id,
    member_id,
    service_date,
    claim_type,
    allowed_amount,
    paid_amount,
    diagnosis_code,
    procedure_code,
    provider_id,
    facility_id,
    place_of_service
from {{ source('healthcare_raw', 'claims') }}