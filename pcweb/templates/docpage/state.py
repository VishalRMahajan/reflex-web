"""The state for the navbar component."""
import os
from datetime import datetime
from typing import Any, Optional, Set

import reflex as rx
import requests
from sqlmodel import Field


class Feedback(rx.Model, table=True):
    email: Optional[str]
    feedback: str
    score: Optional[int]
    date_created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    page: str

class FeedbackState(rx.State):
    """The state for feedback components"""

    feedback_open: list[bool] = [False, False]

    def feedback_change(self, change, score):
        self.feedback_open[score] = change

    def handle_submit(self, form_data: dict, score):

        feedback = form_data["feedback"]

        # Check if the email is valid.
        if "email" in form_data:
            email = form_data["email"]

        if len(feedback) < 10 or len(feedback) > 500:
            return rx.window_alert(
                "Please enter your feedback. Between 10 and 500 characters."
            )

        current_page_route = self.get_current_page()

        discord_message = f"""
Contact: {email}
Page: {current_page_route}
Score: {"?" if  score==0 else "👍" if score > 1 else "👎"}
Feedback: {feedback}
"""

        DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
        payload = {"content": discord_message}
        try:
            requests.post(DISCORD_WEBHOOK_URL, json=payload)
        except:
            pass

        self.feedback_open[score] = False
