import numpy as np
from tensorflow.keras.models import load_model
import os

# Hàm chuẩn bị dữ liệu chữ ký cho mô hình LSTM


def prepare_signature_for_prediction(signature_path):
    # Đọc chữ ký và chuyển thành vector
    with open(signature_path, "rb") as sig_file:
        signature_data = sig_file.read()

    # Chuyển byte data thành mảng các giá trị nhị phân (0, 1)
    signature_vector = np.unpackbits(
        np.frombuffer(signature_data, dtype=np.uint8))
    # Reshape cho LSTM (1, timesteps, features)
    signature_vector = signature_vector.reshape(1, -1, 1)
    return signature_vector

# Hàm kiểm tra chữ ký sau khi huấn luyện mô hình


def check_signature_validity(model_path, signature_path):
    # Tải mô hình đã huấn luyện
    model = load_model(model_path)

    # Chuẩn bị dữ liệu chữ ký
    signature_vector = prepare_signature_for_prediction(signature_path)

    # Dự đoán chữ ký có hợp lệ hay không (1: hợp lệ, 0: giả)
    prediction = model.predict(signature_vector)
    is_valid = (prediction > 0.8)  # Chuyển xác suất sang nhãn (1 hoặc 0)

    if is_valid:
        print("Chữ ký hợp lệ.", prediction)
    else:
        print("Chữ ký giả mạo.", prediction)


# Đường dẫn đến mô hình đã huấn luyện
model_path = "D:/wordspace/PYTHON/do_an_chu_ky_so/models/signature_model_lstm.keras"

# Đường dẫn đến chữ ký cần kiểm tra
signature_path = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_true/signatures/signature_2.bin"

# Kiểm tra tính hợp lệ của chữ ký
check_signature_validity(model_path, signature_path)
