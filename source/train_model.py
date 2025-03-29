import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, SpatialDropout1D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import os
import h5py
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Hàm đọc dữ liệu từ tệp .h5 (dữ liệu chữ ký và nhãn)


def load_data(file_path):
    with h5py.File(file_path, 'r') as f:
        X = f['X_train'][:]  # Dữ liệu (chữ ký)
        y = f['y_train'][:]  # Nhãn (0 hoặc 1)
    return X, y

# Hàm đọc khóa công khai từ tệp .pem


def load_public_key(public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend())
    return public_key

# Hàm kiểm tra tính hợp lệ của chữ ký số với khóa công khai


def verify_signature(document_path, signature_path, public_key_path):
    with open(signature_path, "rb") as sig_file:
        signature = sig_file.read()

    with open(document_path, "r", encoding="utf-8") as doc_file:
        document_data = doc_file.read()

    public_key = load_public_key(public_key_path)

    try:
        public_key.verify(
            signature,
            document_data.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True  # Chữ ký hợp lệ
    except Exception as e:
        return False  # Chữ ký không hợp lệ

# Hàm chuẩn bị dữ liệu huấn luyện


def create_training_data(documents_folder, signatures_folder, public_keys_folder, num_samples):
    data = []
    labels = []

    for i in range(1, num_samples + 1):
        document_path = os.path.join(documents_folder, f"contract_{i}.txt")
        signature_path = os.path.join(signatures_folder, f"signature_{i}.bin")
        public_key_path = os.path.join(
            public_keys_folder, f"public_key_{i}.pem")

        # Kiểm tra tính hợp lệ của chữ ký
        is_valid = verify_signature(
            document_path, signature_path, public_key_path)

        # Gán nhãn (1 cho chữ ký hợp lệ, 0 cho chữ ký sai)
        labels.append(1 if is_valid else 0)

        # Đọc chữ ký và chuyển thành vector
        with open(signature_path, "rb") as sig_file:
            signature_data = sig_file.read()

        # Chuyển byte data thành mảng các giá trị (0, 1)
        signature_vector = np.unpackbits(
            np.frombuffer(signature_data, dtype=np.uint8))
        data.append(signature_vector)

    return np.array(data), np.array(labels)

# Hàm xây dựng mô hình LSTM cho nhận diện chữ ký


def build_signature_model(input_shape):
    model = Sequential()

    # Thêm lớp LSTM với 100 đơn vị
    model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2,
              input_shape=input_shape))

    # Thêm lớp Dense với hàm kích hoạt ReLU
    model.add(Dense(128, activation='relu'))

    # Lớp đầu ra (1 đơn vị với hàm kích hoạt sigmoid cho phân loại nhị phân)
    model.add(Dense(1, activation='sigmoid'))

    # Biên dịch mô hình với Adam optimizer và hàm mất mát binary_crossentropy
    model.compile(optimizer=Adam(), loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model

# Hàm huấn luyện mô hình


def train_signature_model(documents_folder, signatures_folder, public_keys_folder, num_samples, epochs=10, batch_size=32, validation_split=0.2):
    # Tạo dữ liệu huấn luyện từ tài liệu, chữ ký và khóa công khai
    X_train, y_train = create_training_data(
        documents_folder, signatures_folder, public_keys_folder, num_samples)

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(
        X_train, y_train, test_size=validation_split, random_state=42)

    # Định dạng lại dữ liệu cho LSTM (dữ liệu 1D)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Xây dựng mô hình LSTM
    input_shape = (X_train.shape[1], 1)  # (timesteps, features)
    model = build_signature_model(input_shape)

    # Tóm tắt mô hình
    model.summary()

    # Định nghĩa callback cho early stopping (dừng khi mô hình không cải thiện)
    early_stopping = EarlyStopping(monitor='val_loss', patience=3)

    # Huấn luyện mô hình
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                        validation_data=(X_test, y_test), callbacks=[early_stopping])

    # Đánh giá mô hình trên dữ liệu kiểm tra
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Độ chính xác của mô hình trên tập kiểm tra: {test_acc}")
    print(f"Độ chính không xác của mô hình trên tập kiểm tra: {test_loss}")

    # Lưu mô hình đã huấn luyện vào tệp .keras
    model.save(
        'D:/wordspace/PYTHON/do_an_chu_ky_so/models/signature_model_lstm.keras')
    print("Mô hình đã được lưu vào file 'signature_model_lstm.kẻa'")

    return model, history


# Đường dẫn tới các thư mục chứa tài liệu, chữ ký và khóa công khai
documents_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_true/documents"
signatures_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_true/signatures"
public_keys_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_true/keys/public_keys"

# Số lượng mẫu dữ liệu huấn luyện
num_samples = 2000

# Huấn luyện mô hình
model, history = train_signature_model(
    documents_folder, signatures_folder, public_keys_folder, num_samples, epochs=40, batch_size=32)
