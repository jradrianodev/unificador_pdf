import os
import re
import sys
import argparse
import fitz  # PyMuPDF

def ordenar_arquivos(lista):
    """Ordenação natural inteligente reconhecendo números nos nomes (ex: ad1, ad2... ad10, ad14)"""
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', os.path.basename(s))]
    return sorted(lista, key=natural_sort_key)

def unificar_pdfs(arquivos, caminho_saida, criar_sumario=True, callback_progresso=None):
    """
    Função modular para unificação de PDFs.
    Pode ser importada e utilizada diretamente por agentes de IA (Antigravity, Claude, ChatGPT)
    ou chamada via linha de comando (CLI).
    """
    if not arquivos:
        raise ValueError("A lista de arquivos para unificar está vazia.")

    total = len(arquivos)
    merged = fitz.open()
    toc = []
    pagina_atual = 1

    for i, arq in enumerate(arquivos):
        if not os.path.exists(arq):
            print(f"[Aviso] Arquivo não encontrado: {arq}")
            continue

        nome_base = os.path.splitext(os.path.basename(arq))[0]
        if callback_progresso:
            callback_progresso(i + 1, total, nome_base)
        else:
            print(f"[{i + 1}/{total}] Processando: {nome_base}...")

        sub = fitz.open(arq)
        qtd_paginas = len(sub)
        
        if criar_sumario:
            toc.append([1, nome_base, pagina_atual])
        
        merged.insert_pdf(sub)
        pagina_atual += qtd_paginas
        sub.close()

    if criar_sumario:
        merged.set_toc(toc)

    # Otimização e compressão de disco
    merged.save(caminho_saida, garbage=3, deflate=True)
    merged.close()

    total_paginas = pagina_atual - 1
    return {
        "arquivo_saida": caminho_saida,
        "total_paginas": total_paginas,
        "total_arquivos": total
    }

