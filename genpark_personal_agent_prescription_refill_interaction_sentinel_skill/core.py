# -*- coding: utf-8 -*-
"""Prescription Refill & Drug Interaction Sentinel Skill for GenPark Personal Health Agents."""
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Known clinical high-risk interaction matrix
CONTRAINDICATED_PAIRS = [
    {
        "drugs": {"warfarin", "aspirin"},
        "severity": "CRITICAL",
        "risk": "Additive anticoagulant effect; substantially elevated major hemorrhage / bleeding risk."
    },
    {
        "drugs": {"lisinopril", "potassium"},
        "severity": "HIGH",
        "risk": "Risk of severe hyperkalemia leading to cardiac arrhythmias."
    },
    {
        "drugs": {"fluoxetine", "selegiline"},
        "severity": "CRITICAL",
        "risk": "Serotonin syndrome risk; potentially life-threatening hyperthermia and neuromuscular excitation."
    },
    {
        "drugs": {"atorvastatin", "clarithromycin"},
        "severity": "HIGH",
        "risk": "CYP3A4 inhibition increases statin systemic exposure, elevating rhabdomyolysis and myopathy risk."
    },
    {
        "drugs": {"metformin", "contrast_dye"},
        "severity": "HIGH",
        "risk": "Lactic acidosis risk; withhold metformin prior to iodinated radiocontrast procedures."
    }
]

def track_medication_refill_burn_rate(medication_name: str, pills_remaining: int, doses_per_day: int, pills_per_dose: int = 1, pharmacy_processing_lead_days: int = 4) -> Dict[str, Any]:
    daily_consumption = doses_per_day * pills_per_dose
    if daily_consumption <= 0:
        return {"error": "daily consumption must be at least 1"}

    days_remaining = int(pills_remaining / daily_consumption)
    now = datetime.now()
    depletion_date = now + timedelta(days=days_remaining)
    refill_trigger_date = depletion_date - timedelta(days=pharmacy_processing_lead_days)

    is_urgent_refill = days_remaining <= pharmacy_processing_lead_days

    return {
        "medication_name": medication_name,
        "pills_remaining": pills_remaining,
        "daily_burn_pills": daily_consumption,
        "days_supply_remaining": days_remaining,
        "projected_depletion_date": depletion_date.strftime("%Y-%m-%d"),
        "recommended_refill_dispatch_date": refill_trigger_date.strftime("%Y-%m-%d"),
        "refill_status": "URGENT_DISPATCH_NOW" if is_urgent_refill else "SUFFICIENT_BUFFER",
        "requires_pharmacy_dispatch": is_urgent_refill,
        "clinical_note": "Ensure continuous uninterrupted adherence for chronic medications."
    }

def cross_check_drug_interactions(current_medications: List[str], prospective_medication: str) -> Dict[str, Any]:
    prospective_clean = prospective_medication.strip().lower()
    current_clean = [m.strip().lower() for m in current_medications]
    
    detected_conflicts = []
    
    for conflict in CONTRAINDICATED_PAIRS:
        pair = conflict["drugs"]
        if prospective_clean in pair:
            for active in current_clean:
                if active in pair and active != prospective_clean:
                    detected_conflicts.append({
                        "drug_a": prospective_clean,
                        "drug_b": active,
                        "severity": conflict["severity"],
                        "clinical_risk_description": conflict["risk"]
                    })

    has_critical = any(c["severity"] == "CRITICAL" for c in detected_conflicts)
    has_high = any(c["severity"] == "HIGH" for c in detected_conflicts)

    if has_critical:
        status = "CONTRAINDICATED_BLOCK"
    elif has_high:
        status = "REQUIRES_PHYSICIAN_OVERRIDE"
    else:
        status = "NO_KNOWN_MAJOR_CONTRAINDICATIONS"

    return {
        "prospective_medication": prospective_medication,
        "screened_medication_count": len(current_medications),
        "safety_clearance_status": status,
        "conflicts_found": detected_conflicts,
        "guidance": "Always confirm pharmacological alterations with licensed clinical prescribing physician."
    }
