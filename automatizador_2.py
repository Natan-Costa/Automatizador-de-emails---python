import csv
import smtplib
from email.mime.text import MIMEText

def atributos_de_arquivo(): 
    nome_arquivo = input("Insira o nome do arquivo armazenado na pasta do programa para funcionar: ") + ".csv"
    numero_coluna = int(input("Insira o valor da coluna com e-mail a ser enviado: "))
    
    return nome_arquivo, numero_coluna 
    
def ler_coluna_csv(nome_arquivo, numero_coluna):
    email = set()
    try:
        numero_coluna = int(numero_coluna)
    except ValueError:
        print('Valor inválido, digite o número da coluna')
        return email

    try:
        with open(nome_arquivo) as csv_file:
            csv_reader = csv.reader(csv_file)

            for linha in csv_reader:
                if len(linha) > numero_coluna:
                    coluna_selecionada = linha[numero_coluna]
                    email.add(coluna_selecionada)
                else:
                    print(f"A linha {linha} não tem uma coluna {numero_coluna}")
    except FileNotFoundError:
        print(f'O arquivo {nome_arquivo} não foi encontrado')
        return email
    return email

def criar_bd(emails):
    nomear_novo_csv = input("Digite um nome para o banco de dados: ") + ".csv"
    with open(nomear_novo_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        for email in emails:
            writer.writerow([email])
    print("Banco de dados criado com sucesso")

def enviar_email(emails, assunto, mensagem):
    email_remetente = input("Digite o endereço de e-mail do remetente: ")
    senha_remetente = input("Digite a senha do remetente: ")
    
    smtp_host = input("Digite o servidor SMTP: ")
    smtp_porta = int(input("Digite a porta do servidor SMTP: "))

    server = smtplib.SMTP(smtp_host, smtp_porta)
    server.starttls()
    server.login(email_remetente, senha_remetente)

    for email_destinatario in emails:
        msg = MIMEText(mensagem, 'html')
        msg['Subject'] = assunto
        msg['From'] = email_remetente
        msg['To'] = email_destinatario

        server.sendmail(email_remetente, [email_destinatario], msg.as_string())

    server.quit()
    print("E-mails enviados com sucesso")

while True:
    nome_arquivo, numero_coluna = atributos_de_arquivo()
    emails = ler_coluna_csv(nome_arquivo, numero_coluna)
    criar_bd(emails)
    assunto = input("Digite o assunto do e-mail: ")
    mensagem = input("Digite a mensagem do e-mail: ")
    enviar_email(emails, assunto, mensagem)