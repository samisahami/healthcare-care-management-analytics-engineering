with members as (

    select *
    from {{ ref('stg_members') }}

),

engagement as (

    select *
    from {{ ref('int_member_engagement_rollup') }}

),

Utilization as (

    select *
    from {{ ref('int_member_monthly_utilization') }}

),

current_utilization as (

    select *
    from utilization
    qualify row_number() over (
        partition by member_id
        order by service_month desc
    ) = 1
),

final as (

    select
        m.member_id,
        m.first_name,
        m.last_name,
        m.gender,
        m.state,
        m.employer_group,
        m.risk_level,
        m.chronic_condition_flag,

        coalesce(e.total_interactions, 0) as total_interactions,
        coalesce(e.successful_interactions, 0) as successful_interactions,
        e.last_interaction_date,
        coalesce(e.engagement_status, 'Not Engaged') as engagement_status,

        cu.service_month,
        coalesce(cu.total_claims, 0) as total_claims,
        coalesce(cu.total_allowed_amount, 0) as total_allowed_amount,
        coalesce(cu.total_paid_amount, 0) as total_paid_amount,
        coalesce(cu.ip_claims, 0) as ip_claims,
        coalesce(cu.er_claims, 0) as er_claims,
        coalesce(cu.op_claims, 0) as op_claims,
        coalesce(cu.rx_claims, 0) as rx_claims,

        case
            when m.risk_level = 'High'
                 and coalesce(e.engagement_status, 'Not Engaged') = 'Not Engaged'
                 and coalesce(cu.total_allowed_amount, 0) >= 1000
                then 'High Priority'

            when m.risk_level in ('Medium', 'High')
                 and coalesce(e.engagement_status, 'Not Engaged') = 'Not Engaged'
                then 'Medium Priority'

            else 'Low Priority'
        end as outreach_priority

    from members m
    left join engagement e
        on m.member_id = e.member_id
    left join current_utilization cu
        on m.member_id = cu.member_id

)

select *
from final