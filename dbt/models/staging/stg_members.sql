select
    member_id,
    first_name,
    last_name,
    dob,
    gender,
    state,
    employer_group,
    risk_level,
    chronic_condition_flag
from {{ source('healthcare_raw', 'members') }}