# ==========================================
# Interface Gráfica Tkinter (Modo Desktop)
# ==========================================
def iniciar_gui():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    import threading

    class UnificadorApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Unificador de PDFs - PyMuPDF")
            self.root.geometry("720x560")
            self.root.minsize(600, 450)

            self.arquivos = []

            style = ttk.Style()
            style.theme_use("clam")

            top_frame = ttk.Frame(root, padding=10)
            top_frame.pack(fill=tk.X)

            btn_add = ttk.Button(top_frame, text="➕ Adicionar PDFs", command=self.adicionar_arquivos)
            btn_add.pack(side=tk.LEFT, padx=5)

            btn_add_dir = ttk.Button(top_frame, text="📁 Adicionar Pasta", command=self.adicionar_pasta)
            btn_add_dir.pack(side=tk.LEFT, padx=5)

            btn_sort = ttk.Button(top_frame, text="🔢 Ordenação Inteligente", command=self.ordenar_inteligente)
            btn_sort.pack(side=tk.LEFT, padx=5)

            btn_clear = ttk.Button(top_frame, text="🗑️ Limpar Tudo", command=self.limpar_tudo)
            btn_clear.pack(side=tk.RIGHT, padx=5)

            mid_frame = ttk.Frame(root, padding=10)
            mid_frame.pack(fill=tk.BOTH, expand=True)

            list_container = ttk.Frame(mid_frame)
            list_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL)
            self.listbox = tk.Listbox(
                list_container, 
                selectmode=tk.SINGLE, 
                font=("Segoe UI", 10), 
                yscrollcommand=self.scrollbar.set
            )
            self.scrollbar.config(command=self.listbox.yview)

            self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            ctrl_frame = ttk.Frame(mid_frame, padding=5)
            ctrl_frame.pack(side=tk.RIGHT, fill=tk.Y)

            btn_up = ttk.Button(ctrl_frame, text="▲ Subir", command=self.mover_cima)
            btn_up.pack(fill=tk.X, pady=4)

            btn_down = ttk.Button(ctrl_frame, text="▼ Descer", command=self.mover_baixo)
            btn_down.pack(fill=tk.X, pady=4)

            btn_del = ttk.Button(ctrl_frame, text="✕ Remover", command=self.remover_selecionado)
            btn_del.pack(fill=tk.X, pady=4)

            bot_frame = ttk.Frame(root, padding=10)
            bot_frame.pack(fill=tk.X)

            self.lbl_status = ttk.Label(bot_frame, text="Nenhum arquivo adicionado.")
            self.lbl_status.pack(anchor=tk.W, pady=2)

            self.progress = ttk.Progressbar(bot_frame, orient=tk.HORIZONTAL, mode="determinate")
            self.progress.pack(fill=tk.X, pady=6)

            action_frame = ttk.Frame(bot_frame)
            action_frame.pack(fill=tk.X, pady=4)

            self.check_toc = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(action_frame, text="Criar sumário/marcadores com o nome dos arquivos", variable=self.check_toc)
            chk.pack(side=tk.LEFT)

            self.btn_merge = ttk.Button(action_frame, text="⚡ Unificar PDFs Agora", command=self.iniciar_unificacao)
            self.btn_merge.pack(side=tk.RIGHT)

        def atualizar_lista(self):
            self.listbox.delete(0, tk.END)
            for idx, arq in enumerate(self.arquivos, start=1):
                nome = os.path.basename(arq)
                self.listbox.insert(tk.END, f"{idx:02d}. {nome}")
            self.lbl_status.config(text=f"Total: {len(self.arquivos)} arquivo(s) selecionado(s)")

        def adicionar_arquivos(self):
            arquivos_selecionados = filedialog.askopenfilenames(
                title="Selecione os PDFs",
                filetypes=[("Arquivos PDF", "*.pdf")]
            )
            if arquivos_selecionados:
                for f in arquivos_selecionados:
                    if f not in self.arquivos:
                        self.arquivos.append(f)
                self.atualizar_lista()

        def adicionar_pasta(self):
            pasta = filedialog.askdirectory(title="Selecione uma pasta com PDFs")
            if pasta:
                encontrados = []
                for item in os.listdir(pasta):
                    if item.lower().endswith(".pdf"):
                        caminho_completo = os.path.join(pasta, item)
                        if caminho_completo not in self.arquivos:
                            encontrados.append(caminho_completo)
                self.arquivos.extend(encontrados)
                self.atualizar_lista()

        def ordenar_inteligente(self):
            self.arquivos = ordenar_arquivos(self.arquivos)
            self.atualizar_lista()

        def limpar_tudo(self):
            self.arquivos.clear()
            self.atualizar_lista()

        def mover_cima(self):
            sel = self.listbox.curselection()
            if not sel or sel[0] == 0:
                return
            idx = sel[0]
            self.arquivos[idx], self.arquivos[idx - 1] = self.arquivos[idx - 1], self.arquivos[idx]
            self.atualizar_lista()
            self.listbox.selection_set(idx - 1)

        def mover_baixo(self):
            sel = self.listbox.curselection()
            if not sel or sel[0] >= len(self.arquivos) - 1:
                return
            idx = sel[0]
            self.arquivos[idx], self.arquivos[idx + 1] = self.arquivos[idx + 1], self.arquivos[idx]
            self.atualizar_lista()
            self.listbox.selection_set(idx + 1)

        def remover_selecionado(self):
            sel = self.listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            del self.arquivos[idx]
            self.atualizar_lista()

        def iniciar_unificacao(self):
            if not self.arquivos:
                messagebox.showwarning("Atenção", "Selecione pelo menos um arquivo PDF para unificar.")
                return

            caminho_saida = filedialog.asksaveasfilename(
                title="Salvar PDF Unificado Como",
                defaultextension=".pdf",
                filetypes=[("Arquivo PDF", "*.pdf")],
                initialfile="documento_unificado.pdf"
            )
            if not caminho_saida:
                return

            self.btn_merge.config(state=tk.DISABLED)
            thread = threading.Thread(target=self.processar_gui, args=(caminho_saida,), daemon=True)
            thread.start()

        def processar_gui(self, caminho_saida):
            try:
                def progresso(i, total, nome):
                    self.lbl_status.config(text=f"Processando ({i}/{total}): {nome}...")
                    self.progress["value"] = (i / total) * 100
                    self.root.update_idletasks()

                res = unificar_pdfs(
                    self.arquivos, 
                    caminho_saida, 
                    criar_sumario=self.check_toc.get(),
                    callback_progresso=progresso
                )

                self.progress["value"] = 100
                self.lbl_status.config(text=f"Concluído! Salvo em: {os.path.basename(caminho_saida)}")
                
                messagebox.showinfo(
                    "Sucesso!",
                    f"PDF Unificado com sucesso!\n\nTotal de páginas: {res['total_paginas']}\nSalvo em: {caminho_saida}"
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao unir os arquivos:\n{str(e)}")
            finally:
                self.btn_merge.config(state=tk.NORMAL)
                self.progress["value"] = 0

    janela = tk.Tk()
    app = UnificadorApp(janela)
    janela.mainloop()

# ==========================================
# CLI / Linha de comando para Agentes e Scripts
# ==========================================
def executar_cli():
    parser = argparse.ArgumentParser(
        description="Unificador de PDFs para Agentes de IA (Antigravity, Claude, ChatGPT) e Terminal."
    )
    parser.add_argument("arquivos", nargs="*", help="Lista de arquivos PDF específicos para unir.")
    parser.add_argument("-d", "--dir", dest="diretorio", help="Caminho da pasta onde estão os PDFs.")
    parser.add_argument("-o", "--output", default="documento_unificado.pdf", help="Nome/caminho do arquivo de saída.")
    parser.add_argument("--no-sort", action="store_true", help="Desativa a ordenação natural inteligente.")
    parser.add_argument("--no-toc", action="store_true", help="Desativa a geração do sumário/marcadores.")

    args = parser.parse_args()

    lista_arquivos = []
    if args.diretorio:
        if not os.path.exists(args.diretorio):
            print(f"Erro: O diretório '{args.diretorio}' não existe.")
            sys.exit(1)
        for item in os.listdir(args.diretorio):
            if item.lower().endswith(".pdf"):
                lista_arquivos.append(os.path.join(args.diretorio, item))
    
    if args.arquivos:
        lista_arquivos.extend(args.arquivos)

    if not lista_arquivos:
        print("Erro: Nenhum arquivo PDF informado ou encontrado. Use --dir ou passe a lista de arquivos.")
        sys.exit(1)

    if not args.no_sort:
        lista_arquivos = ordenar_arquivos(lista_arquivos)

    print(f"Iniciando unificação de {len(lista_arquivos)} arquivo(s)...")
    resultado = unificar_pdfs(
        lista_arquivos, 
        caminho_saida=args.output, 
        criar_sumario=not args.no_toc
    )

    print(f"\n✅ Sucesso!")
    print(f"Arquivo gerado: {resultado['arquivo_saida']}")
    print(f"Total de páginas: {resultado['total_paginas']}")
    print(f"Total de arquivos unidos: {resultado['total_arquivos']}")

if __name__ == "__main__":
    # Se recebeu argumentos de linha de comando, roda em modo CLI/Agent
    if len(sys.argv) > 1:
        executar_cli()
    else:
        # Se chamado sem argumentos (duplo clique ou 'python unificador_desktop.py'), abre a janela gráfica
        iniciar_gui()
