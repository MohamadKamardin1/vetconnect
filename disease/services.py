from disease.models import DiseaseRule


def assess_disease(*, species_code, inputs):
    required = {"age", "location", "symptoms", "onset_days", "severity", "vaccination", "exposure"}
    missing = sorted(required - set(inputs))
    if missing:
        return None, {"status": "INVALID", "missing_inputs": missing, "message": "Required assessment inputs are missing."}
    symptoms = inputs.get("symptoms")
    if not isinstance(symptoms, list) or not symptoms:
        return None, {"status": "INVALID", "message": "symptoms must be a non-empty list."}
    rule = DiseaseRule.objects.filter(species_code=species_code, is_active=True).order_by("-version").first()
    if not rule:
        return None, {"status": "MISSING_CONFIGURATION", "message": "No verified disease decision-support rule is configured for this species."}
    high_risk = sorted(set(symptoms) & set(rule.high_risk_symptoms))
    scores = {name: sum(float(rule.symptom_weights.get(symptom, {}).get(name, 0)) for symptom in symptoms) for name in {name for value in rule.symptom_weights.values() for name in value}}
    ranked = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[:3]
    urgent = bool(high_risk) or inputs.get("severity") in {"SEVERE", "CRITICAL"}
    return rule, {"status": "COMPLETED", "possible_conditions": [{"name": name, "score": score} for name, score in ranked], "urgency": "EMERGENCY" if urgent else "ROUTINE", "referral_required": urgent, "high_risk_symptoms": high_risk, "disclaimer": rule.disclaimer, "version": rule.version}
