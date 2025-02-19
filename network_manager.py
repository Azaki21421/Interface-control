import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import psutil
import os
import sys
import ctypes
import socket


class NetworkManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Manager")
        self.interfaces = []
        self.new_interfaces = set()

        self.interface_frame = ttk.Frame(self.root)
        self.interface_frame.pack(fill=tk.BOTH, expand=True)

        self.add_interface_button = ttk.Button(self.root, text="Add Interface", command=self.add_interface)
        self.add_interface_button.pack(side=tk.LEFT)

        self.remove_interface_button = ttk.Button(self.root, text="Remove Interface", command=self.remove_interface)
        self.remove_interface_button.pack(side=tk.LEFT)

        self.route_button = ttk.Button(self.root, text="Assign Routes", command=self.route_traffic)
        self.route_button.pack(side=tk.LEFT)

        self.update_interfaces()

    def update_interfaces(self):
        for widget in self.interface_frame.winfo_children():
            widget.destroy()

        self.interfaces = list(psutil.net_if_addrs().keys())
        for i, interface in enumerate(self.interfaces):
            label_text = f"{i + 1}. {interface}"

            if interface in self.new_interfaces:
                label_text += " *new*"

            label = ttk.Label(self.interface_frame, text=label_text)
            label.grid(row=i * 2, column=0, padx=10, pady=5)

            if i > 0:
                ttk.Separator(self.interface_frame, orient="horizontal").grid(row=i * 2 - 1, column=0, sticky="ew",
                                                                              pady=5)

    def add_interface(self):
        new_interface_name = simpledialog.askstring("Add Interface", "Enter the name of the new interface:")
        if not new_interface_name:
            return

        try:
            command = f'"tapctl.exe" create --hwid root\\tap0901 --name {new_interface_name}'
            subprocess.check_call(command, shell=True)
            self.new_interfaces.add(new_interface_name)
            self.update_interfaces()
            messagebox.showinfo("Success", f"Interface {new_interface_name} created successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create the interface. Error: {e}")

    def remove_interface(self):
        interface = simpledialog.askstring("Remove Interface", "Enter the name of the interface to remove:")
        if not interface:
            return

        try:
            command = f'"tapctl.exe" delete {interface}'
            subprocess.check_call(command, shell=True)
            self.new_interfaces.discard(interface)
            self.update_interfaces()
            messagebox.showinfo("Success", f"Interface {interface} removed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to remove the interface. Error: {e}")

    def route_traffic(self):
        app_window = tk.Toplevel(self.root)
        app_window.title("Select Application")
        app_window.geometry("500x400")

        columns = ("PID", "Name")
        process_tree = ttk.Treeview(app_window, columns=columns, show="headings", height=15)
        process_tree.pack(fill=tk.BOTH, expand=True)

        process_tree.heading("PID", text="PID", command=lambda: sort_column(process_tree, "PID", False))
        process_tree.heading("Name", text="Name", command=lambda: sort_column(process_tree, "Name", False))
        process_tree.column("PID", width=100, anchor="center")
        process_tree.column("Name", width=350, anchor="w")

        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                processes.append((proc.info['pid'], proc.info['name']))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        for pid, name in processes:
            process_tree.insert("", tk.END, values=(pid, name))

        def sort_column(tree, col, reverse):
            data_list = [(tree.set(item, col), item) for item in tree.get_children("")]

            if col == "PID":
                data_list.sort(key=lambda x: int(x[0]), reverse=reverse)
            else:
                data_list.sort(key=lambda x: x[0].lower(), reverse=reverse)

            for index, (val, item) in enumerate(data_list):
                tree.move(item, "", index)

            tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

        def select_process():
            selected_item = process_tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Select an application.")
                return
            selected_values = process_tree.item(selected_item[0], "values")
            pid = int(selected_values[0])
            app_window.destroy()
            self.assign_route(pid)

        select_button = ttk.Button(app_window, text="Select", command=select_process)
        select_button.pack(pady=10)

    def assign_route(self, pid):
        try:
            process = psutil.Process(pid)
            exe_path = process.exe()

            interface_num = int(simpledialog.askstring("Interface", "Enter the number of the interface for routing:"))
            if interface_num < 1 or interface_num > len(self.interfaces):
                messagebox.showerror("Error", "Invalid interface number.")
                return

            interface = self.interfaces[interface_num - 1]

            interface_ip = None
            for addr in psutil.net_if_addrs().get(interface, []):

                if addr.family == socket.AF_INET:
                    interface_ip = addr.address
                    break

            if not interface_ip:
                messagebox.showerror("Error", f"Failed to find IP address for interface {interface}.")
                return

            forcebindip_path = r"ForceBindIP\ForceBindIP.exe"
            if not os.path.exists(forcebindip_path):
                messagebox.showerror("Error", "ForceBindIP not found. Make sure it is installed.")
                return

            command = f'"{forcebindip_path}" {interface_ip} "{exe_path}"'
            subprocess.Popen(command, shell=True)
            messagebox.showinfo("Success", f"Application launched through interface {interface} with IP {interface_ip}.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid interface number.")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", "Process not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch the application through ForceBindIP. Error: {e}")

    def get_pid(self, app_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == app_name:
                return proc.info['pid']
        return None

    def get_main_interface_ip(self):
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith("169"):
                    return addr.address
        return None


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        return os.geteuid() == 0


if __name__ == "__main__":
    if is_admin():
        root = tk.Tk()
        app = NetworkManagerApp(root)
        root.mainloop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
