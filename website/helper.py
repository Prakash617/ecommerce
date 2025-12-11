from typing import Union, List, Dict, Optional, Tuple, Any

import requests
from django.core.mail import send_mail, send_mass_mail, get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.conf import settings
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class EmailHelper:
    """
    Production-ready Django Email Helper for single and mass emails with HTML support.

    Features:
    - Single email sending
    - Mass email sending with batching
    - HTML email support
    - Template-based emails
    - Async and sync sending options
    - Error handling and logging
    - Connection reuse for performance
    """

    def __init__(self,
                 from_email: str = None,
                 batch_size: int = 100,
                 max_workers: int = 3,
                 connection_timeout: int = 60):
        """
        Initialize EmailHelper with configuration.

        Args:
            from_email (str): Default from email address
            batch_size (int): Number of emails per batch for mass sending
            max_workers (int): Maximum concurrent threads
            connection_timeout (int): SMTP connection timeout in seconds
        """
        self.from_email = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', "no-reply@clubnect.com")
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.connection_timeout = connection_timeout
        self.sms_api = "a5c721be4a76bf54964b12641e02a1d680db8f20dfc29aaf2d3a34e05cd2901c"

    def send_sms(self, phone_number: str, message: str) -> bool:
        try:
            request_url = "https://sms.aakashsms.com/sms/v3/send"
            payload = {
                "auth_token": self.sms_api,
                "to": phone_number,
                "text": message
            }

            response = requests.post(request_url, json=payload)
            print(f"SMS Response: {response.status_code} - {response.text}")
            return True
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False


    def generate_token(self, length: int = 32) -> str:
        """
        Generates a unique token for various purposes (e.g., email verification).

        Args:
            length (int): The length of the token to generate. Default is 32.

        Returns:
            str: A randomly generated token.
        """
        return get_random_string(
            length=length,
            allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789"
        )

    def get_template_content(self, template_name: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Renders the specified template with the given context.

        Args:
            template_name (str): The name of the template file (without the extension).
            context (Optional[Dict[str, Any]]): The context data to be passed to the template.

        Returns:
            str: The rendered template content as a string.
        """
        if context is None:
            context = {}

        try:
            return render_to_string(f"mail/{template_name}.html", context)
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {str(e)}")
            raise

    def _send_mass_html_mail(self,
                             datatuple: List[Tuple],
                             fail_silently: bool = False,
                             user: str = None,
                             password: str = None,
                             connection=None) -> int:
        """
        Sends mass emails with HTML support using EmailMultiAlternatives.

        Args:
            datatuple: List of tuples (subject, text_content, html_content, from_email, recipient_list)
            fail_silently: Whether to suppress exceptions
            user: SMTP username
            password: SMTP password
            connection: Existing SMTP connection

        Returns:
            int: Number of successfully sent emails
        """
        connection = connection or get_connection(
            username=user,
            password=password,
            fail_silently=fail_silently,
            timeout=self.connection_timeout
        )

        messages = []
        for subject, text_content, html_content, from_email, recipient_list in datatuple:
            # Ensure recipient_list is actually a list
            if isinstance(recipient_list, str):
                recipient_list = [recipient_list]

            message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=recipient_list
            )

            if html_content:
                message.attach_alternative(html_content, 'text/html')

            messages.append(message)

        try:
            return connection.send_messages(messages)
        except Exception as e:
            if not fail_silently:
                raise
            logger.error(f"Failed to send mass email: {str(e)}")
            return 0
        finally:
            if hasattr(connection, 'close'):
                try:
                    connection.close()
                except:
                    pass

    def _prepare_mass_html_mail_data(self,
                                     subject: str,
                                     html_content: str,
                                     recipients: List[str],
                                     text_content: str = None) -> List[Tuple]:
        """
        Prepares email data for mass HTML email sending.

        Args:
            subject (str): Email subject (same for all)
            html_content (str): Email HTML content (same for all)
            recipients (List[str]): List of recipient emails
            text_content (str): Plain text version (optional)

        Returns:
            List[Tuple]: List of tuples for _send_mass_html_mail
        """
        if text_content is None:
            text_content = strip_tags(html_content)

        return [
            (subject, text_content, html_content, self.from_email, [recipient])
            for recipient in recipients
        ]

    def _send_mass_mail_batch(self, mail_data: List[Tuple]) -> Dict[str, Union[int, str, bool]]:
        """
        Sends a batch of emails using the custom HTML mass mail function.

        Args:
            mail_data (List[Tuple]): Email data formatted for mass sending

        Returns:
            Dict with batch results
        """
        try:
            sent_count = self._send_mass_html_mail(mail_data, fail_silently=False)
            success_count = sent_count if sent_count is not None else 0
            failed_count = len(mail_data) - success_count

            logger.info(f"Batch completed: {success_count}/{len(mail_data)} emails sent successfully")

            return {
                "success": True,
                "sent_count": success_count,
                "total_count": len(mail_data),
                "failed_count": failed_count
            }
        except Exception as e:
            logger.error(f"Failed to send email batch: {str(e)}")
            return {
                "success": False,
                "sent_count": 0,
                "total_count": len(mail_data),
                "failed_count": len(mail_data),
                "error": str(e)
            }

    def _chunk_recipients(self, recipients: List[str], chunk_size: int) -> List[List[str]]:
        """Split recipients into chunks of specified size."""
        return [recipients[i:i + chunk_size] for i in range(0, len(recipients), chunk_size)]

    def _validate_email_params(self, subject: str, message: str, recipients: List[str]) -> None:
        """Validate email parameters."""
        if not subject or not subject.strip():
            raise ValueError("Email subject cannot be empty")

        if not message or not message.strip():
            raise ValueError("Email message cannot be empty")

        if not recipients:
            raise ValueError("Recipients list cannot be empty")

        # Basic email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = [email for email in recipients if not re.match(email_pattern, email)]

        if invalid_emails:
            logger.warning(f"Invalid email addresses found: {invalid_emails[:5]}...")  # Log first 5
            # Remove invalid emails rather than failing completely
            return [email for email in recipients if re.match(email_pattern, email)]

        return recipients

    def send_single_email(self,
                          subject: str,
                          message: str,
                          to_email: str,
                          html_message: str = None,
                          from_email: str = None) -> Dict[str, Any]:
        """
        Sends a single email with HTML support.

        Args:
            subject (str): Email subject
            message (str): Plain text message
            to_email (str): Recipient email address
            html_message (str): HTML version of the message (optional)
            from_email (str): Custom from email (optional)

        Returns:
            Dict: Result with success status
        """
        try:
            from_addr = from_email or self.from_email

            if html_message:
                # Use EmailMultiAlternatives for HTML support
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=from_addr,
                    to=[to_email]
                )
                email.attach_alternative(html_message, "text/html")
                result = email.send()
            else:
                # Use regular send_mail
                result = send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_addr,
                    recipient_list=[to_email],
                    fail_silently=False
                )

            logger.info(f"Single email sent successfully to {to_email}")
            return {
                "success": True,
                "recipient": to_email,
                "method": "single_email"
            }

        except Exception as e:
            logger.error(f"Failed to send single email to {to_email}: {str(e)}")
            return {
                "success": False,
                "recipient": to_email,
                "error": str(e),
                "method": "single_email"
            }

    def send_email(self,
                   subject: str,
                   message: str,
                   to_email: Union[str, List[str], Dict[str, str]],
                   html_message: str = None,
                   from_email: str = None) -> Dict[str, Union[int, str]]:
        """
        Sends email(s) with HTML support to single or multiple recipients.

        Args:
            subject (str): The subject of the email (same for all recipients).
            message (str): The plain text content of the email.
            to_email (Union[str, List[str], Dict[str, str]]): The recipient(s) email address(es).
            html_message (str): HTML version of the message (optional).
            from_email (str): Custom from email (optional).

        Returns:
            Dict: Results summary with success/failure counts
        """
        try:
            # Normalize recipients to list
            if isinstance(to_email, dict):
                recipients = list(to_email.values())
            elif isinstance(to_email, str):
                recipients = [to_email]
            else:
                recipients = list(to_email)

            # Remove duplicates and validate
            recipients = list(dict.fromkeys(recipients))
            recipients = self._validate_email_params(subject, message, recipients)

            if not recipients:
                return {
                    "success": False,
                    "error": "No valid recipients found",
                    "total_recipients": 0
                }

            # For single recipient, use single email method
            if len(recipients) == 1:
                result = self.send_single_email(
                    subject=subject,
                    message=message,
                    to_email=recipients[0],
                    html_message=html_message,
                    from_email=from_email
                )
                return {
                    "total_recipients": 1,
                    "method": "single_email",
                    "success": result["success"],
                    "results": [result]
                }

            # Use mass email for multiple recipients
            return self._send_mass_emails_async(
                subject=subject,
                message=message,
                recipients=recipients,
                html_message=html_message,
                from_email=from_email
            )

        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "total_recipients": 0
            }

    def _send_mass_emails_async(self,
                                subject: str,
                                message: str,
                                recipients: List[str],
                                html_message: str = None,
                                from_email: str = None) -> Dict[str, Union[int, str]]:
        """
        Sends mass emails asynchronously with HTML support.
        """
        results = {
            "total_recipients": len(recipients),
            "total_sent": 0,
            "total_failed": 0,
            "method": "mass_email_async",
            "status": "processing"
        }

        def process_mass_emails():
            try:
                # Use HTML message if provided, otherwise convert plain text
                html_content = html_message or f"<p>{message.replace(chr(10), '<br>')}</p>"

                # Split into batches
                recipient_chunks = self._chunk_recipients(recipients, self.batch_size)

                # Process batches concurrently
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    batch_futures = []

                    for chunk in recipient_chunks:
                        # Prepare batch data with HTML support
                        batch_mail_data = self._prepare_mass_html_mail_data(
                            subject=subject,
                            html_content=html_content,
                            recipients=chunk,
                            text_content=message
                        )
                        future = executor.submit(self._send_mass_mail_batch, batch_mail_data)
                        batch_futures.append(future)

                    # Collect results from all batches
                    for future in as_completed(batch_futures):
                        try:
                            batch_result = future.result()
                            results["total_sent"] += batch_result["sent_count"]
                            results["total_failed"] += batch_result["failed_count"]
                        except Exception as e:
                            logger.error(f"Batch processing error: {str(e)}")
                            results["total_failed"] += self.batch_size

                results["status"] = "completed"
                logger.info(
                    f"Mass email completed: {results['total_sent']} sent, "
                    f"{results['total_failed']} failed out of {results['total_recipients']} total"
                )

            except Exception as e:
                logger.error(f"Mass email processing failed: {str(e)}")
                results["status"] = "failed"
                results["error"] = str(e)

        # Start async processing
        thread = Thread(target=process_mass_emails)
        thread.daemon = True  # Daemon thread for better cleanup
        thread.start()

        return results

    def send_with_template(self,
                           template: str,
                           context: Dict[str, Any],
                           subject: str,
                           to_email: Union[str, List[str], Dict[str, str]],
                           from_email: str = None) -> Dict[str, Union[int, str]]:
        """
        Sends an email using a template with HTML support.

        Args:
            template (str): The template name to use for the email content.
            context (Dict[str, Any]): A dictionary of context data to be passed to the template.
            subject (str): The subject of the email (same for all recipients).
            to_email (Union[str, List[str], Dict[str, str]]): The recipient(s) email address(es).
            from_email (str): Custom from email (optional).

        Returns:
            Dict: Results summary
        """
        try:
            html_message = self.get_template_content(template, context=context)
            print(html_message)
            plain_message = strip_tags(html_message)

            return self.send_email(
                subject=subject,
                message=plain_message,
                to_email=to_email,
                html_message=html_message,
                from_email=from_email
            )
        except Exception as e:
            logger.error(f"Template email failed: {str(e)}")
            return {
                "success": False,
                "error": f"Template processing failed: {str(e)}",
                "total_recipients": 0
            }

    def send_mass_email_sync(self,
                             subject: str,
                             message: str,
                             recipients: List[str],
                             html_message: str = None,
                             from_email: str = None) -> Dict[str, Union[int, str]]:
        """
        Sends mass emails synchronously (blocking) with HTML support.
        Use this when you need to wait for completion and get immediate results.

        Args:
            subject (str): Email subject (same for all recipients)
            message (str): Plain text content (same for all recipients)
            recipients (List[str]): List of recipient email addresses
            html_message (str): HTML version of the message (optional)
            from_email (str): Custom from email (optional)

        Returns:
            Dict: Complete results with success/failure counts
        """
        try:
            # Validate and clean recipients
            recipients = list(dict.fromkeys(recipients))  # Remove duplicates
            recipients = self._validate_email_params(subject, message, recipients)

            if not recipients:
                return {
                    "success": False,
                    "error": "No valid recipients found",
                    "total_recipients": 0
                }

            results = {
                "total_recipients": len(recipients),
                "total_sent": 0,
                "total_failed": 0,
                "method": "mass_email_sync",
                "batches_processed": 0,
                "batch_results": []
            }

            # Use HTML message if provided
            html_content = html_message or f"<p>{message.replace(chr(10), '<br>')}</p>"

            # Split into batches
            recipient_chunks = self._chunk_recipients(recipients, self.batch_size)

            # Process each batch synchronously
            for i, chunk in enumerate(recipient_chunks):
                try:
                    batch_mail_data = self._prepare_mass_html_mail_data(
                        subject=subject,
                        html_content=html_content,
                        recipients=chunk,
                        text_content=message
                    )

                    batch_result = self._send_mass_mail_batch(batch_mail_data)

                    results["total_sent"] += batch_result["sent_count"]
                    results["total_failed"] += batch_result["failed_count"]
                    results["batches_processed"] += 1
                    results["batch_results"].append(batch_result)

                    logger.info(
                        f"Processed batch {i + 1}/{len(recipient_chunks)}: "
                        f"{batch_result['sent_count']} sent, {batch_result['failed_count']} failed"
                    )

                    # Small delay between batches to avoid overwhelming the server
                    if i < len(recipient_chunks) - 1:
                        time.sleep(0.1)

                except Exception as e:
                    logger.error(f"Batch {i + 1} failed: {str(e)}")
                    results["total_failed"] += len(chunk)
                    results["batch_results"].append({
                        "success": False,
                        "error": str(e),
                        "total_count": len(chunk)
                    })

            results["success"] = results["total_sent"] > 0
            results["status"] = "completed"

            logger.info(
                f"Sync mass email completed: {results['total_sent']} sent, "
                f"{results['total_failed']} failed"
            )

        except Exception as e:
            logger.error(f"Sync mass email failed: {str(e)}")
            return {
                "success": False,
                "status": "failed",
                "error": str(e),
                "total_recipients": len(recipients) if recipients else 0,
                "total_sent": 0,
                "total_failed": len(recipients) if recipients else 0
            }

        return results

    def get_email_stats(self) -> Dict[str, Any]:
        """
        Returns current configuration and stats.

        Returns:
            Dict: Current configuration
        """
        return {
            "from_email": self.from_email,
            "batch_size": self.batch_size,
            "max_workers": self.max_workers,
            "connection_timeout": self.connection_timeout,
            "features": [
                "Single email sending",
                "Mass email sending",
                "HTML email support",
                "Template-based emails",
                "Async and sync sending",
                "Batch processing",
                "Error handling and logging"
            ]
        }

# Usage Examples:

# Initialize the helper
# email_helper = EmailHelper(
#     from_email="noreply@yourapp.com",
#     batch_size=50,
#     max_workers=3
# )

# 1. Send single email with HTML
# result = email_helper.send_single_email(
#     subject="Welcome!",
#     message="Welcome to our platform!",
#     to_email="user@example.com",
#     html_message="<h1>Welcome!</h1><p>Welcome to our platform!</p>"
# )

# 2. Send to multiple recipients (same content)
# recipients = ["user1@example.com", "user2@example.com", "user3@example.com"]
# results = email_helper.send_email(
#     subject="Newsletter March 2025",
#     message="Check out our latest updates!",
#     to_email=recipients,
#     html_message="<h1>Newsletter</h1><p>Check out our latest updates!</p>"
# )

# 3. Send with template
# results = email_helper.send_with_template(
#     template="newsletter",
#     context={"month": "March", "year": "2025", "user_name": "John"},
#     subject="Monthly Newsletter - March 2025",
#     to_email=recipients
# )

# 4. Synchronous mass email (wait for completion)
# results = email_helper.send_mass_email_sync(
#     subject="Important Update",
#     message="This is an important system update.",
#     recipients=recipients,
#     html_message="<h1>Important Update</h1><p>This is an important system update.</p>"
# )
# print(f"Completed: {results['total_sent']} sent, {results['total_failed']} failed")

# 5. Check configuration
# stats = email_helper.get_email_stats()
# print(f"Current config: {stats}")