# 📖 Livro Digital de Amor (Python + Streamlit)

Versão em **Python** do livro digital interativo de amor.

Crie um livro romântico personalizado com fotos, textos, datas especiais e visualize página por página.

## ✨ Funcionalidades

- Tela inicial romântica
- Formulário de personalização (nomes, datas, mensagem)
- Upload e gerenciamento de fotografias (com compressão)
- Escolha de foto de capa e legendas
- Editor de 10 páginas pré-configuradas (todas editáveis)
- Datas especiais com contagem regressiva
- Visualização página a página com navegação
- Download dos dados em JSON
- Interface bonita com tema rosa/bege

## 🚀 Como rodar

```bash
# 1. Entre na pasta
cd livro-amor-python

# 2. (Recomendado) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
# ou
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o app
streamlit run app.py
```

O navegador abrirá automaticamente em **http://localhost:8501**

## 📦 Dependências

- `streamlit` — interface web
- `Pillow` — processamento e compressão de imagens
- `streamlit-option-menu` — (opcional, já tratado)

## 📁 Estrutura

```
livro-amor-python/
├── app.py              # Aplicação completa
├── requirements.txt
└── README.md
```

## 💡 Observações

- Os dados ficam na sessão do navegador (enquanto a aba estiver aberta).
- Para persistência permanente, você pode integrar com banco de dados (SQLite, PostgreSQL, Supabase, etc.).
- Para gerar PDF profissional, pode-se adicionar `reportlab` ou `fpdf2` depois.

Feito com ❤️ em Python.
