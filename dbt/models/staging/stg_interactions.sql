select
    interaction_id,
    member_id,
    interaction_date,
    interaction_type,
    interaction_status,
    outreach_channel
from {{ source('healthcare_raw', 'interactions') }}