import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from airflow.models import Variable


def email_success(context):
    subject = context["var"]["value"].get("subject_mail")
    from_address = context["var"]["value"].get("email")
    password = context["var"]["value"].get("email_password")
    to_address = context["var"]["value"].get("to_address")

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText('ETL successfully completed'))

    print(
    f"""
    subject:    {subject}
    from:    {from_address}
    to:    {to_address}
    """
    )

    try:
        server = smtplib.SMTP('smtp.mailersend.net', 587)
        server.starttls()  # Enable security
        server.login(from_address, password)

        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")


def email_failed(context):
    subject = context["var"]["value"].get("subject_mail")
    from_address = context["var"]["value"].get("email")
    password = context["var"]["value"].get("email_password")
    to_address = context["var"]["value"].get("to_address")

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText('ETL error'))

    print(
    f"""
    subject:    {subject}
    from:    {from_address}
    to:    {to_address}
    """
    )

    try:
        server = smtplib.SMTP('smtp.mailersend.net', 587)
        server.starttls()  # Enable security
        server.login(from_address, password)

        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("_________________Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
