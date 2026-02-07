"""Domain knowledge for German income tax prep (non-authoritative, no filing)."""

from __future__ import annotations

DEDUCTION_CATALOG: list[dict] = [
    {
        "id": "employment_expenses",
        "name": "Employment expenses (Werbungskosten)",
        "summary": "Costs that are directly related to your job.",
        "applies_if": [{"field": "employment_type", "values": ["employee", "public_servant"]}],
        "items": [
            "Commuting to work (distance-based commuting costs)",
            "Home office or dedicated workroom costs",
            "Work equipment (laptop, desk, chair, tools)",
            "Professional training, certifications, courses",
            "Business travel costs (transport, meals, accommodation)",
            "Job application costs and interview travel",
            "Relocation costs due to job change",
            "Union or professional association fees",
            "Work-related phone and internet usage",
            "Double household costs (if maintaining a second household for work)",
        ],
        "questions": [
            "Did you commute regularly and how?",
            "Did you work from home or have a dedicated workroom?",
            "Did you buy work equipment or software?",
            "Any professional training or certifications?",
            "Any work travel or interviews?",
        ],
        "documents": [
            "Employer wage statement (Lohnsteuerbescheinigung)",
            "Receipts for work equipment and training",
            "Travel tickets, invoices, mileage logs",
            "Home office utility/lease evidence if applicable",
        ],
    },
    {
        "id": "self_employed",
        "name": "Self-employment and freelance expenses",
        "summary": "Business expenses and income for freelancers and self-employed individuals.",
        "applies_if": [{"field": "employment_type", "values": ["self_employed", "freelancer"]}],
        "items": [
            "Business travel and client meetings",
            "Office space and equipment",
            "Software subscriptions and services",
            "Professional liability insurance",
            "Marketing, website, and advertising costs",
            "Accounting and advisory fees",
        ],
        "questions": [
            "What income sources and clients did you have?",
            "Which business expenses did you incur?",
            "Do you have invoices, contracts, and receipts?",
        ],
        "documents": [
            "Invoices issued and received",
            "Business bank statements",
            "Receipts and contracts",
            "Insurance statements",
        ],
    },
    {
        "id": "rental_income",
        "name": "Rental income expenses (Vermietung und Verpachtung)",
        "summary": "Costs related to rental property income.",
        "applies_if": [{"field": "has_rental_property", "values": [True]}],
        "items": [
            "Maintenance and repair costs",
            "Property management fees",
            "Mortgage interest (if applicable)",
            "Insurance for the property",
            "Depreciation (AfA) where eligible",
        ],
        "questions": [
            "Do you own and rent out property?",
            "Any repairs or renovation costs?",
            "Do you have mortgage interest statements?",
        ],
        "documents": [
            "Rental income statements",
            "Repair and maintenance invoices",
            "Mortgage interest statements",
            "Insurance policies",
        ],
    },
    {
        "id": "special_expenses",
        "name": "Special expenses (Sonderausgaben)",
        "summary": "Payments that can reduce taxable income.",
        "applies_if": [],
        "items": [
            "Health, nursing care, and unemployment insurance contributions",
            "Pension and retirement contributions",
            "Donations to eligible organizations",
            "Church tax (if applicable)",
            "Alimony payments (subject to conditions)",
        ],
        "questions": [
            "Which insurance or pension contributions did you pay?",
            "Did you make donations or pay church tax?",
            "Did you pay alimony or support payments?",
        ],
        "documents": [
            "Annual insurance contribution statements",
            "Donation receipts",
            "Church tax statements (if applicable)",
            "Alimony agreements and payment evidence",
        ],
    },
    {
        "id": "extraordinary_burdens",
        "name": "Extraordinary burdens (Außergewöhnliche Belastungen)",
        "summary": "Unavoidable costs like medical or care expenses.",
        "applies_if": [],
        "items": [
            "Medical treatments and prescriptions",
            "Care costs for dependents",
            "Disability-related expenses",
            "Necessary home adaptations for disability",
        ],
        "questions": [
            "Did you incur significant medical or care costs?",
            "Are there disability-related expenses to report?",
        ],
        "documents": [
            "Medical invoices and prescriptions",
            "Care service invoices",
            "Disability certificates",
        ],
    },
    {
        "id": "childcare",
        "name": "Child-related reliefs",
        "summary": "Childcare costs and related benefits.",
        "applies_if": [{"field": "has_children", "values": [True]}],
        "items": [
            "Childcare costs (daycare, nanny, after-school care)",
            "Education-related costs where eligible",
            "Child allowance and related reliefs",
        ],
        "questions": [
            "Did you pay for childcare or daycare?",
            "Do you have invoices or contracts for childcare services?",
        ],
        "documents": [
            "Childcare invoices and contracts",
            "Proof of payment",
        ],
    },
    {
        "id": "household_services",
        "name": "Household services and craftspeople",
        "summary": "Eligible household services and renovation work.",
        "applies_if": [],
        "items": [
            "Domestic services (cleaning, gardening, care)",
            "Craftspeople services and renovations (labor portion)",
        ],
        "questions": [
            "Did you pay for household services or repairs at home?",
            "Do you have invoices with labor costs separated?",
        ],
        "documents": [
            "Invoices for household services",
            "Craftspeople invoices with labor costs",
            "Bank transfer confirmations",
        ],
    },
    {
        "id": "education",
        "name": "Education and training",
        "summary": "Costs for studies or professional training.",
        "applies_if": [],
        "items": [
            "Tuition and course fees",
            "Study materials and equipment",
            "Travel to education facilities",
        ],
        "questions": [
            "Did you study or take professional courses?",
            "Any tuition, course, or exam fees?",
        ],
        "documents": [
            "Course and tuition invoices",
            "Receipts for materials",
        ],
    },
    {
        "id": "capital_income",
        "name": "Capital income considerations",
        "summary": "Bank fees, investment-related costs, and losses.",
        "applies_if": [{"field": "has_investments", "values": [True]}],
        "items": [
            "Investment-related fees",
            "Losses that might be reportable",
            "Foreign withholding taxes (if applicable)",
        ],
        "questions": [
            "Do you have investment accounts or capital income?",
            "Any foreign dividends or withholding taxes?",
        ],
        "documents": [
            "Annual bank tax statement (Jahressteuerbescheinigung)",
            "Broker statements",
        ],
    },
    {
        "id": "relocation",
        "name": "Relocation and double household",
        "summary": "Moving costs or maintaining a second household for work.",
        "applies_if": [],
        "items": [
            "Relocation costs due to job change",
            "Second household costs for work",
        ],
        "questions": [
            "Did you move for work or keep a second household?",
            "Any relocation invoices or rental contracts?",
        ],
        "documents": [
            "Relocation invoices",
            "Rental contracts and travel logs",
        ],
    },
]

