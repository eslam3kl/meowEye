import os

def load_payloads(filename):
    try:
        with open(os.path.join('payloads', filename), 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        from config import color_tag
        print(f"{color_tag('[ERROR]')} Error loading payloads from {filename}: {e}")
        return []

def get_payloads(attack_choice):
    if attack_choice == 'ref':
        return ['ES"><']
    elif attack_choice == 'lfiLinux':
        return load_payloads('lfi-unix-payloads.txt')
    elif attack_choice == 'lfiWin':
        return load_payloads('lfi-windows-payloads.txt')
    elif attack_choice == 'ssti':
        return load_payloads('ssti-payloads.txt')
    return []
