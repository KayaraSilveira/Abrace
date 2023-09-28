# Abrace
![Logo do Projeto](base_static/global/img/logo.png)

## Descrição

O Abrace é uma plataforma dedicada à promoção da solidariedade e ao apoio à comunidade. Com o Abrace, você pode facilmente criar e participar de projetos solidários que fazem a diferença na vida das pessoas.

## Funcionalidades Principais
- Cadastro, login, edição e exclusão de perfil
![Página de cadastro](base_static/global/img/registerpage.png)
![Página de login](base_static/global/img/loginpage.png)
![Página de perfil](base_static/global/img/profilepage.png)
- Criação e moderação de projetos, permitindo editar projeto, excluir projeto, aceitar ou recusar solicitações de membros, remover um membro e adicionar ou remover um moderador
![Página de criação de projeto](base_static/global/img/createprojectpage.png)
![Página de solicitações](base_static/global/img/solicitationpage.png)
![Página de membros](base_static/global/img/memberspage.png)
- Postagens e comentários no projeto
![Página de projeto](base_static/global/img/projectpage.png)
![Página de postagem](base_static/global/img/postpage.png)
- Avaliação de usuários
![Página de usuário](base_static/global/img/memberpage.png)
![Página de avaliação](base_static/global/img/reviewpage.png)
- Recomendação de projetos baseado em preferências do usuário
![Página de projetos](base_static/global/img/projectspage.png)

## Nossa Equipe
Somos uma equipe incrível que desenvolveu uma ideia para aproximar voluntários dedicados a fazer a diferença em nossas comunidades e no mundo. Acreditamos no poder da ação voluntária e no impacto positivo que ela pode ter em nossas vidas e naqueles que ajudamos.

### Gabriele Lucas
![Gabriele](base_static/global/img/gabriele.JPG)
- **Função:** Tech Lead e QA
   
- **GitHub:** [SLGabi](https://github.com/SLGabi)

### Diulia Deon
![Diulia](base_static/global/img/diulia.JPG)
- **Função:** UI/UX Design
   
- **GitHub:** [diuliad](https://github.com/diuliad)

### Kayara Silveira
![Kayara](base_static/global/img/kayara.JPG)
- **Função:** Desenvolvedora Full Stack e Arquiteta de Software
   
- **GitHub:** [kayarasilveira](https://github.com/kayarasilveira)

### Frederico dal Soglio
![Frederico](base_static/global/img/frederico.JPG)
- **Função:** Desenvolvedor Back end
   
- **GitHub:** [FredDsR](https://github.com/FredDsR)

### Rafael Copes
![Rafael](base_static/global/img/copes.JPG)
- **Função:** Desenvolvedor Front end
   
- **GitHub:** [RafaelCopes](https://github.com/RafaelCopes)

### Italo Silveira
![italo](base_static/global/img/italo.JPG)
- **Função:** Desenvolvedor Front end
   
- **GitHub:** [italotss](https://github.com/italotss)



## Instalação

Para executar o projeto localmente, siga estas etapas:

1. Clone este repositório:
   ```bash
   git clone https://github.com/KayaraSilveira/Abrace.git
   ```
2. Crie e Ative o ambiente virtual:

No Windows 
```bash
   python -m venv venv
   venv\Scripts\activate
```

No macOS e Linux 
```bash
   python3 -m venv venv
   source venv/bin/activate
 ```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Crie o banco de dados
```bash
python manage.py migrate
```

5. Crie um super usuário
```bash
python manage.py createsuperuser
```

6. Rode o servidor
```bash
python manage.py runserver
```

7. Acesse a url http://127.0.0.1:8000/accounts/register/ para criar sua conta e navegar pelo Abrace

**OBS**
Para criação de categorias de projetos entre no django admin e crie as categorias desejadas no model Category. O Login no django admin é feito com Email e senha do super usuário acessando a url http://127.0.0.1:8000/admin. Nunca utilize seu super usuário para navegar pelo sistema Abrace, para isso crie uma conta em http://127.0.0.1:8000/accounts/register/.
