import html2text
from imapclient import IMAPClient
import email
from bs4 import BeautifulSoup
from datetime import datetime
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

EMAIL = ""
MOT_DE_PASSE = ""
SERVEUR_IMAP = "imap.gmail.com"

from datetime import datetime

def get_emails(from_email, date_debut_str, date_fin_str):
    messages = []

    # Convertir les chaînes en objets datetime
    date_debut = datetime.strptime(date_debut_str, "%d-%b-%Y")
    date_fin = datetime.strptime(date_fin_str, "%d-%b-%Y")

    # Reformater pour IMAP
    date_debut_imap = date_debut.strftime("%d-%b-%Y")
    date_fin_imap = date_fin.strftime("%d-%b-%Y")

    with IMAPClient(SERVEUR_IMAP, ssl=True) as server:
        server.login(EMAIL, MOT_DE_PASSE)
        server.select_folder("INBOX")
        messages_ids = server.search([
            'FROM', from_email,
            'SINCE', date_debut_imap,
            'BEFORE', date_fin_imap
        ])

        for msgid, data in server.fetch(messages_ids, ["RFC822"]).items():
            email_message = email.message_from_bytes(data[b"RFC822"])
            for part in email_message.walk():
                if part.get_content_type() == "text/html":
                    contenu_html = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    texte = html2text.html2text(contenu_html)
                    messages.append(texte)
    return messages



if __name__ == "__main__":
    expediteur = input("Adresse email de l’expéditeur : ")
    date_debut = input("Date de début (ex : 01-Jan-2024) : ")
    date_fin = input("Date de fin (ex : 01-Apr-2024) : ")
    emails = get_emails(expediteur, date_debut, date_fin)
    print("emails",emails)