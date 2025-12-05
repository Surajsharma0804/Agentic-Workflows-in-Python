from .base import PluginBase
import textwrap
from pathlib import Path

class EmailSummarizer(PluginBase):
    name = "email_summarizer"

    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.source = params.get("source_path")  # for demo: local mbox or txt
        self.num_sentences = int(params.get("num_sentences", 3))
        self.dry_run = params.get("dry_run", True)

    def _load_emails(self):
        if not self.source:
            return []
        p = Path(self.source)
        if not p.exists():
            return []
        text = p.read_text(encoding="utf-8")
        # naive split: each paragraph is an "email"
        emails = [e.strip() for e in text.split("\n\n") if e.strip()]
        return emails

    def plan(self):
        n = len(self._load_emails())
        return [{"action": "summarize", "emails": n}]

    def execute(self):
        """Execute email summarization with detailed statistics."""
        if self.dry_run:
            emails = self._load_emails()
            return {
                "status": "planned",
                "source": self.source,
                "emails_found": len(emails),
                "num_sentences": self.num_sentences,
                "would_process": len(emails)
            }
        
        emails = self._load_emails()
        summaries = []
        total_chars_original = 0
        total_chars_summary = 0
        
        for idx, e in enumerate(emails):
            # naive summarization: take first N sentences by splitting on '.'
            sentences = [s.strip() for s in e.split('.') if s.strip()]
            summary = '. '.join(sentences[:self.num_sentences])
            if summary and not summary.endswith('.'):
                summary += '.'
            
            total_chars_original += len(e)
            total_chars_summary += len(summary)
            
            summaries.append({
                "email_index": idx,
                "original_length": len(e),
                "summary_length": len(summary),
                "summary": summary,
                "compression_ratio": round(len(summary) / len(e), 2) if len(e) > 0 else 0
            })
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "email_index": idx,
                    "summary_len": len(summary),
                    "original_len": len(e)
                })
        
        return {
            "status": "completed",
            "emails_processed": len(emails),
            "summaries": summaries[:20],  # Limit to first 20 for response size
            "total_summaries": len(summaries),
            "statistics": {
                "total_original_chars": total_chars_original,
                "total_summary_chars": total_chars_summary,
                "average_compression_ratio": round(
                    total_chars_summary / total_chars_original, 2
                ) if total_chars_original > 0 else 0,
                "sentences_per_summary": self.num_sentences
            },
            "source": self.source
        }
