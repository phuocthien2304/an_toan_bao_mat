# Script xử lý dữ liệu đầu vào (trích xuất văn bản từ PDF, etc.)
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

# Hàm tải private key từ file


def load_private_key(private_key_path):
    with open(private_key_path, "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=None,
        )
    return private_key

# Hàm ký tài liệu với private key


def sign_document_with_key(document_path, private_key):
    # Đọc nội dung tài liệu
    with open(document_path, "rb") as document_file:
        document_content = document_file.read()

    # Sử dụng private key để ký tài liệu
    signature = private_key.sign(
        document_content,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

# Hàm ký tất cả tài liệu với các private key tương ứng


def sign_documents(documents_folder, keys_folder, output_folder, num_documents):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(1, num_documents + 1):
        document_path = os.path.join(
            documents_folder, f"contract_fake_{i}.txt")
        private_key_path = os.path.join(
            keys_folder, f"private_key_fake_{i}.pem")

        # Tải private key
        private_key = load_private_key(private_key_path)

        # Ký tài liệu
        signature = sign_document_with_key(document_path, private_key)

        # Lưu chữ ký vào tệp
        signature_file_path = os.path.join(
            output_folder, f"signature_fake_{i}.bin")
        with open(signature_file_path, "wb") as signature_file:
            signature_file.write(signature)

        print(
            f"Đã ký và lưu chữ ký cho tài liệu {i} vào {signature_file_path}")


# Đường dẫn đến thư mục chứa tài liệu, khóa và nơi lưu chữ ký
documents_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_false/documents_false"
keys_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_false/keys_false/private_keys"
output_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_false/signatures"

# Số lượng tài liệu cần ký
num_documents = 1000

# Ký tài liệu và lưu chữ ký
sign_documents(documents_folder, keys_folder, output_folder, num_documents)

print("Đã ký tất cả tài liệu và lưu chữ ký thành công!")
