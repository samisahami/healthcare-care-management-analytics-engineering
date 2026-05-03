with claims_base as (
    SELECT
        member_id,
        date_trunc('month', service_date) as service_month,
        claim_id,
        claim_type,
        allowed_amount,
        paid_amount
    FROM {{ ref('stg_claims') }}

    ),

    monthly_summary as (
        select
    member_id,
    service_month,
    count(*) as total_claims,
    sum(allowed_amount) as total_allowed_amount,
    sum(paid_amount) as total_paid_amount,
    sum(case when claim_type = 'IP' then 1 else 0 end) as ip_claims,
    sum(case when claim_type = 'ER' then 1 else 0 end) as er_claims,
    sum(case when claim_type = 'OP' then 1 else 0 end) as op_claims,
    sum(case when claim_type = 'RX' then 1 else 0 end) as rx_claims
        from claims_base
        group by member_id, service_month
    )

    select *
    from monthly_summary