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
        emails = self._load_emails()
        summaries = []
        for e in emails:
            # naive summarization: take first N sentences by splitting on '.'
            sentences = [s.strip() for s in e.split('.') if s.strip()]
            summary = '. '.join(sentences[:self.num_sentences])
            if summary and not summary.endswith('.'):
                summary += '.'
            summaries.append(summary)
            if self.audit:
                self.audit.record({"plugin": self.name, "summary_len": len(summary)})
        return {"status": "ok", "summaries": summaries}
