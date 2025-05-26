# Registro de Treino

Um aplicativo web para gerenciar seus treinos de academia, permitindo criar, organizar e acompanhar exercícios com dados detalhados de séries, repetições e cargas.

## Funcionalidades

- Criação e gerenciamento de treinos
- Controle de séries de preparação e séries eficazes
- Timer de descanso entre séries
- Registro de pesos e repetições
- Interface intuitiva e responsiva

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/registro-treino.git
cd registro-treino
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o aplicativo:
```bash
python app.py
```

5. Acesse o aplicativo em seu navegador:
```
http://localhost:5000
```

## Estrutura do Projeto

```
registro-treino/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências
├── static/            # Arquivos estáticos
│   └── notification.mp3
└── templates/         # Templates HTML
    ├── base.html
    ├── home.html
    ├── treino.html
    ├── exercicio.html
    └── novo_treino.html
```

## Uso

1. Na página inicial, você verá a lista de seus treinos
2. Clique em "Novo Treino" para criar um treino
3. Adicione exercícios ao treino com suas configurações
4. Inicie o treino e acompanhe seu progresso
5. Use o timer de descanso entre as séries

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes. 