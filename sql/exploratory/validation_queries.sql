-- Validate raw source row counts
select 'members' as table_name, count(*) as row_count from healthcare_cm_db.raw.members
union all
select 'eligibility', count(*) from healthcare_cm_db.raw.eligibility
union all
select 'claims', count(*) from healthcare_cm_db.raw.claims
union all
select 'interactions', count(*) from healthcare_cm_db.raw.interactions
union all
select 'care_management_episodes', count(*) from healthcare_cm_db.raw.care_management_episodes;


-- Validate final outreach priority distribution
select
    outreach_priority,
    count(*) as member_count
from healthcare_cm_db.analytics.mart_member_outreach_priority
group by outreach_priority
order by member_count desc;


-- Validate engagement status distribution
select
    engagement_status,
    count(*) as member_count
from healthcare_cm_db.analytics.mart_member_outreach_priority
group by engagement_status;


-- Validate utilization by outreach priority
select
    outreach_priority,
    count(*) as member_count,
    round(avg(total_allowed_amount), 2) as avg_allowed_amount,
    round(avg(total_paid_amount), 2) as avg_paid_amount,
    sum(ip_claims) as total_ip_claims,
    sum(er_claims) as total_er_claims
from healthcare_cm_db.analytics.mart_member_outreach_priority
group by outreach_priority
order by avg_allowed_amount desc;