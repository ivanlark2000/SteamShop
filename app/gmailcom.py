import email
from imaplib import IMAP4_SSL
from config import config


class Gmail:
    """Объект почта"""
    google_host = "imap.gmail.com"
    port = 993
    paswd = config.pwdMail
    email = config.email

    def __init__(self, category='inbox'):
        self.connection = IMAP4_SSL(host=self.google_host, port=self.port)
        self.connection.login(user=self.email, password=self.paswd)
        self.connection.list()
        self.connection.select(category)  # Подключаемся к папке "входящие".

    def gettingSteamCode(self):
        """Получаем код для авторизации стима"""
        _, msgnums = self.connection.search(None, "(SUBJECT 'Steam')")
        msgnum = msgnums[0].split()[-1]
        _, data = self.connection.fetch(msgnum, "(RFC822)")
        self.connection.store(msgnum, "+FLAGS", "\\Deleted")  # устанавливаем метку удаленные
        massage = email.message_from_bytes(data[0][1])
        for part in massage.walk():
            if part.get_content_type() == "text/plain":
                msg = part.as_string()
                self.connection.expunge()  # Навсегда удаляет помеченные письма
                return msg[msg.find('Login Code') + 11:msg.find('Login Code') + 17]

    def cleaningAllemail(self):
        """Для очистки почты"""
        _, msgnums = self.connection.search(None, "ALL")
        for msg in msgnums[0].split():
            print(msg)
            self.connection.store(msg, "+FLAGS", "\\Deleted")  # устанавливаем метку удаленные
        self.connection.expunge()  # Навсегда удаляет помеченные письма
