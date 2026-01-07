import subprocess
import sys
import os
import platform
import time
import signal
import threading

# 颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def print(message, color=ENDC):
        if platform.system() == 'Windows':
            # Windows CMD 可能不支持 ANSI 颜色，简单打印
            print(message)
        else:
            print(f"{color}{message}{Colors.ENDC}")

def run_command(command, cwd, name):
    """运行命令并打印输出"""
    Colors.print(f"[{name}] 正在启动...", Colors.BLUE)
    
    # 根据系统决定是否使用 shell
    is_windows = platform.system() == 'Windows'
    shell = True
    
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=shell,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            # universal_newlines=True
            # 直接继承父进程的 stdout/stderr，这样输出会有颜色且实时
        )
        return process
    except Exception as e:
        Colors.print(f"[{name}] 启动失败: {e}", Colors.FAIL)
        return None

import socket

def check_port(port):
    """检查端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """尝试终止占用端口的进程 (仅限 Windows)"""
    if platform.system() == 'Windows':
        try:
            # 查找占用端口的 PID
            output = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
            lines = output.strip().split('\n')
            for line in lines:
                parts = line.strip().split()
                if len(parts) > 4:
                    pid = parts[-1]
                    Colors.print(f"发现端口 {port} 被进程 {pid} 占用，正在终止...", Colors.WARNING)
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def main():
    # 获取项目根目录
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, 'backend')
    frontend_dir = os.path.join(root_dir, 'frontend')

    # 检测操作系统
    system = platform.system()
    Colors.print(f"检测到操作系统: {system}", Colors.BOLD)

    # 检查并清理端口 (后端 8010, 前端 5173)
    if system == 'Windows':
        for port in [8010, 5173]:
            if check_port(port):
                kill_process_on_port(port)
                time.sleep(1) # 等待释放

    # 定义命令
    if system == 'Windows':
        backend_cmd = "uv run uvicorn app.main:app --reload --port 8010"
        frontend_cmd = "npm run dev"
    else:
        # Linux / macOS
        backend_cmd = "uv run uvicorn app.main:app --reload --port 8010"
        frontend_cmd = "npm run dev"

    processes = []

    try:
        # 启动后端
        backend_process = run_command(backend_cmd, backend_dir, "Backend")
        if backend_process:
            processes.append(backend_process)
        
        # 稍等一下再启动前端，让后端先初始化
        time.sleep(2)

        # 启动前端
        frontend_process = run_command(frontend_cmd, frontend_dir, "Frontend")
        if frontend_process:
            processes.append(frontend_process)

        Colors.print("\n所有服务已启动。按 Ctrl+C 停止服务。\n", Colors.GREEN)

        # 保持主线程运行，直到收到中断信号
        while True:
            time.sleep(1)
            # 检查子进程是否还在运行
            if backend_process.poll() is not None:
                Colors.print("[Backend] 已停止", Colors.WARNING)
                break
            if frontend_process.poll() is not None:
                Colors.print("[Frontend] 已停止", Colors.WARNING)
                break

    except KeyboardInterrupt:
        Colors.print("\n正在停止服务...", Colors.WARNING)
    finally:
        # 终止所有子进程
        for p in processes:
            if p.poll() is None:
                if system == 'Windows':
                    # Windows 下 terminate 可能无法杀死 shell 启动的子进程树
                    subprocess.run(f"taskkill /F /T /PID {p.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        Colors.print("服务已全部停止。", Colors.GREEN)

if __name__ == "__main__":
    main()
