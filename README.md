# 📑 Unificador de PDFs (PDF Merger)

> Uma ferramenta leve, moderna e segura para unir múltiplos arquivos PDF em um único documento, sem limites de quantidade, tamanho ou cobranças de assinaturas.

[![Licença: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow.svg?logo=javascript&logoColor=white)](https://developer.mozilla.org/)
[![Privacidade](https://img.shields.io/badge/Privacidade-100%25%20Local-success.svg)](#-privacidade-e-segurança)

---

## 💡 Por que este projeto?

A maioria dos serviços online (como iLovePDF, Smallpdf) impõe restrições severas: limite de 2 a 3 tarefas por dia, limites de tamanho (MB) ou exigência de planos pagos. Além disso, enviar documentos corporativos, contratos e dados sigilosos para servidores de terceiros pode violar políticas de compliance e LGPD.

Este repositório oferece **duas abordagens complementares e 100% locais**:

1. **Aplicação Web no Navegador (`unificador_pdf.html`)**: Não precisa instalar nada. Basta dar dois cliques e usar no Chrome, Edge ou Firefox.
2. **Aplicação Desktop / Script Python (`unificador_desktop.py` e `merge_pdfs.py`)**: Interface gráfica nativa ou script automatizado usando o motor de alta velocidade do PyMuPDF com geração automática de sumário/marcadores.

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

Ideal para quem busca máxima performance com grandes volumes de páginas.

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
  - Botão **🔢 Ordenação Inteligente**.
  - Checkbox para ativar/desativar a criação de marcadores/sumário.

---

### Opção 3: Script Automatizado via Linha de Comando (CLI)

Se você precisa automatizar a junção de arquivos de forma programática ou em esteiras de rotina:

```bash
python merge_pdfs.py
```

Você pode editar a lista de arquivos e o nome de saída diretamente no script `merge_pdfs.py`.

---

## 📂 Estrutura do Repositório

```text
├── unificador_pdf.html     # Web App completo (HTML5 + CSS3 + pdf-lib)
├── unificador_desktop.py   # Aplicativo Desktop nativo com interface Tkinter
├── merge_pdfs.py           # Script Python para automação direta via terminal
└── README.md               # Documentação do projeto
```

---

## 🛠️ Tecnologias Utilizadas

- **Interface Web:**
  - [PDF-Lib](https://pdf-lib.js.org/) – Manipulação e junção de PDFs direto no navegador.
  - HTML5, CSS3 moderno (Flexbox, CSS Variables) e JavaScript puro (Vanilla JS).
- **Interface Desktop e Scripts:**
  - [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) – Uma das bibliotecas mais rápidas do mercado para processamento de PDFs.
  - [Tkinter](https://docs.python.org/3/library/tkinter.html) – Biblioteca padrão de interface gráfica do Python.

---

## 🔒 Privacidade e Segurança

- **Zero Telemetria:** O código não possui rastreadores, analytics ou chamadas a APIs proprietárias.
- **Conformidade com LGPD / GDPR:** Ideal para documentos jurídicos, contratos, holerites e informações confidenciais que não podem transitar em servidores de terceiros.

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo `LICENSE` para obter mais informações.
