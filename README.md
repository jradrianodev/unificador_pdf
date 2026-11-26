# 📑 Unificador de PDFs (PDF Merger)

> Uma ferramenta leve, moderna e segura para unir múltiplos arquivos PDF em um único documento, sem limites de quantidade, tamanho ou cobranças de assinaturas.

[![Licença: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow.svg?logo=javascript&logoColor=white)](https://developer.mozilla.org/)
[![Privacidade](https://img.shields.io/badge/Privacidade-100%25%20Local-success.svg)](#-privacidade-e-segurança)

---

## 💡 Por que este projeto?

A maioria dos serviços online (como iLovePDF, Smallpdf) impõe restrições severas: limite de 2 a 3 tarefas por dia, limites de tamanho (MB) ou exigência de planos pagos. Além disso, enviar documentos corporativos, contratos e dados sigilosos para servidores de terceiros pode violar políticas de compliance e LGPD.

Este repositório oferece **duas soluções complementares e 100% locais**:

1. **Aplicação Web no Navegador (`unificador_pdf.html`)**: Não precisa instalar nada. Basta dar dois cliques e usar no Chrome, Edge ou Firefox com suporte a *drag & drop*.
2. **Aplicação Desktop Nativa (`unificador_desktop.py`)**: Interface gráfica nativa para Windows/Linux/macOS usando o motor de alta performance do PyMuPDF, com geração automática de sumário e marcadores.

---

## ✨ Funcionalidades Principais

- ♾️ **Uploads Ilimitados**: Adicione dezenas ou centenas de arquivos sem qualquer restrição de quantidade ou tamanho.
- 🔒 **100% Offline e Privado**: O processamento é realizado no seu próprio computador. Nenhum documento é enviado para a internet.
- 🔢 **Ordenação Inteligente (Natural Sort)**: Reconhece numerações nos nomes dos arquivos (ex: organiza `contrato_ad1.pdf` até `contrato_ad14.pdf` na ordem correta, sem colocar o `ad10` após o `ad1`).
- 📑 **Sumário e Marcadores Automáticos**: O PDF gerado já vem com índice clicável na barra lateral com o título de cada documento.
- 🔄 **Reorganização Flexível**: Mova itens para cima/baixo ou remova arquivos individuais antes de unificar.
- 🗜️ **Otimização Automática**: Compressão e limpeza de objetos duplicados para manter o PDF final leve.

---

## 🚀 Como Usar

### Opção 1: No Navegador (Sem Instalação)

Ideal para uso rápido no dia a dia ou para compartilhar com colegas de equipe que não possuem ambiente Python instalado.

1. Baixe ou clone o repositório.
2. Dê um **duplo clique** no arquivo `unificador_pdf.html`.
3. Arraste seus arquivos PDF para a área indicada (ou clique para selecionar).
4. Clique em **"Ordenação Inteligente"** para ordenar automaticamente ou use as setas para ajustar.
5. Clique em **"⚡ Unificar e Baixar Arquivo"**.

---

### Opção 2: Aplicativo Desktop (Interface Gráfica com Python)

Ideal para quem busca máxima performance com grandes volumes de páginas ou quer processar uma pasta inteira com um clique.

#### Pré-requisitos
- Python 3.8 ou superior instalado.
- Biblioteca `PyMuPDF`:
  ```bash
  pip install pymupdf
  ```

#### Executando a interface:
```bash
python unificador_desktop.py
```

* **Recursos da interface:**
  - Botão **➕ Adicionar PDFs** (seleção múltipla).
  - Botão **📁 Adicionar Pasta** (carrega todos os PDFs de um diretório de uma só vez).
  - Botão **🔢 Ordenação Inteligente** (ordena naturalmente por números nos nomes).
  - Botões **▲ Subir** e **▼ Descer** para ajuste manual de posição.
  - Checkbox para ativar/desativar a criação de marcadores/sumário clicáveis no PDF final.

---

## 🤖 Uso com Assistentes de IA (Antigravity, Claude & ChatGPT)

O arquivo `unificador_desktop.py` foi construído com arquitetura híbrida (**GUI + CLI + Módulo Python**). Isso significa que enquanto humanos podem usá-lo com interface gráfica de janelas, assistentes de IA e agentes autônomos podem acioná-lo diretamente sem abrir janelas.

### 1. Com o Antigravity (Google DeepMind)
O Antigravity pode chamar a ferramenta de duas formas no seu fluxo de trabalho:

- **Via Terminal / Shell Tool:**
  ```powershell
  python unificador_desktop.py --dir "." --output "documento_unificado.pdf"
  ```
- **Via Importação Direta em Scripts Python:**
  ```python
  from unificador_desktop import unificar_pdfs, ordenar_arquivos

  arquivos = ordenar_arquivos(["contrato.pdf", "contrato_ad1.pdf", "contrato_ad2.pdf"])
  resultado = unificar_pdfs(arquivos, caminho_saida="resultado.pdf", criar_sumario=True)
  print(f"Gerado: {resultado['arquivo_saida']} com {resultado['total_paginas']} páginas.")
  ```

**Prompt de exemplo para o Antigravity:**
> *"Antigravity, use o `unificador_desktop.py` para juntar todos os PDFs desta pasta em ordem cronológica de aditivos, gerando o sumário como 'contrato_completo.pdf'."*

---

### 2. Com o Claude (Claude Code / Terminal / API)
O Claude Code pode executar comandos de terminal nativamente para gerenciar seus arquivos e executar a ferramenta:

**Comando direto via CLI que o Claude executa:**
```bash
python unificador_desktop.py --dir "/caminho/dos/documentos" -o "saida.pdf"
```

**Prompt de exemplo para o Claude:**
> *"Claude, examine os PDFs desta pasta e execute o script `unificador_desktop.py` passando os arquivos em ordem numérica para gerar um único PDF unificado."*

---

### 3. Com o ChatGPT (Code Interpreter / Análise Avançada de Dados)
Ao subir seus arquivos e o `unificador_desktop.py` em uma sessão de chat do ChatGPT com suporte a código:

**Prompt de exemplo para o ChatGPT:**
> *"Execute a função `unificar_pdfs()` do `unificador_desktop.py` com os PDFs que acabei de enviar, criando o sumário automático com o nome de cada arquivo e disponibilize o link para download."*

---

### 🛠️ Parâmetros da Linha de Comando (CLI para Agentes)

| Parâmetro | Descrição | Exemplo |
| :--- | :--- | :--- |
| `-d`, `--dir` | Caminho do diretório contendo os PDFs | `--dir "./documentos"` |
| `arquivos` | Lista posicional de PDFs específicos | `doc1.pdf doc2.pdf doc3.pdf` |
| `-o`, `--output` | Nome ou caminho do arquivo consolidado | `-o "final.pdf"` |
| `--no-sort` | Desativa a ordenação natural numérica | `--no-sort` |
| `--no-toc` | Desativa a criação de marcadores/sumário | `--no-toc` |

---

## 📂 Estrutura do Repositório

```text
├── unificador_pdf.html     # Web App completo (HTML5 + CSS3 + pdf-lib)
├── unificador_desktop.py   # Aplicativo Desktop nativo com interface Tkinter + PyMuPDF
├── .gitignore              # Protege arquivos *.pdf de serem commitados por engano
└── README.md               # Documentação completa do projeto
```

---

## 🛠️ Tecnologias Utilizadas

- **Interface Web:**
  - [PDF-Lib](https://pdf-lib.js.org/) – Manipulação e junção de PDFs direto no navegador.
  - HTML5, CSS3 moderno (Flexbox, CSS Variables) e JavaScript puro (Vanilla JS).
- **Interface Desktop:**
  - [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) – Uma das bibliotecas mais rápidas do mercado para processamento de PDFs.
  - [Tkinter](https://docs.python.org/3/library/tkinter.html) – Biblioteca nativa de interface gráfica do Python.

---

## 🔒 Privacidade e Segurança

- **Zero Telemetria:** O código não possui rastreadores, analytics ou chamadas a APIs proprietárias.
- **Conformidade com LGPD / GDPR:** Ideal para documentos jurídicos, contratos, holerites e informações confidenciais que não podem transitar em servidores de terceiros.

---

## 📄 Licença

Distribuído sob a licença **MIT**.
