select
    episode_id,
    member_id,
    program_type,
    episode_start,
    episode_end,
    episode_status,
    case_manager
from {{ source('healthcare_raw', 'care_management_episodes') }}