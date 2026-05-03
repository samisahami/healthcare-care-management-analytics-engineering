with outreach_priority as (

    select *
    from {{ ref('mart_member_outreach_priority') }}

),

final as (

    select
        employer_group,
        risk_level,
        engagement_status,
        outreach_priority,

        count(*) as member_count,
        sum(total_interactions) as total_interactions,
        sum(successful_interactions) as successful_interactions,
        sum(total_claims) as total_claims,
        sum(total_allowed_amount) as total_allowed_amount,
        sum(total_paid_amount) as total_paid_amount,
        sum(ip_claims) as ip_claims,
        sum(er_claims) as er_claims,

        round(
            sum(successful_interactions) / nullif(sum(total_interactions), 0),
            4
        ) as interaction_success_rate,

        round(
            sum(total_allowed_amount) / nullif(count(*), 0),
            2
        ) as allowed_amount_per_member

    from outreach_priority
    group by
        employer_group,
        risk_level,
        engagement_status,
        outreach_priority

)

select *
from final