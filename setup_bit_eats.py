import subprocess
import os
import sys

REPO_URL = "git@github.com:Tecnizium/bit_eats.git"
INSTALL_DIR = "C:\\BitEats"
SSH_KEY_PATH = os.path.expanduser("~/.ssh/id_rsa")

def generate_ssh_key():
    try:
        if not os.path.exists(SSH_KEY_PATH):
            print("Gerando chave SSH...")
            subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", SSH_KEY_PATH, "-N", ""], check=True)
            print("Chave SSH gerada com sucesso.")
        else:
            print("Chave SSH já existe.")
    except Exception as e:
        print(f"Erro ao gerar chave SSH: {e}")

def show_ssh_key():
    try:
        with open(f"{SSH_KEY_PATH}.pub", "r") as file:
            ssh_key = file.read()
        print("\nAdicione a seguinte chave SSH ao seu GitHub:\n")
        print(ssh_key)
        input("Pressione Enter depois de adicionar a chave ao GitHub e configurar o SSH agent...")
    except Exception as e:
        print(f"Erro ao mostrar chave SSH: {e}")

def start_ssh_agent():
    try:
        print("Iniciando o SSH agent...")
        subprocess.run(["start", "ssh-agent"], shell=True)
        subprocess.run(["ssh-add", SSH_KEY_PATH], check=True)
    except Exception as e:
        print(f"Erro ao iniciar SSH agent: {e}")

def clone_repository(branch_name):
    try:
        if not os.path.exists(INSTALL_DIR):
            os.makedirs(INSTALL_DIR)
            print(f"Pasta {INSTALL_DIR} criada.")
        print(f"Clonando repositório em {INSTALL_DIR}...")
        subprocess.run(["git", "clone", "--branch", branch_name, REPO_URL, INSTALL_DIR], check=True)
        print("Repositório clonado com sucesso.")
    except Exception as e:
        print(f"Erro ao clonar repositório: {e}")

def create_shortcut():
    try:
        exe_path = os.path.join(INSTALL_DIR, "BitEats.exe")
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        if not os.path.exists(desktop):
            desktop = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Desktop')
        
        shortcut_path = os.path.join(desktop, "BitEats.lnk")

        powershell_script = f"""
        $WScriptShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WScriptShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{exe_path}"
        $Shortcut.WorkingDirectory = "{INSTALL_DIR}"
        $Shortcut.IconLocation = "{exe_path}"
        $Shortcut.Save()
        """

        subprocess.run(["powershell", "-Command", powershell_script], check=True)
        print("Atalho criado na área de trabalho.")
    except Exception as e:
        print(f"Erro ao criar atalho: {e}")

def main():
    try:
        print("Inicializando...")
        if not os.path.exists(INSTALL_DIR):
            os.makedirs(INSTALL_DIR)
            print(f"Pasta {INSTALL_DIR} criada.")
        else:
            print(f"Pasta {INSTALL_DIR} já existe.")
        
        generate_ssh_key()
        show_ssh_key()
        start_ssh_agent()
        
        branch_name = input("Por favor, insira o nome do restaurante / estabelecimento (branch): ")
        clone_repository(branch_name)
        
        create_shortcut()
        print("Configuração concluída.")
    except Exception as e:
        print(f"Erro na configuração: {e}")
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
