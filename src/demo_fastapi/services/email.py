import logging
from email.message import EmailMessage
from smtplib import SMTP

from demo_fastapi.constants.message import FAILED_TO_SEND_MAIL
from demo_fastapi.core.config import SMTP_FROM, SMTP_HOST, SMTP_PORT

logger = logging.getLogger(__name__)


def send_comment_notification(
    to_email: str,
    task_title: str,
    author_name: str,
    content: str,
) -> None:
    message = EmailMessage()
    message["From"] = SMTP_FROM
    message["To"] = to_email
    message["Subject"] = "TaskHub: New comment"
    message.set_content(f"Task: {task_title}\n\n{author_name} commented:\n{content}")

    try:
        with SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as smtp:
            smtp.send_message(message)
    except OSError:
        logger.exception(FAILED_TO_SEND_MAIL)
