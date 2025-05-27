import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailClient:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.imap_server = "imap.gmail.com"
        self.smtp_port = 587

    def send_message(self, recipients, subject, message):
        """
        Отправляет письмо на указанные адреса.

        :param recipients: Список адресов получателей
        :param subject: Тема письма
        :param message: Текст письма
        """
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.login, self.password)
            server.sendmail(self.login, recipients, msg.as_string())

    def receive_message(self, header=None):
        """
        Получает последнее письмо из входящих.

        :param header: Заголовок для фильтрации писем (опционально)
        :return: Объект письма
        """
        with imaplib.IMAP4_SSL(self.imap_server) as mail:
            mail.login(self.login, self.password)
            mail.list()
            mail.select("inbox")
            criterion = f'(HEADER Subject "{header}")' if header else 'ALL'
            result, data = mail.uid('search', None, criterion)
            if not data[0]:
                raise ValueError('There are no letters with current header')
            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            return email.message_from_bytes(raw_email)


if __name__ == '__main__':
    # Пример использования
    mail_client = MailClient(
        login='login@gmail.com',
        password='qwerty'
    )

    # Отправка письма
    mail_client.send_message(
        recipients=['vasya@email.com', 'petya@email.com'],
        subject='Subject',
        message='Message'
    )

    # Получение письма
    try:
        received_email = mail_client.receive_message()
        print("Получено письмо:", received_email)
    except ValueError as e:
        print(e)