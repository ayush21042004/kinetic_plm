import os
import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AiService:
    def __init__(self):
        self.api_key = (os.getenv("GEMINI_API_KEY") or "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        # Increase timeout to 30s as default, and ensure a minimum of 10s for generation
        try:
            self.timeout = int(os.getenv("GEMINI_TIMEOUT", "30"))
        except (ValueError, TypeError):
            self.timeout = 30
            
        if self.timeout < 10:
            logger.warning(f"Gemini timeout {self.timeout}s is too low for generation. Increasing to 30s.")
            self.timeout = 30

        self.api_url = None
        if self.api_key:
            # Using v1beta for gemini-2.5-flash as it's often more accessible for experimental models
            self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            logger.info(
                "Gemini AI service configured with model '%s' and API key suffix '%s'",
                self.model,
                self._masked_key_suffix(),
            )
        else:
            logger.warning("Gemini AI service disabled: GEMINI_API_KEY is missing or empty.")

    def generate_impact_analysis(self, eco_data: Dict[str, Any]) -> str:
        """
        Generate an impact analysis for an ECO using Gemini.
        """
        if not self.api_key or not self.api_url:
            return "AI Analysis skipped: GEMINI_API_KEY is not configured."

        prompt = self._build_prompt(eco_data)
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        try:
            logger.info(
                "Calling Gemini API for impact analysis with model '%s' and key suffix '%s'",
                self.model,
                self._masked_key_suffix(),
            )
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract text from Gemini response structure
            candidates = result.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "No analysis generated.")
            
            return "AI Analysis failed: Unexpected response format from Gemini."
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else "unknown"
            response_body = e.response.text if e.response is not None else ""
            logger.error("Gemini API HTTP error %s: %s", status_code, response_body)

            if status_code == 403:
                return (
                    "AI Analysis failed: Gemini returned 403 Forbidden. "
                    "Check GEMINI_API_KEY, API restrictions, enabled APIs, model access, and billing. "
                    f"Response: {response_body}"
                )

            return f"AI Analysis failed: Gemini HTTP {status_code}. Response: {response_body}"
        except requests.exceptions.RequestException as e:
            logger.error("Gemini API request failed: %s", e)
            return f"AI Analysis failed: Request error while contacting Gemini: {str(e)}"
        except Exception as e:
            logger.error("Gemini API unexpected failure: %s", e)
            return f"AI Analysis failed: Unexpected error: {str(e)}"

    def _masked_key_suffix(self) -> str:
        if not self.api_key:
            return "missing"
        if len(self.api_key) <= 4:
            return self.api_key
        return self.api_key[-4:]

    def _build_prompt(self, eco_data: Dict[str, Any]) -> str:
        """Construct the prompt for Gemini."""
        eco_name = eco_data.get("title", "Unknown ECO")
        eco_type = eco_data.get("entity_type", "Unknown Type")
        subtitle = eco_data.get("subtitle", "")
        
        # Build a detailed string of changes
        changes_str = ""
        if eco_type == "product":
            field_changes = eco_data.get("field_changes", [])
            for change in field_changes:
                label = change.get('label', change.get('field'))
                changes_str += f"- {label}: {change.get('old_value')} -> {change.get('new_value')}\n"
        elif eco_type == "bom":
            comp_changes = eco_data.get("component_changes", [])
            for change in comp_changes:
                type_msg = change.get("change_type", "changed").upper()
                changes_str += f"- COMPONENT {type_msg}: {change.get('label')} (Old: {change.get('old_value')}, New: {change.get('new_value')})\n"
            
            work_changes = eco_data.get("workorder_changes", [])
            for change in work_changes:
                type_msg = change.get("change_type", "changed").upper()
                changes_str += f"- WORK ORDER {type_msg}: {change.get('label')} (Old: {change.get('old_value')}, New: {change.get('new_value')})\n"

        prompt = f"""
You are an expert Engineering Change Management consultant working for Kinetic PLM.
Provide a concise but professional impact analysis for the following Engineering Change Order (ECO).

{eco_name}
{subtitle}

ECO TYPE: {eco_type.upper()}

PROPOSED CHANGES:
{changes_str if changes_str else "No specific document changes provided."}

Please provide your analysis.
IMPORTANT FORMATTING RULES:
1. Do NOT use markdown bolding (no **stars**).
2. Each header MUST be on clear, plain text in ALL CAPS.
3. Each header MUST be on its own line and be followed by TWO newlines.
4. Use double newlines (blank line) between EVERY bullet point.
5. Use bullet points (-) for the analysis points.
6. Each bullet point MUST be on its own new line.
7. Avoid ALL paragraph blocks. Every piece of information must be a bullet point.
8. Limit the total response to ~150-200 words.
9. The tone should be professional and technical.
"""
        return prompt

_ai_service = None

def get_ai_service() -> AiService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AiService()
    return _ai_service
