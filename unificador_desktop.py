import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import fitz  # PyMuPDF
import os
import re
import threading

class UnificadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unificador de PDFs - PyMuPDF")
        self.root.geometry("720x560")
        self.root.minsize(600, 450)

        self.arquivos = []

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")

        # Top Frame - Botões de ação rápida
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

        # Middle Frame - Lista de arquivos e controles laterais
        mid_frame = ttk.Frame(root, padding=10)
        mid_frame.pack(fill=tk.BOTH, expand=True)

        # Lista de arquivos com scrollbar
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

        # Botões de mover para cima/baixo
        ctrl_frame = ttk.Frame(mid_frame, padding=5)
        ctrl_frame.pack(side=tk.RIGHT, fill=tk.Y)

        btn_up = ttk.Button(ctrl_frame, text="▲ Subir", command=self.mover_cima)
        btn_up.pack(fill=tk.X, pady=4)

        btn_down = ttk.Button(ctrl_frame, text="▼ Descer", command=self.mover_baixo)
        btn_down.pack(fill=tk.X, pady=4)

        btn_del = ttk.Button(ctrl_frame, text="✕ Remover", command=self.remover_selecionado)
        btn_del.pack(fill=tk.X, pady=4)

        # Bottom Frame - Configuração de saída e Unificar
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
        # Ordenação natural numérica (ex: ad1, ad2... ad10, ad14)
        def natural_sort_key(s):
            return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', os.path.basename(s))]
        self.arquivos.sort(key=natural_sort_key)
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
        thread = threading.Thread(target=self.processar_unificacao, args=(caminho_saida,), daemon=True)
        thread.start()

    def processar_unificacao(self, caminho_saida):
        try:
            total = len(self.arquivos)
            merged = fitz.open()
            toc = []
            pagina_atual = 1

            for i, arq in enumerate(self.arquivos):
                nome_base = os.path.splitext(os.path.basename(arq))[0]
                self.lbl_status.config(text=f"Processando ({i+1}/{total}): {nome_base}...")
                self.progress["value"] = ((i) / total) * 100
                self.root.update_idletasks()

                sub = fitz.open(arq)
                qtd_paginas = len(sub)
                
                if self.check_toc.get():
                    toc.append([1, nome_base, pagina_atual])
                
                merged.insert_pdf(sub)
                pagina_atual += qtd_paginas
                sub.close()

            if self.check_toc.get():
                merged.set_toc(toc)

            self.lbl_status.config(text="Salvando e otimizando arquivo...")
            self.progress["value"] = 98
            self.root.update_idletasks()

            merged.save(caminho_saida, garbage=3, deflate=True)
            merged.close()

            self.progress["value"] = 100
            self.lbl_status.config(text=f"Concluído! Salvo em: {os.path.basename(caminho_saida)}")
            
            messagebox.showinfo(
                "Sucesso!",
                f"PDF Unificado com sucesso!\n\nTotal de páginas: {pagina_atual - 1}\nSalvo em: {caminho_saida}"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao unir os arquivos:\n{str(e)}")
        finally:
            self.btn_merge.config(state=tk.NORMAL)
            self.progress["value"] = 0

if __name__ == "__main__":
    janela = tk.Tk()
    app = UnificadorApp(janela)
    janela.mainloop()
