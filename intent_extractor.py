import dateparser
import re
from datetime import datetime

class IntentExtractor:
    def __init__(self):
        # Keywords for intent classification
        self.INTENT_MAP = {
            "schedule_event": ["schedule", "meet", "meeting", "appointment", "calendar", "event"],
            "create_reminder": ["remind", "reminder", "notify", "alarm"],
            "create_task": ["do", "submit", "finish", "buy", "get", "make", "task", "todo", "write", "send", "cod", "create"]
        }
        
        self.PRIORITY_MAP = {
            "high": ["urgent", "asap", "important", "critical", "high", "immediately"],
            "low": ["low", "whenever", "eventually"],
            "medium": [] # Default
        }

    def _detect_intent(self, text_lower: str) -> str:
        """Simple keyword matching to guess intent."""
        for intent, keywords in self.INTENT_MAP.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        return "unknown"

    def _extract_priority(self, text_lower: str) -> str:
        for priority, keywords in self.PRIORITY_MAP.items():
            if any(keyword in text_lower for keyword in keywords):
                return priority
        return "medium"

    def _clean_title(self, text: str, intent: str, date_obj) -> str:
        """
        Heuristic cleanup to extract the core task/event title.
        1. Remove intent keywords (intro phrases).
        2. Dateparser consumes date strings, but we might want to remove them from title if possible. 
           (Simplification: validation is complex without robust NER, keeping it simple for Hackathon).
        """
        # Remove common "remind me to" or "schedule a" prefixes
        # This is a very basic replacement strategy
        clean_text = text
        
        prefixes = [
            "remind me to", "remind me", "please remind me to",
            "schedule a", "schedule", "create a task to", 
            "add a task to", "i need to", "don't forget to"
        ]
        
        text_lower = text.lower()
        for prefix in prefixes:
            if text_lower.startswith(prefix):
                clean_text = text[len(prefix):].strip()
                break # Only remove the first matching prefix
        
        return clean_text.capitalize()

    def extract(self, text: str) -> dict:
        """
        Main extraction method.
        """
        if not text:
            return {
                "intent": "unknown",
                "task_title": "",
                "datetime": None,
                "priority": "medium",
                "confidence": 0.0
            }

        text_lower = text.lower()
        
        # 1. Detect Intent
        intent = self._detect_intent(text_lower)
        
        # 2. Extract Priority
        priority = self._extract_priority(text_lower)
        
        # 3. Extract Date/Time
        # Use search_dates to find the date/time part within the sentence
        from dateparser.search import search_dates
        found_dates = search_dates(text, settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': datetime.now()})
        
        dt_obj = None
        date_str_found = ""
        if found_dates:
            # Take the first date found (usually the most relevant for simple tasks)
            date_str_found, dt_obj = found_dates[0]
        
        # 4. Extract Title
        # For a truly clean title, we remove the exact date string found by dateparser
        task_title = self._clean_title(text, intent, dt_obj)
        if date_str_found:
            # Case insensitive removal of the date string from the title
            pattern = re.compile(re.escape(date_str_found), re.IGNORECASE)
            task_title = pattern.sub("", task_title).strip()
            # Clean up potential double spaces or trailing punctuation
            task_title = re.sub(r'\s+', ' ', task_title).strip()
            task_title = task_title.strip(",. ")

        # Calculate a mock confidence score
        confidence = 0.5
        if intent != "unknown":
            confidence += 0.3
        if dt_obj:
            confidence += 0.15

        return {
            "intent": intent,
            "task_title": task_title,
            "datetime": dt_obj.isoformat() if dt_obj else None,
            "priority": priority,
            "confidence": round(confidence, 2)
        }

if __name__ == "__main__":
    # Simple test
    extractor = IntentExtractor()
    print(extractor.extract("Remind me to submit DBMS assignment tomorrow at 6 pm"))
