import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import email.utils
from email import encoders
import time
import random
import os

# 스크립트 파일이 위치한 디렉토리를 기준으로 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))

# 템플릿 파일 읽기
def read_template(file_path):
    abs_file_path = os.path.join(script_dir, file_path)  # 절대 경로로 변환
    with open(abs_file_path, 'r', encoding='utf-8') as template_file:
        return template_file.read()

# 템플릿에 변수를 채워넣기
def fill_template(template, variables):
    return template.format(**variables)

# SMTP 서버 설정
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "info@clovercell.com"
sender_password = "hspf djcy rlkq lezc"

# 템플릿 파일 경로 (상대 경로)
template_file_path = r"./mail_templates/temp_style-doc.html"

# 템플릿 내용 읽기
template_content = read_template(template_file_path)

# 수신자 CSV 파일 경로 (상대 경로)
csv_file_path = r"./csv/recipients.csv"

# 첨부 파일 경로 (필요시)
attachment_file_path = r""

# CSV 파일에서 수신자 목록 읽기 및 이메일 전송
abs_csv_file_path = os.path.join(script_dir, csv_file_path)  # 절대 경로로 변환
with open(abs_csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        recipient_email = row['email']
        recipient_name = row['recipient_name']
        person_in_charge = row['person_in_charge']
        mail_subject = row['mail_subject']  
        cc_emails = [email.strip() for email in row['cc'].split(',')] if 'cc' in row else []
        bcc_emails = [email.strip() for email in row['bcc'].split(',')] if 'bcc' in row else []
        
        # 변수 채우기
        variables = {
            "recipient_name": recipient_name,
            "person_in_charge": person_in_charge,
            "mail_subject": mail_subject, 
        }

        # 템플릿에 변수 적용
        html_content = fill_template(template_content, variables)

        # 이메일 메시지 설정
        msg = MIMEMultipart("alternative")
        msg['From'] = f'CLOVERCELL <{sender_email}>'
        msg['To'] = recipient_email
        msg['Cc'] = ', '.join(cc_emails)
        msg['Subject'] = f"{variables['mail_subject']}" 
        # msg['Subject'] = f"{variables['mail_subject']}____ID{random.randint(1000, 9999)}"  # 각 이메일마다 고유한 ID 추가
        msg['Message-ID'] = email.utils.make_msgid(domain="clovercell.com")

        # HTML 본문 추가
        msg.attach(MIMEText(html_content, 'html'))

        # 첨부 파일 추가
        if attachment_file_path and os.path.exists(os.path.join(script_dir, attachment_file_path)):
            with open(os.path.join(script_dir, attachment_file_path), "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # 파일을 Base64로 인코딩
            encoders.encode_base64(part)

            # 헤더 추가
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_file_path)}",
            )

            # 메시지에 첨부 파일 추가
            msg.attach(part)
            
        # 최종 수신자 리스트 (To + Cc + Bcc)
        recipients = [recipient_email] + cc_emails + bcc_emails
        
        try:
            # SMTP 서버에 연결
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # TLS 모드로 전환
            server.login(sender_email, sender_password)

            # 이메일 전송
            server.sendmail(sender_email, recipients, msg.as_string())

            print(f"Email sent successfully to {recipient_email}, CC: {', '.join(cc_emails)}, BCC: {', '.join(bcc_emails)}")

        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")

        finally:
            server.quit()
