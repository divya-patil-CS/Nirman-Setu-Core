"""
schemes_data.py
==================

This is where every scheme's data lives: its hard eligibility rule (the
AND/OR tree that evaluate_rule() checks), plus, for schemes that need it,
extra structured data that ISN'T a simple pass/fail:

    - "components"       : sub-benefits within one scheme, each with its own
                            minimum land requirement and amount. Component
                            amounts are NOT automatically added together.
    - "priority_factors"  : things that affect WHO GETS PICKED FIRST when a
                            scheme has limited slots, but do NOT disqualify
                            anyone who lacks them. These are informational,
                            never used to filter someone out.
    - "area_limits"       : per-division min/max land, used by
                            calculate_remaining_eligible_area() in
                            rule_engine.py for schemes where a previous
                            benefit shrinks (not blocks) how much area
                            still qualifies.
    - "*_note" / "*_policy" strings : plain-English flags for restrictions
                            that are too case-by-case to safely automate as
                            a hard True/False rule. These are never read by
                            evaluate_rule() — they exist so a human (or a
                            future, more detailed rule) can review that
                            specific case rather than the engine silently
                            guessing wrong.

IMPORTANT — new profile fields these two schemes need:
  Your existing profile dict (from the chatbot) doesn't yet have some
  fields these schemes check. You'll need to ask your teammate to add
  these to the chatbot's collected profile:

    agricultural_land_hectares   (number)
    aadhaar_available             (True/False)
    bank_account_linked_aadhaar   (True/False)
    beneficiary_type              ("individual" or "institutional")
    division                      ("konkan" or "other" — map any
                                    Maharashtra district into one of these
                                    two for now)

  Optional, only used for PRIORITY (never disqualifies anyone):
    farm_category                       ("small", "marginal", or "other")
    has_disability                      (True/False)
    family_livelihood_only_agriculture  (True/False)
    mgnregs_eligible                    (True/False) — informational only,
                                          see mgnregs_note below
    previous_benefit_area_hectares      (number) — for the Falbag scheme's
                                          remaining-area calculation
"""

