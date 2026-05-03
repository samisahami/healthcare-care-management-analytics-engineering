import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

NUM_MEMBERS = 1000
NUM_CLAIMS = 10000
NUM_INTERACTIONS = 5000
NUM_EPISODES = 1500

def generate_members(num_members):
    members = []

    for i in range(1, num_members + 1):
        members.append({
            "member_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=90),
            "gender": random.choice(["M", "F"]),
            "state": random.choice(["FL", "TX", "GA", "NC", "CA"]),
            "employer_group": random.choice([
                "Rosen Hotels",
                "Lee Health",
                "Baptist Health",
                "Advent Health"
            ]),
            "risk_level": random.choice(["Low", "Medium", "High"]),
            "chronic_condition_flag": random.choice([0, 1])
        })

    return pd.DataFrame(members)


def generate_eligibility(members_df):
    eligibility = []

    plan_names = ["HMO Basic", "PPO Standard", "HDHP Saver", "Gold Plus"]

    for _, row in members_df.iterrows():
        coverage_start = fake.date_between(start_date="-2y", end_date="-6m")
        active_flag = random.choice([0, 1])

        if active_flag == 1:
            coverage_end = None
        else:
            coverage_end = fake.date_between(start_date=coverage_start, end_date="today")

        eligibility.append({
            "eligibility_id": f"E{row['member_id']:06d}",
            "member_id": row["member_id"],
            "plan_name": random.choice(plan_names),
            "coverage_start": coverage_start,
            "coverage_end": coverage_end,
            "active_flag": active_flag
        })

    return pd.DataFrame(eligibility)

def generate_claims(members_df, eligibility_df, num_claims):
    claims = []

    claim_types = ["IP", "OP", "ER", "RX"]
    place_of_service_map = {
        "IP": "Inpatient Hospital",
        "OP": "Outpatient Hospital",
        "ER": "Emergency Room",
        "RX": "Pharmacy"
    }

    diagnosis_codes = [
        "E11.9",   # Type 2 diabetes
        "I10",     # Hypertension
        "J45.909", # Asthma
        "F32.A",   # Depression
        "M54.50",  # Low back pain
        "E78.5",   # Hyperlipidemia
        "Z00.00",  # General exam
        "N39.0"    # UTI
    ]

    procedure_codes = [
        "99213",   # office visit
        "99214",
        "93000",   # EKG
        "80053",   # metabolic panel
        "70450",   # CT head
        "71046",   # chest xray
        "A0429",   # ambulance
        "J3490"    # unclassified drug
    ]

    for i in range(1, num_claims + 1):
        member_row = members_df.sample(1).iloc[0]
        member_id = member_row["member_id"]

        elig_row = eligibility_df[eligibility_df["member_id"] == member_id].iloc[0]
        coverage_start = pd.to_datetime(elig_row["coverage_start"])

        if pd.isna(elig_row["coverage_end"]):
            coverage_end = pd.Timestamp.today()
        else:
            coverage_end = pd.to_datetime(elig_row["coverage_end"])

        if coverage_start >= coverage_end:
            service_date = coverage_start
        else:
            date_range_days = (coverage_end - coverage_start).days
            random_offset = random.randint(0, max(date_range_days, 0))
            service_date = coverage_start + pd.Timedelta(days=random_offset)

        claim_type = random.choices(
            claim_types,
            weights=[0.10, 0.45, 0.20, 0.25],
            k=1
        )[0]

        if claim_type == "IP":
            allowed_amount = round(random.uniform(5000, 50000), 2)
        elif claim_type == "ER":
            allowed_amount = round(random.uniform(500, 5000), 2)
        elif claim_type == "OP":
            allowed_amount = round(random.uniform(150, 3000), 2)
        else:  # RX
            allowed_amount = round(random.uniform(20, 800), 2)

        paid_amount = round(allowed_amount * random.uniform(0.7, 1.0), 2)

        claims.append({
            "claim_id": f"C{i:07d}",
            "member_id": member_id,
            "service_date": service_date.date(),
            "claim_type": claim_type,
            "allowed_amount": allowed_amount,
            "paid_amount": paid_amount,
            "diagnosis_code": random.choice(diagnosis_codes),
            "procedure_code": random.choice(procedure_codes),
            "provider_id": f"P{random.randint(1, 250):04d}",
            "facility_id": f"F{random.randint(1, 75):03d}",
            "place_of_service": place_of_service_map[claim_type]
        })

    return pd.DataFrame(claims)

def generate_interactions(members_df, num_interactions):
    interactions = []

    interaction_types = [
        "Call",
        "Email",
        "SMS",
        "Care Manager Outreach"
    ]

    interaction_statuses = [
        "Successful",
        "Attempted",
        "Failed",
        "No Response"
    ]

    outreach_channels = [
        "Phone",
        "Email",
        "Text"
    ]

    for i in range(1, num_interactions + 1):
        member_row = members_df.sample(1).iloc[0]
        member_id = member_row["member_id"]

        interaction_date = fake.date_between(start_date="-1y", end_date="today")

        interactions.append({
            "interaction_id": f"I{i:07d}",
            "member_id": member_id,
            "interaction_date": interaction_date,
            "interaction_type": random.choice(interaction_types),
            "interaction_status": random.choice(interaction_statuses),
            "outreach_channel": random.choice(outreach_channels)
        })

    return pd.DataFrame(interactions)

def generate_care_management_episodes(members_df, num_episodes):
    episodes = []

    program_types = [
        "Case Management",
        "Disease Management",
        "Maternity",
        "Behavioral Health",
        "High Risk"
    ]

    episode_statuses = [
        "Open",
        "Closed",
        "Completed",
        "Unable to Reach"
    ]

    case_managers = [
        "Alice Johnson",
        "Brian Smith",
        "Carla Davis",
        "Daniel Lopez",
        "Emily Chen",
        "Fatima Khan"
    ]

    for i in range(1, num_episodes + 1):
        member_row = members_df.sample(1).iloc[0]
        member_id = member_row["member_id"]

        episode_start = fake.date_between(start_date="-1y", end_date="-30d")
        episode_status = random.choice(episode_statuses)

        if episode_status == "Open":
            episode_end = None
        else:
            episode_end = fake.date_between(start_date=episode_start, end_date="today")

        episodes.append({
            "episode_id": f"EP{i:07d}",
            "member_id": member_id,
            "program_type": random.choice(program_types),
            "episode_start": episode_start,
            "episode_end": episode_end,
            "episode_status": episode_status,
            "case_manager": random.choice(case_managers)
        })

    return pd.DataFrame(episodes)


if __name__ == "__main__":
    members_df = generate_members(NUM_MEMBERS)
    eligibility_df = generate_eligibility(members_df)
    claims_df = generate_claims(members_df, eligibility_df, NUM_CLAIMS)
    interactions_df = generate_interactions(members_df, NUM_INTERACTIONS)
    episodes_df = generate_care_management_episodes(members_df, NUM_EPISODES)

    members_df.to_csv("data/raw/members.csv", index=False)
    eligibility_df.to_csv("data/raw/eligibility.csv", index=False)
    claims_df.to_csv("data/raw/claims.csv", index=False)
    interactions_df.to_csv("data/raw/interactions.csv", index=False)
    episodes_df.to_csv("data/raw/care_management_episodes.csv", index=False)

    print("Members dataset generated successfully.")
    print("Eligibility dataset generated successfully.")
    print("Claims dataset generated successfully.")
    print("Interactions dataset generated successfully.")
    print("Care management episodes dataset generated successfully.")