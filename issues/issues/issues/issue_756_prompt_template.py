"""
Code Name: prompt_template_secondary_knowledge
File: issues/issue_756_prompt_template.py

This script defines prompt templates that inject secondary knowledge
before the main text is fed into the model.
"""

from typing import Dict

class PromptTemplate:
    def __init__(self, secondary_knowledge: str, rules: Dict[str, str]):
        """
        :param secondary_knowledge: Knowledge to prepend to the main text
        :param rules: Dict defining rules that the output must follow
        """
        self.secondary_knowledge = secondary_knowledge
        self.rules = rules

    def generate_prompt(self, main_text: str) -> str:
        """
        Combine secondary knowledge with main text to create the final prompt.
        """
        prompt = f"Knowledge:\n{self.secondary_knowledge}\n\nText:\n{main_text}\n\nRules:\n"
        for rule_name, rule_desc in self.rules.items():
            prompt += f"- {rule_name}: {rule_desc}\n"
        prompt += "\nPlease generate output following the above rules."
        return prompt


# Example usage
if __name__ == "__main__":
    secondary_knowledge = "Python data structures include lists, dictionaries, and sets."
    rules = {
        "Format": "Use bullet points",
        "Length": "No more than 100 words",
        "Accuracy": "Do not invent facts"
    }

    template = PromptTemplate(secondary_knowledge, rules)
    main_text = "Explain how to use lists in Python for beginners."
    final_prompt = template.generate_prompt(main_text)

    print("Generated Prompt:")
    print(final_prompt)