SCHEMES = [
    # -----------------------------------------------------------------
    # Your original 3 example schemes — unchanged, kept here so
    # everything lives in one place now.
    # -----------------------------------------------------------------
    {
        "scheme_id": "farmer_income_scheme",
        "name": "Farmer Income Support Scheme",
        "deadline": "2026-12-31",
        "active": True,
        "rules": {
            "operator": "AND",
            "conditions": [
                {"field": "occupation", "op": "==", "value": "farmer"},
                {"field": "annual_income", "op": "<=", "value": 250000},
            ],
        },
    },
    {
        "scheme_id": "senior_citizen_pension",
        "name": "Senior Citizen Pension Scheme",
        "deadline": "2026-10-15",
        "active": True,
        "rules": {
            "operator": "AND",
            "conditions": [
                {"field": "age", "op": ">=", "value": 60},
                {"field": "annual_income", "op": "<=", "value": 300000},
            ],
        },
    },
    {
        "scheme_id": "rural_worker_scheme",
        "name": "Rural Worker Support Scheme",
        "deadline": "2026-11-30",
        "active": True,
        "rules": {
            "operator": "AND",
            "conditions": [
                {
                    "operator": "OR",
                    "conditions": [
                        {"field": "occupation", "op": "==", "value": "farmer"},
                        {"field": "occupation", "op": "==", "value": "laborer"},
                    ],
                },
                {"field": "annual_income", "op": "<=", "value": 200000},
            ],
        },
    },

    # -----------------------------------------------------------------
    # PRIMARY TEST SCHEME 1
    # Dr. Babasaheb Ambedkar Krushi Swavalamban Yojana (GR 2018-19)
    # -----------------------------------------------------------------
    {
        "scheme_id": "ambedkar_krushi_swavalamban",
        "name": "Dr. Babasaheb Ambedkar Krushi Swavalamban Yojana",
        "gr_version": "2018-19",
        "deadline": None,
        "active": True,

        # SCHEME-LEVEL hard eligibility — must ALL be true just to be
        # considered for ANY component of this scheme.
        "rules": {
            "operator": "AND",
            "conditions": [
                {"field": "caste", "op": "in", "value": ["SC", "Nav-Buddhist"]},
                {"field": "annual_income", "op": "<=", "value": 150000},
                {"field": "agricultural_land_hectares", "op": "<=", "value": 6},
                {"field": "aadhaar_available", "op": "==", "value": True},
                {"field": "bank_account_linked_aadhaar", "op": "==", "value": True},
            ],
        },

        "required_documents": [
            "caste_certificate",
            "aadhaar",
            "bank_account_linked_with_aadhaar",
            "7_12_land_extract",
            "8a_land_extract",
        ],

        # --------------------------------------------------------------
        # Per the actual GR (section 2, 2.1-2.4, 3.1-3.4, 6.1, 6.4):
        #
        # The 8 components form ONE package. Of "new_well",
        # "old_well_repair", and "plastic_lining_farm_pond", a
        # beneficiary may receive AT MOST ONE (package_group below) —
        # your UI should let the applicant choose one, not auto-grant
        # multiple. "pump_set", "electricity_connection",
        # "inwell_boring", "drip_irrigation", and "sprinkler_irrigation"
        # can accompany whichever of those three the applicant picked,
        # OR stand alone if the farmer already has a well (see
        # eligibility_rule on each below).
        #
        # New profile fields these components need (add to the
        # chatbot's collected profile):
        #   already_has_well               (True/False) - a well already
        #                                    exists on the 7/12 record or
        #                                    physically in the field
        #   received_well_assistance_before (True/False) - previously
        #                                    got a new-well or old-well-
        #                                    repair benefit from THIS or
        #                                    ANY other government scheme
        #   has_old_well_to_repair         (True/False) - only relevant
        #                                    if applying for old_well_repair
        #   completed_magel_tyala_shettale (True/False) - completed a
        #                                    farm pond under the separate
        #                                    Gram Vikas dept "Magel Tyala
        #                                    Shettale" scheme (required
        #                                    specifically for
        #                                    plastic_lining_farm_pond)
        # --------------------------------------------------------------
        "components": [
            {
                "component_id": "new_well",
                "name": "New Well",
                "min_land_hectares": 0.40,
                "amount_inr": 250000,
                "package_group": "well_or_pond_package",
                "eligibility_rule": {
                    "operator": "AND",
                    "conditions": [
                        {"field": "received_well_assistance_before", "op": "==", "value": False},
                        {"field": "already_has_well", "op": "==", "value": False},
                    ],
                },
            },
            {
                "component_id": "old_well_repair",
                "name": "Repair of Old Well",
                "min_land_hectares": 0.20,
                "amount_inr": 50000,
                "package_group": "well_or_pond_package",
                "eligibility_rule": {
                    "operator": "AND",
                    "conditions": [
                        {"field": "has_old_well_to_repair", "op": "==", "value": True},
                        {"field": "received_well_assistance_before", "op": "==", "value": False},
                    ],
                },
            },
            {
                "component_id": "plastic_lining_farm_pond",
                "name": "Plastic Lining of Farm Pond",
                "min_land_hectares": 0.20,
                "amount_inr": 100000,
                "package_group": "well_or_pond_package",
                "eligibility_rule": {
                    "operator": "AND",
                    "conditions": [
                        {"field": "completed_magel_tyala_shettale", "op": "==", "value": True},
                        {"field": "received_well_assistance_before", "op": "==", "value": False},
                    ],
                },
            },
            {
                "component_id": "inwell_boring",
                "name": "In-well Boring",
                "min_land_hectares": 0.20,
                "amount_inr": 20000,
                "package_group": "well_addon",
                "eligibility_rule": {
                    "operator": "OR",
                    "conditions": [
                        {"field": "already_has_well", "op": "==", "value": True},
                        {"field": "received_well_assistance_before", "op": "==", "value": False},
                    ],
                },
            },
            {
                "component_id": "pump_set",
                "name": "Pump Set",
                "min_land_hectares": 0.20,
                "amount_inr": 20000,
                "package_group": "well_addon",
                "eligibility_rule": {
                    "field": "already_has_well", "op": "==", "value": True,
                },
            },
            {
                "component_id": "electricity_connection",
                "name": "Electricity Connection",
                "min_land_hectares": 0.20,
                "amount_inr": 10000,
                "package_group": "well_addon",
                "eligibility_rule": {
                    "field": "already_has_well", "op": "==", "value": True,
                },
            },
            {
                "component_id": "drip_irrigation",
                "name": "Drip Irrigation",
                "min_land_hectares": 0.20,
                "amount_inr": 50000,
            },
            {
                "component_id": "sprinkler_irrigation",
                "name": "Sprinkler Irrigation",
                "min_land_hectares": 0.20,
                "amount_inr": 25000,
            },
        ],

        # Per GR section 2: the applicant picks ONE of new_well /
        # old_well_repair / plastic_lining_farm_pond (package_group
        # "well_or_pond_package" above) — this is an applicant CHOICE,
        # not something the engine should auto-decide. pump_set,
        # electricity_connection, and inwell_boring (package_group
        # "well_addon") ride along with whichever primary package is
        # chosen, or can be requested alone if the farmer already has a
        # well (section 6.4). Drip/sprinkler irrigation additionally
        # get co-funding from the separate PM Krishi Sinchan Yojana per
        # section 6.7 — that funding-split math is NOT modeled here,
        # only base eligibility.
        "package_notes": (
            "Beneficiary may receive at most ONE of: new_well, "
            "old_well_repair, plastic_lining_farm_pond (package_group "
            "'well_or_pond_package') — this is the applicant's choice. "
            "Component amounts are not additive across the whole scheme."
        ),
        "previous_benefit_policy": "encoded_via_received_well_assistance_before_field",
    },

    # -----------------------------------------------------------------
    # PRIMARY TEST SCHEME 2
    # Bhausaheb Fundkar Falbag Lagvad Yojana (GR 2018-19)
    # -----------------------------------------------------------------
    {
        "scheme_id": "bhausaheb_fundkar_falbag",
        "name": "Bhausaheb Fundkar Falbag Lagvad Yojana",
        "gr_version": "2018-19",
        "deadline": None,
        "active": True,

        "rules": {
            "operator": "AND",
            "conditions": [
                {"field": "beneficiary_type", "op": "==", "value": "individual"},
                {
                    "operator": "OR",
                    "conditions": [
                        {
                            "operator": "AND",
                            "conditions": [
                                {"field": "division", "op": "==", "value": "konkan"},
                                {"field": "agricultural_land_hectares", "op": ">=", "value": 0.10},
                                {"field": "agricultural_land_hectares", "op": "<=", "value": 10.00},
                            ],
                        },
                        {
                            "operator": "AND",
                            "conditions": [
                                {"field": "division", "op": "!=", "value": "konkan"},
                                {"field": "agricultural_land_hectares", "op": ">=", "value": 0.20},
                                {"field": "agricultural_land_hectares", "op": "<=", "value": 6.00},
                            ],
                        },
                    ],
                },
            ],
        },

        "required_documents": [
            "7_12_land_extract",
            "joint_holder_consent_if_applicable",
            "tenant_consent_if_applicable",
        ],

        # Used by calculate_remaining_eligible_area() in rule_engine.py.
        # Keep these numbers in sync with the "rules" tree above if you
        # ever change them — they're kept separate here so the remaining-
        # area math doesn't have to parse the rule tree itself.
        "area_limits": {
            "konkan": {"min": 0.10, "max": 10.00},
            "other": {"min": 0.20, "max": 6.00},
        },

        # A previous benefit under a related scheme REDUCES the eligible
        # area rather than blocking eligibility outright — see
        # calculate_remaining_eligible_area() in rule_engine.py.
        "previous_benefit_policy": "reduces_remaining_eligible_area",

        # Farmers eligible under MGNREGS are generally not meant to get
        # financial assistance here, EXCEPT for exceptions described in
        # paragraphs 7.3/7.4 of the referenced 6 July 2018 GR. That
        # exception is too case-specific to safely hardcode, so this is
        # NOT implemented as an automatic disqualifier — it's a flag for
        # manual review.
        "mgnregs_note": (
            "Farmers who are MGNREGS-eligible are generally excluded from "
            "financial assistance under this scheme, subject to exceptions "
            "in GR paragraphs 7.3/7.4 (6 July 2018 GR). Requires manual "
            "review — do not auto-disqualify on mgnregs_eligible=True."
        ),

        # PRIORITY factors: these affect selection order when applications
        # exceed the funded target. They NEVER disqualify anyone who lacks
        # them — get_priority_factors() in rule_engine.py only reports
        # which ones a profile matches, it never filters.
        "priority_factors": [
            {"field": "caste", "op": "in", "value": ["SC", "ST"], "label": "SC/ST farmer priority"},
            {"field": "farm_category", "op": "in", "value": ["small", "marginal"], "label": "Small/marginal farmer priority"},
            {"field": "gender", "op": "==", "value": "female", "label": "Woman farmer priority"},
            {"field": "has_disability", "op": "==", "value": True, "label": "Person with disability priority"},
            {
                "field": "family_livelihood_only_agriculture",
                "op": "==",
                "value": True,
                "label": "Family's livelihood depends only on agriculture (first priority)",
            },
        ],
    },
]