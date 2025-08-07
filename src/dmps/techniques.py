"""
4-D optimization techniques implementation.
"""

import re
from typing import Final


class OptimizationTechniques:
    """4-D methodology implementation: Deconstruct, Develop, Design, Deliver"""

    # Supported platforms and techniques
    ALLOWED_PLATFORMS: Final = frozenset({"claude", "chatgpt", "gemini", "generic"})
    ALLOWED_TECHNIQUES: Final = frozenset(
        {"develop_clarity", "design_structure", "deliver_format"}
    )

    # Compiled patterns for performance
    _CONTEXT_KEYWORDS = re.compile(r"context|background|requirements", re.IGNORECASE)
    _FORMAT_KEYWORDS = re.compile(r"format|structure|organize", re.IGNORECASE)
    _WHITESPACE_CLEANER = re.compile(r"\s+")

    def develop_clarity(self, prompt: str, intent: str) -> str:
        """Step 1: Develop clarity by removing vague terms and adding context"""
        enhanced_prompt = prompt

        # Add technical context if missing
        if intent == "technical" and not self._CONTEXT_KEYWORDS.search(enhanced_prompt):
            enhanced_prompt = f"Context: {enhanced_prompt}"

        # Replace vague terms with specific alternatives
        vague_term_replacements = [
            (re.compile(r"\bsomething\b", re.IGNORECASE), "a specific item"),
            (re.compile(r"\banything\b", re.IGNORECASE), "any relevant information"),
            (re.compile(r"\bstuff\b", re.IGNORECASE), "relevant details"),
            (re.compile(r"\bthings\b", re.IGNORECASE), "specific elements"),
        ]

        for vague_pattern, specific_replacement in vague_term_replacements:
            enhanced_prompt = vague_pattern.sub(specific_replacement, enhanced_prompt)

        # Encourage detail for short prompts
        if len(enhanced_prompt.split()) < 10:
            enhanced_prompt += " Please provide detailed information."

        return enhanced_prompt

    def design_structure(self, prompt: str, platform: str, intent: str) -> str:
        """Step 2: Design structure optimized for target AI platform"""
        from .rbac import AccessControl, Role

        # Strict platform validation with authorization check
        if platform not in self.ALLOWED_PLATFORMS:
            raise ValueError(f"Invalid platform: {platform}")

        # Authorization check for platform access
        if not AccessControl.validate_platform_access(Role.USER, platform):
            raise PermissionError(f"Access denied for platform: {platform}")

        structured_prompt = prompt

        platform_templates = {
            "claude": {
                "prefix": "Human: ",
                "structure": "Please {action}. Be thorough and accurate.",
                "suffix": "",
            },
            "chatgpt": {
                "prefix": "",
                "structure": "Act as an expert. {action}",
                "suffix": "Provide a comprehensive response.",
            },
            "gemini": {
                "prefix": "",
                "structure": "{action}",
                "suffix": "Be precise and helpful.",
            },
            "generic": {"prefix": "", "structure": "{action}", "suffix": ""},
        }

        template = platform_templates[platform]

        # Apply platform-specific structure for simple prompts
        word_count = len(structured_prompt.split())
        if word_count < 15:
            user_action = structured_prompt.lower().strip()

            # Apply structure template
            if template["structure"] and "{action}" in template["structure"]:
                structured_prompt = template["structure"].format(action=user_action)

            # Add prefix and suffix
            if template["prefix"]:
                structured_prompt = template["prefix"] + structured_prompt

            if template["suffix"]:
                structured_prompt += " " + template["suffix"]

        # Add polite framing for technical requests
        if intent == "technical" and not structured_prompt.startswith(
            ("Please", "Can you", "How")
        ):
            structured_prompt = f"Please {structured_prompt.lower()}"

        return structured_prompt

    def deliver_format(self, prompt: str, output_type: str) -> str:
        """Step 3: Deliver final formatting based on expected output type"""
        formatted_prompt = prompt

        # Output type specific formatting
        format_instructions = {
            "list": "Please format your response as a numbered or bulleted list.",
            "explanation": "Please provide a clear, step-by-step explanation.",
            "code": "Please provide code examples with comments and explanations.",
            "creative": "Please be creative and engaging in your response.",
            "general": "Please provide a comprehensive and well-structured response.",
        }

        format_instruction = format_instructions.get(
            output_type, format_instructions["general"]
        )

        # Add format guidance if not already specified
        if not self._FORMAT_KEYWORDS.search(formatted_prompt):
            formatted_prompt += f" {format_instruction}"

        # Ensure proper sentence ending
        if not formatted_prompt.endswith((".", "!", "?")):
            formatted_prompt += "."

        # Clean whitespace
        formatted_prompt = self._WHITESPACE_CLEANER.sub(" ", formatted_prompt).strip()

        return formatted_prompt

    def get_technique_description(self, technique: str) -> str:
        """Get description of optimization technique with validation"""
        if technique not in self.ALLOWED_TECHNIQUES:
            return "Unknown technique"

        descriptions = {
            "develop_clarity": "Enhanced clarity and specificity by replacing vague terms and adding context",
            "design_structure": "Optimized structure for target platform and intent",
            "deliver_format": "Applied final formatting and output type optimization",
        }

        return descriptions[technique]
