import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import yaml
import uuid
import os
from datetime import datetime
import logging

class QEMUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QEMU GUI")
        self.root.configure(bg="#f0f0f0")

        self.qemu_version = self.check_qemu_version()
        if self.qemu_version:
            self.root.title(f"QEMU GUI (版本: {self.qemu_version})")
        else:
            messagebox.showerror("错误", "未检测到QEMU, 请安装到系统中。")
            self.install_qemu()

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="QEMU路径:", background="#f0f0f0").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.qemu_path = ttk.Entry(main_frame, width=40)
        self.qemu_path.grid(row=0, column=1, pady=5)
        ttk.Button(main_frame, text="浏览", command=self.load_qemu_path).grid(row=0, column=2, padx=5)

        ttk.Label(main_frame, text="虚拟机镜像:", background="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.vm_image = ttk.Entry(main_frame, width=40)
        self.vm_image.grid(row=1, column=1, pady=5)
        ttk.Button(main_frame, text="浏览", command=self.load_image).grid(row=1, column=2, padx=5)

        ttk.Label(main_frame, text="网络配置:", background="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.network_var = ttk.Combobox(main_frame, values=["用户网络", "桥接网络", "主机网络"], state="readonly")
        self.network_var.grid(row=2, column=1, pady=5)
        self.network_var.current(0)
        self.network_var.bind("<<ComboboxSelected>>", self.toggle_bridge_nic_input)

        ttk.Label(main_frame, text="桥接网卡:", background="#f0f0f0").grid(row=2, column=2, sticky=tk.W, padx=5)
        self.bridge_nic_entry = ttk.Entry(main_frame, width=15)
        self.bridge_nic_entry.grid(row=2, column=3, pady=5)
        self.bridge_nic_entry.config(state="disabled")

        ttk.Label(main_frame, text="CPU核心数:", background="#f0f0f0").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cpu_cores = ttk.Entry(main_frame, width=10)
        self.cpu_cores.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="内存(单位MB):", background="#f0f0f0").grid(row=3, column=2, sticky=tk.E, padx=5)
        self.memory_size = ttk.Entry(main_frame, width=10)
        self.memory_size.grid(row=3, column=3)

        self.start_button = ttk.Button(main_frame, text="启动虚拟机", command=self.start_vm, width=15)
        self.start_button.grid(row=4, column=0, pady=10)

        self.save_button = ttk.Button(main_frame, text="保存配置", command=self.save_config, width=15)
        self.save_button.grid(row=4, column=1, pady=10)

        self.load_button = ttk.Button(main_frame, text="读取配置", command=self.load_config, width=15)
        self.load_button.grid(row=4, column=2, pady=10)

        self.output_text = tk.Text(main_frame, height=10, width=70)
        self.output_text.grid(row=5, column=0, columnspan=4, pady=5)
        self.output_text.config(state=tk.DISABLED)

        self.command_input = ttk.Entry(main_frame, width=70)
        self.command_input.grid(row=6, column=0, columnspan=3, pady=5)
        self.command_input.bind("<Return>", self.execute_command)

        self.clear_button = ttk.Button(main_frame, text="清屏", command=self.clear_output, width=15)
        self.clear_button.grid(row=6, column=3, pady=5)

        self.status_label = ttk.Label(main_frame, text="状态信息", background="#f0f0f0")
        self.status_label.grid(row=7, column=0, columnspan=4, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_log_file()

    def create_log_file(self):
        log_dir = 'log'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file_name = f"{uuid.uuid4()}.log"
        log_file_path = os.path.join(log_dir, log_file_name)

        logging.basicConfig(
            filename=log_file_path,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def check_qemu_version(self):
        try:
            result = subprocess.run(['qemu-system-x86_64', '--version'], capture_output=True, text=True)
            return result.stdout.strip()
        except Exception:
            return None

    def install_qemu(self):
        try:
            subprocess.run(['bash', './install.sh'], check=True)
            messagebox.showinfo("信息", "QEMU 安装完成。请重新启动应用。")
            self.root.quit()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"安装失败: {e}")

    def toggle_bridge_nic_input(self, event):
        if self.network_var.get() == "桥接网络":
            self.bridge_nic_entry.config(state="normal")
        else:
            self.bridge_nic_entry.config(state="disabled")
            self.bridge_nic_entry.delete(0, tk.END)

    def log_output(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.yview(tk.END)
        logging.info(message)

    def update_status(self, message):
        self.status_label.config(text=message)

    def load_qemu_path(self):
        qemu_path = filedialog.askdirectory(title="选择QEMU目录")
        if qemu_path:
            self.qemu_path.delete(0, tk.END)
            self.qemu_path.insert(0, qemu_path)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.img;*.qcow2")])
        if file_path:
            self.vm_image.delete(0, tk.END)
            self.vm_image.insert(0, file_path)

    def start_vm(self):
        if not self.qemu_path.get() or not self.vm_image.get():
            messagebox.showerror("错误", "请确保填入QEMU路径和虚拟机镜像。")
            return
        
        try:
            cpu_cores = int(self.cpu_cores.get())
            memory_size = int(self.memory_size.get())
            if cpu_cores <= 0 or memory_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "请输入有效的CPU核心数和内存大小。")
            return

        network_option = self.network_var.get()
        if network_option == "桥接网络":
            bridge_nic = self.bridge_nic_entry.get().strip()
            if not bridge_nic or bridge_nic == "选择网卡":
                messagebox.showerror("错误", "请提供有效的网卡名称。")
                return
            network_option += f",model=virtio,if=bridge,br={bridge_nic}"

        qemu_command = f'{self.qemu_path.get()} -hda {self.vm_image.get()} -m {memory_size} -smp {cpu_cores} -net {network_option}'

        self.log_output(f"正在启动: {qemu_command}")
        self.update_status("虚拟机启动中...")

        try:
            subprocess.run(qemu_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.update_status("虚拟机启动成功！")
            self.log_output("虚拟机启动成功！")
        except subprocess.CalledProcessError as e:
            self.update_status("启动虚拟机失败！")
            error_message = f"启动虚拟机失败: {e.stderr.decode().strip()}"
            self.log_output(error_message)
            messagebox.showerror("错误", error_message)

    def save_config(self):
        config_dir = "configs"
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        config = {
            'qemu_path': self.qemu_path.get(),
            'vm_image': self.vm_image.get(),
            'network_config': self.network_var.get(),
            'cpu_cores': self.cpu_cores.get(),
            'memory_size': self.memory_size.get(),
            'bridge_nic': self.bridge_nic_entry.get()
        }

        file_name = f"config_{uuid.uuid4()}.yaml"
        file_path = os.path.join(config_dir, file_name)

        with open(file_path, 'w') as file:
            yaml.dump(config, file)

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml")])
        if file_path:
            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)
                self.qemu_path.delete(0, tk.END)
                self.qemu_path.insert(0, config.get('qemu_path', ''))
                self.vm_image.delete(0, tk.END)
                self.vm_image.insert(0, config.get('vm_image', ''))
                self.network_var.set(config.get('network_config', '用户网络'))
                self.cpu_cores.delete(0, tk.END)
                self.cpu_cores.insert(0, config.get('cpu_cores', ''))
                self.memory_size.delete(0, tk.END)
                self.memory_size.insert(0, config.get('memory_size', ''))
                self.bridge_nic_entry.delete(0, tk.END)
                self.bridge_nic_entry.insert(0, config.get('bridge_nic', ''))

    def execute_command(self, event=None):
        command = self.command_input.get()
        if command:
            self.log_output(f"执行命令: {command}")
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                self.log_output(result.stdout)
                if result.stderr:
                    self.log_output(f"错误信息: {result.stderr}")
            except Exception as e:
                messagebox.showerror("执行错误", str(e))
            self.command_input.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "请输入要执行的命令。")

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.update_status("日志已清空")
        self.output_text.config(state=tk.DISABLED)

    def on_closing(self):
        try:
            self.save_config()
        finally:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QEMUApp(root)
    root.mainloop()
