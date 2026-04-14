# EuroPolicy Agent - 后端国际化映射资源
# 支持: en, zh, fr, de

OPPORTUNITY_TRANSLATIONS = {
    "en": {
        "Capital Grant": "Capital Grant",
        "Tax Exemption": "Tax Exemption",
        "Green Loan": "Green Loan",
        "Heavy Industry": "Heavy Industry",
        "Energy Storage": "Energy Storage",
        "Hydropower": "Hydropower",
        "urgency_high": "High",
        "urgency_medium": "Medium",
        "urgency_low": "Low"
    },
    "zh": {
        "Capital Grant": "资本拨款",
        "Tax Exemption": "免税/税收抵免",
        "Green Loan": "绿色贷款",
        "Heavy Industry": "重工业",
        "Energy Storage": "储能行业",
        "Hydropower": "水电项目",
        "urgency_high": "极高",
        "urgency_medium": "中等",
        "urgency_low": "较低"
    },
    "fr": {
        "Capital Grant": "Subvention de Capital",
        "Tax Exemption": "Exonération Fiscale",
        "Green Loan": "Prêt Vert",
        "Heavy Industry": "Industrie Lourde",
        "Energy Storage": "Stockage d'Énergie",
        "Hydropower": "Hydroélectricité",
        "urgency_high": "Élevée",
        "urgency_medium": "Moyenne",
        "urgency_low": "Faible"
    },
    "de": {
        "Capital Grant": "Investitionszuschuss",
        "Tax Exemption": "Steuerbefreiung",
        "Green Loan": "Grüner Kredit",
        "Heavy Industry": "Schwerindustrie",
        "Energy Storage": "Energiespeicherung",
        "Hydropower": "Wasserkraft",
        "urgency_high": "Hoch",
        "urgency_medium": "Mittel",
        "urgency_low": "Niedrig"
    }
}

# 各语言的默认获客查询模板
OPPORTUNITY_QUERIES = {
    "en": "What are the specific subsidies, compliance deadlines, and sales opportunities for energy companies under EU RED III (Directive 2023/2413) and CBAM (Regulation 2023/956) in 2026? Focus on hydrogen, renewable energy, and heavy industry sectors.",
    "zh": "欧盟 RED III（指令 2023/2413）和 CBAM（法规 2023/956）在 2026 年对能源企业有哪些具体的补贴、合规截止日期和销售机会？重点关注氢能、可再生能源和重工业领域。",
    "fr": "Quelles sont les subventions, les délais de conformité et les opportunités commerciales spécifiques pour les entreprises énergétiques dans le cadre du RED III (Directive 2023/2413) et du CBAM (Règlement 2023/956) en 2026 ? Concentrez-vous sur l'hydrogène, les énergies renouvelables et l'industrie lourde.",
    "de": "Welche spezifischen Subventionen, Compliance-Fristen und Verkaufschancen gibt es für Energieunternehmen unter der EU RED III (Richtlinie 2023/2413) und dem CBAM (Verordnung 2023/956) im Jahr 2026? Fokus auf Wasserstoff, erneuerbare Energien und Schwerindustrie.",
}

def get_localized_value(key: str, lang: str, category: str = "en") -> str:
    """
    通用本地化获取函数
    """
    return OPPORTUNITY_TRANSLATIONS.get(lang, OPPORTUNITY_TRANSLATIONS["en"]).get(key, key)
