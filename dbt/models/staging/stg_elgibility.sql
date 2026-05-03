select
    eligibility_id,
    member_id,
    plan_name,
    coverage_start,
    coverage_end,
    active_flag
from {{ source('healthcare_raw', 'eligibility') }}