# Passo a Passo

1. **Configurar o Ambiente Virtual:**

Primeiramente precisamos criar um ambiente virtual com o seguinte comando:

No Windows 
python -m venv venv

No macOS e Linux 
python3 -m venv venv

Depois de criar o ambiente virtual precisamos ativá-lo SEMPRE que estivermos trabalhando no projeto, ativamos com o seguinte comando:

No Windows 
```
venv\Scripts\activate
```

No macOS e Linux 
```
source venv/bin/activate
```

1. **Instalar Dependências:**

Precisamos instalar os pacotes e bibliotecas usados no projeto, fazemos isso com o seguinte comando:

```
pip install -r requirements.txt
```

Sempre que um pacote for instalado precisamos atualizar o requirements com o seguinte comando:

```
pip freeze > requirements.txt
```

1. **Configurar o Banco de Dados:**

Precisamos criar o banco de dados com o seguinte comando:

```
python manage.py migrate
```

E criar um super usuário com o comando:

```
python manage.py createsuperuser
```


1. **Executar o Servidor**

Para executar o servidor é só usar o comando:

```
python manage.py runserver
```

**OBS**
O Login no django admin é feito com Email e senha
