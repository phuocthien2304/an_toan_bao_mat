from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import os

# Hàm ký tài liệu với một private key và tài liệu tương ứng


def sign_document_with_key(document_path, private_key_path, output_path):
    # Đọc tài liệu
    with open(document_path, "r", encoding="utf-8") as document_file:
        document_data = document_file.read()

    # Đọc private key từ tệp .pem
    with open(private_key_path, "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(), password=None)

    # Ký tài liệu với private key
    signature = private_key.sign(
        document_data.encode(),  # Mã hóa tài liệu thành byte
        padding.PKCS1v15(),  # Phương pháp padding
        hashes.SHA256()  # Sử dụng SHA-256 cho hàm băm
    )

    # Lưu chữ ký vào tệp .bin
    with open(output_path, "wb") as signature_file:
        signature_file.write(signature)

    print(f"Chữ ký đã được lưu vào: {output_path}")


# Hàm ký nhiều tài liệu với nhiều khóa riêng
def sign_multiple_documents(documents_folder, keys_folder, output_folder, num_documents):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(1, num_documents + 1):
        # Đường dẫn tài liệu và khóa riêng
        document_path = os.path.join(
            documents_folder, f"contract_{i}.txt")
        private_key_path = os.path.join(
            keys_folder, f"private_key_{5}.pem")

        # Đường dẫn lưu chữ ký
        output_path = os.path.join(output_folder, f"signature_{2}.bin")

        # Ký tài liệu với private key tương ứng
        sign_document_with_key(document_path, private_key_path, output_path)


# Đường dẫn đến các thư mục chứa tài liệu và khóa riêng
documents_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_fake/documents_fake"
keys_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_true/keys/private_keys"
output_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_fake/signatures_fake"

# Số lượng tài liệu và khóa riêng
num_documents = 1

# Ký tất cả tài liệu với các khóa riêng tương ứng
sign_multiple_documents(documents_folder, keys_folder,
                        output_folder, num_documents)
