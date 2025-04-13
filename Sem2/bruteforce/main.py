import subprocess
import shlex

def generate_passwords(charset, length):
    if length == 0:
        yield ""
    else:
        for char in charset:
            for password in generate_passwords(charset, length - 1):
                yield char + password


def brut_hash(charset, max_length):
    passwords_file = "passwords.txt"

    with open(passwords_file, "w") as f:
        for length in range(1, max_length + 1):
            for password in generate_passwords(charset, length):
                f.write(password + "\n")

    subprocess.run(shlex.split("hashcat -m 13000 -a 0 hash.txt {} --force".format(passwords_file)))

    try:
        res = subprocess.check_output(shlex.split("hashcat -m 13000 hash.txt --show")).decode()
        password = res.strip().split(':', 1)[1]
        password_file = open('password_found.txt', 'w')
        password_file.write(password + '\n')
        print(f'Password was found and saved in password_found.txt: {password}')
    except IndexError:
        print('Password was not found.')


def get_hash(archive_name):
    command = subprocess.run(['john/run/rar2john', archive_name], capture_output=True, text=True)

    if command.returncode != 0 or not command.stdout:
        print(command.stderr)
        return False

    hash_value = command.stdout.strip().split(':', 1)[1]

    output_file = open('hash.txt', 'w')
    output_file.write(hash_value)

    print(f"Extracted hash: {hash_value}")
    return True


if __name__ == "__main__":
    # Параметры для брутфорса
    archive_name = "archive1.rar"
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    max_length = 3

    # Сначала получаем хэш, затем брутфорсим
    if get_hash(archive_name):
        brut_hash(charset, max_length)
