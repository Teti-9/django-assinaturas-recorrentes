## Django - Gerenciamento de Alunos, Matrículas e Assinaturas.

Projeto integrado com a EFI Bank API para gerenciamento de alunos, matrículas e assinaturas recorrentes.

## Funcionalidades da API

- 📌 **Alunos:** CRUD (Criar, Ler, Atualizar e Deletar) de alunos.  

- 📌 **Matrículas:** CRUD (Criar, Ler, Atualizar e Deletar) de matrículas.  

- 📌 **Validações:** Valida CPF, CEP, Telefone, Email e utiliza da VIACEP Api para preencher dados residencias através do CEP.  

- 📌 **Efí Bank:** Criação, pagamento e cancelamento de assinaturas recorrentes.  

## 🛠️ Instalação e Configuração

### 🔹 Instalação Local (SQLite)
```
git clone https://github.com/Teti-9/django-assinaturas-recorrentes.git
cd django-assinaturas-recorrentes
pip install -r requirements.txt
python manage.py migrate

Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:

CLIENT = "Client_Id"
SECRET = "Client_Secret"
CERTIFICATE = "O Certificado deve ser convertido para .PEM para funcionar."

- Documentação:
* https://dev.efipay.com.br/docs/api-pix/credenciais/
* https://github.com/efipay/conversor-p12-efi?tab=readme-ov-file

Rode a aplicação na pasta raíz do projeto:

python manage.py runserver
```

## 👨‍💻 Homologação
```
* Postman, Insomnia, Thunder Client, Etc.

Exemplo de rota POST Aluno:

- Cadastro
    - Endpoint: /cadastro
    - Method: POST
    - Request Body: Json
{
    "nome": "João",
    "cpf": "56242009943",
    "email": "joao@email.com",
    "data_de_nascimento": "19/02/1992",
    "telefone": "44123456789",
    "endereco_cep": "12345678"
}

* Painel Admin (Interface Front-end e Operações CRUD.)

Na pasta do projeto:

python manage.py createsuperuser
python manage.py runserver

Acesse:

http://localhost:8000/admin
```