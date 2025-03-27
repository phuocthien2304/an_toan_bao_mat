from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
import random

# Hàm tạo private key và public key giả


def generate_fake_key():
    # Tạo private key giả
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # Kích thước khóa 2048 bit
    )

    # Tạo public key từ private key giả
    public_key = private_key.public_key()

    return private_key, public_key

# Hàm tạo và lưu 1000 khóa giả


def create_fake_keys(output_folder, num_keys):
    # Tạo thư mục lưu khóa nếu chưa tồn tại
    private_folder = os.path.join(output_folder, "private_keys")
    public_folder = os.path.join(output_folder, "public_keys")

    if not os.path.exists(private_folder):
        os.makedirs(private_folder)

    if not os.path.exists(public_folder):
        os.makedirs(public_folder)

    # Tạo và lưu 1000 khóa giả
    for i in range(1, num_keys + 1):
        private_key, public_key = generate_fake_key()

        # Lưu private key giả vào tệp
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        private_key_path = os.path.join(
            private_folder, f'private_key_fake_{i}.pem')
        with open(private_key_path, 'wb') as private_key_file:
            private_key_file.write(private_key_pem)

        # Lưu public key giả vào tệp
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        public_key_path = os.path.join(
            public_folder, f'public_key_fake_{i}.pem')
        with open(public_key_path, 'wb') as public_key_file:
            public_key_file.write(public_key_pem)

        print(
            f"Đã tạo và lưu private_key_fake_{i}.pem và public_key_fake_{i}.pem")


# Đường dẫn thư mục để lưu các khóa
output_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_fake/keys_fake"

# Tạo 1000 khóa giả (private key và public key)
create_fake_keys(output_folder, 2000)

print("Đã tạo 2000 private key và public key giả thành công!")
