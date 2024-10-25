import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class CSVTextReplacer:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Text Replacer")
        self.root.geometry("800x600")
        
        # 데이터 저장 변수
        self.df = None
        self.df_original = None  # 원본 데이터 저장용
        self.current_file_path = None
        
        # UI 구성
        self.create_widgets()
        
    def create_widgets(self):
        # 메뉴바 생성
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 파일 메뉴
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="CSV 파일 열기", command=self.load_csv)
        file_menu.add_command(label="저장", command=self.save_file)
        file_menu.add_command(label="다른 이름으로 저장", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.root.quit)
        
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 파일 선택 영역
        file_frame = ttk.LabelFrame(main_frame, text="파일 선택", padding="5")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state='readonly', width=50)
        self.file_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(file_frame, text="파일 선택", command=self.load_csv).pack(side=tk.LEFT, padx=5)
        
        # 입력 영역
        input_frame = ttk.LabelFrame(main_frame, text="텍스트 교체", padding="5")
        input_frame.pack(fill=tk.X, pady=5)
        
        # 찾을 텍스트
        ttk.Label(input_frame, text="찾을 텍스트:").pack(side=tk.LEFT, padx=5)
        self.text_to_find = ttk.Entry(input_frame, width=20)
        self.text_to_find.pack(side=tk.LEFT, padx=5)
        
        # 바꿀 텍스트
        ttk.Label(input_frame, text="바꿀 텍스트:").pack(side=tk.LEFT, padx=5)
        self.text_to_replace = ttk.Entry(input_frame, width=20)
        self.text_to_replace.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="텍스트 교체", command=self.replace_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="저장", command=self.save_file).pack(side=tk.LEFT, padx=5)
        
        # 프리뷰 영역
        preview_frame = ttk.LabelFrame(main_frame, text="데이터 프리뷰", padding="5")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 트리뷰 생성
        self.tree = ttk.Treeview(preview_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # 스크롤바 추가
        scrollbar_y = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 스타일 설정
        style = ttk.Style()
        style.configure("Modified.Treeview", background="yellow")
        
    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.df_original = self.df.copy()  # 원본 데이터 저장
                self.current_file_path = file_path
                self.file_path_var.set(file_path)
                self.update_treeview()
                messagebox.showinfo("성공", "CSV 파일을 성공적으로 불러왔습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"파일을 불러오는 중 오류가 발생했습니다:\n{str(e)}")
    
    def update_treeview(self, modified_cells=None):
        # 기존 트리뷰 항목 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.df is None:
            return
            
        # 컬럼 설정
        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"
        
        # 컬럼 헤더 설정
        for column in self.df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100, minwidth=50)
        
        # 데이터 추가 및 수정된 셀 하이라이트
        for idx, row in self.df.head(100).iterrows():
            values = list(row)
            item = self.tree.insert("", tk.END, values=values)
            
            # 수정된 셀이 있는 경우 해당 셀만 하이라이트
            if modified_cells and idx in modified_cells:
                # 현재 값을 리스트로 가져오기
                current_values = list(values)
                # 수정된 셀의 배경색을 노란색으로 설정
                for col_idx in modified_cells[idx]:
                    # 트리뷰의 값을 업데이트하여 수정된 셀만 하이라이트
                    self.tree.set(item, col_idx, f"*{current_values[col_idx]}*")
                    self.tree.tag_configure(f'modified_{col_idx}', background='yellow')
                    self.tree.item(item, tags=(f'modified_{col_idx}',))
            
    def replace_text(self):
        if self.df is None:
            messagebox.showwarning("경고", "먼저 CSV 파일을 불러와주세요.")
            return
            
        text_to_find = self.text_to_find.get()
        text_to_replace = self.text_to_replace.get()
        
        if not text_to_find:
            messagebox.showwarning("경고", "찾을 텍스트를 입력해주세요.")
            return
            
        # 변경된 셀 추적을 위한 딕셔너리
        modified_cells = {}
        total_modifications = 0
        
        # 모든 문자열 컬럼에서 텍스트 교체
        for col_idx, column in enumerate(self.df.select_dtypes(include=['object']).columns):
            # 원본 값 저장
            original_values = self.df_original[column].astype(str)
            # 텍스트 교체
            self.df[column] = self.df[column].astype(str).str.replace(text_to_find, text_to_replace)
            
            # 변경된 셀 찾기
            changed_mask = original_values != self.df[column]
            for idx in changed_mask[changed_mask].index:
                if idx not in modified_cells:
                    modified_cells[idx] = set()
                modified_cells[idx].add(col_idx)
                total_modifications += 1
        
        self.update_treeview(modified_cells)
        messagebox.showinfo("수정 완료", f"총 {total_modifications}개의 항목이 수정되었습니다.")
        
    def save_file(self):
        if self.df is None:
            messagebox.showwarning("경고", "저장할 데이터가 없습니다.")
            return
            
        if self.current_file_path:
            try:
                self.df.to_csv(self.current_file_path, index=False)
                # 저장 후 현재 데이터를 새로운 원본으로 설정
                self.df_original = self.df.copy()
                messagebox.showinfo("성공", "파일이 성공적으로 저장되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"파일 저장 중 오류가 발생했습니다:\n{str(e)}")
        else:
            self.save_file_as()
            
    def save_file_as(self):
        if self.df is None:
            messagebox.showwarning("경고", "저장할 데이터가 없습니다.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.df.to_csv(file_path, index=False)
                self.current_file_path = file_path
                self.file_path_var.set(file_path)
                # 저장 후 현재 데이터를 새로운 원본으로 설정
                self.df_original = self.df.copy()
                messagebox.showinfo("성공", "파일이 성공적으로 저장되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"파일 저장 중 오류가 발생했습니다:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVTextReplacer(root)
    root.mainloop()