QUESTION_BANK: list[dict] = [
    {"field": "tax_year", "question": "Which tax year are you preparing for?"},
    {
        "field": "residency",
        "question": "Were you a German tax resident for the full tax year?",
    },
    {"field": "employment_type", "question": "Employment type: employee, freelancer, or self-employed?"},
    {
        "field": "income_sources",
        "question": "Which income sources did you have (employment, freelance, rental, capital)?",
    },
    {"field": "marital_status", "question": "What was your marital status during the tax year?"},
    {"field": "has_children", "question": "Do you have dependent children in the tax year?"},
    {
        "field": "has_rental_property",
        "question": "Did you have rental property income during the tax year?",
    },
    {
        "field": "has_investments",
        "question": "Did you have investment accounts or capital income?",
    },
    {"field": "home_office", "question": "Did you work from home or have a dedicated workroom?"},
    {"field": "commute", "question": "How did you commute to work and how often?"},
    {
        "field": "education_or_training",
        "question": "Did you pay for professional training or education?",
    },
    {"field": "donations", "question": "Did you make donations to eligible organizations?"},
    {"field": "medical_costs", "question": "Any significant medical or care costs?"},
    {
        "field": "household_services",
        "question": "Did you pay for household services or repair work at home?",
    },
    {
        "field": "childcare_costs",
        "question": "Did you pay for childcare (daycare, nanny, after-school care)?",
    },
    {"field": "church_tax", "question": "Did you pay church tax in the tax year?"},
]

BASE_DOCUMENTS: list[str] = [
    "Tax ID and personal details (kept locally, never shared with third parties)",
    "Employer wage statement (Lohnsteuerbescheinigung) if employed",
    "Bank account IBAN for refunds",
    "Annual insurance contribution statements",
]
