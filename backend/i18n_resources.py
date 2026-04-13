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

def get_localized_value(key: str, lang: str, category: str = "en") -> str:
    """
    通用本地化获取函数
    """
    return OPPORTUNITY_TRANSLATIONS.get(lang, OPPORTUNITY_TRANSLATIONS["en"]).get(key, key)
