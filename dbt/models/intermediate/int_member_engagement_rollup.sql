with interaction_summary as (

    select
        member_id,
        count(*) as total_interactions,
        sum(case when interaction_status = 'Successful' then 1 else 0 end) as successful_interactions,
        max(interaction_date) as last_interaction_date
    from {{ ref('stg_interactions') }}
    group by member_id

),

final as (

    select
        member_id,
        total_interactions,
        successful_interactions,
        last_interaction_date,
        case
            when successful_interactions > 0 then 'Engaged'
            else 'Not Engaged'
        end as engagement_status
    from interaction_summary

)

select *
from final