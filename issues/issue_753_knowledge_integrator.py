"""
Code Name: knowledge_integrator
File: issues/issue_753_knowledge_integrator.py

This script integrates LM output with secondary knowledge
to produce more accurate analysis and flag deviations from rules.
"""

from typing import Dict, List

class KnowledgeIntegrator:
    def __init__(self, secondary_knowledge: str, rules: Dict[str, str]):
        """
        :param secondary_knowledge: Background knowledge to integrate with LM output
        :param rules: Rules that the output must follow
        """
        self.secondary_knowledge = secondary_knowledge
        self.rules = rules

    def analyze(self, lm_output: str) -> Dict[str, str]:
        """
        Integrate LM output with secondary knowledge and check for rule violations.
        Returns analysis and warnings if any rule is violated.
        """
        analysis = f"Integrated Analysis:\n{lm_output}\n\nKnowledge:\n{self.secondary_knowledge}"
        warnings = []

        # Simple rule check simulation
        for rule_name, rule_desc in self.rules.items():
            if rule_desc.lower() not in lm_output.lower():
                warnings.append(f"Rule '{rule_name}' violated!")

        return {
            "analysis": analysis,
            "warnings": warnings
        }

# Example usage
if __name__ == "__main__":
    secondary_knowledge = "Data analysis should always validate assumptions."
    rules = {
        "Validate Assumptions": "validate assumptions",
        "Use correct units": "correct units"
    }

    integrator = KnowledgeIntegrator(secondary_knowledge, rules)
    lm_output = "The analysis was performed without checking the assumptions."

    result = integrator.analyze(lm_output)
    print("Analysis Result:")
    print(result["analysis"])
    print("Warnings:")
for w in result["warnings"]:
        print(f"- {w}")
