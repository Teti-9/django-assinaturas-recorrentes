## Django - Gerenciamento de Alunos e Matrículas.

Projeto com integração com a EFI Bank API para gerenciamento de assinaturas recorrentes.

## Funcionalidades da API

- 📌 **Alunos:** CRUD (Criar, Ler, Atualizar, Deletar) de alunos.  

- 📌 **Matrículas:** CRUD (Criar, Ler, Atualizar, Deletar) de matrículas.  

- 📌 **Validações:** Valida CPF, CEP, Telefone, Email e utiliza da VIACEP Api para preencher dados residencias através do CEP.  

## 🛠️ Instalação e Configuração

### 🔹 Instalação Local (SQLite)
```
git clone https://github.com/Teti-9/django-gerenciamento.git
cd django-gerenciamento
pip install -r requirements.txt
python manage.py migrate

Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:

CLIENT = "Client_Id"
SECRET = "Client_Secret"
CERTIFICATE = "O Certificado deve ser convertido para .PEM para funcionar."

* https://github.com/efipay/conversor-p12-efi?tab=readme-ov-file
* https://dev.efipay.com.br/docs/api-pix/credenciais/

Rode a aplicação na pasta raíz do projeto:
python manage.py runserver
```

## 👨‍💻 Interface Admin
```
- Para acessar o painel admin que possui todas operações, crie um super usuário na pasta raiz do projeto:
python manage.py createsuperuser
python manage.py runserver

Acesse:
http://localhost:8000/admin
```

## 📥 Homologação
```
Todo ambiente está configurado em homologação com dados falsos inseridos para que tests possam ser feitos imediatamente.
```