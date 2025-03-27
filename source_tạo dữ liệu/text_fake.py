import random
import string
from datetime import datetime, timedelta
import os

# Hàm sinh tên ngẫu nhiên cho công ty


def generate_random_name():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))

# Hàm sinh số tiền giao dịch ngẫu nhiên


def generate_random_amount():
    return round(random.uniform(1000, 1000000), 2)

# Hàm sinh ngày giao dịch ngẫu nhiên


def generate_random_date():
    today = datetime.today()
    random_days = random.randint(0, 365)
    random_date = today - timedelta(days=random_days)
    return random_date.strftime('%d/%m/%Y')

# Hàm tạo hợp đồng giả


def generate_fake_contract():
    contract_number = f"CONTRACT-FAKE-{random.randint(100000, 999999)}"
    company_name_a = generate_random_name()  # Công ty A giả
    company_name_b = generate_random_name()  # Công ty B giả
    transaction_amount = generate_random_amount()  # Số tiền giao dịch giả
    transaction_date = generate_random_date()  # Ngày giao dịch giả

    terms = [
        "Điều khoản 1: Bên A cam kết chuyển nhượng số tiền cho Bên B trong vòng 10 ngày kể từ ngày ký hợp đồng.",
        "Điều khoản 2: Bên B sẽ sử dụng số tiền này để thực hiện các giao dịch kinh doanh hợp pháp.",
        "Điều khoản 3: Bên A và Bên B có trách nhiệm thực hiện nghĩa vụ tài chính theo các điều khoản đã thỏa thuận.",
        "Điều khoản 4: Bên A sẽ hỗ trợ Bên B trong các vấn đề liên quan đến việc sử dụng số tiền giao dịch.",
        "Điều khoản 5: Hợp đồng này có hiệu lực kể từ ngày ký và có thể được gia hạn sau khi hai bên thỏa thuận."
    ]

    # Tạo hợp đồng giả
    contract_content = f"""
    HỢP ĐỒNG GIAO DỊCH NGÂN HÀNG (GIẢ)
    Số hợp đồng: {contract_number}

    Hôm nay, ngày {transaction_date}, giữa:

    BÊN A: {company_name_a} (Số ĐKKD: {random.randint(100000000, 999999999)})
    BÊN B: {company_name_b} (Số ĐKKD: {random.randint(100000000, 999999999)})

    Các bên đã thống nhất ký kết hợp đồng giao dịch ngân hàng với các điều khoản sau:

    1. Số tiền giao dịch: {transaction_amount} VND (Giao dịch giả)
    2. Điều khoản thanh toán:
        {random.choice(terms)}
    3. Thời gian thực hiện giao dịch: 10 ngày kể từ ngày ký hợp đồng.

    Các bên cam kết thực hiện đầy đủ các nghĩa vụ và quyền lợi của mình theo hợp đồng này.

    Ký tên:

    BÊN A: ________________________    BÊN B: ________________________

    Ngày ký hợp đồng: {transaction_date}
    """

    return contract_content

# Hàm tạo 1000 hợp đồng giả và lưu vào tệp


def create_fake_contracts(output_folder, num_files):
    # Tạo thư mục lưu hợp đồng nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(1, num_files + 1):
        contract_content = generate_fake_contract()
        file_name = os.path.join(
            output_folder, f"contract_fake_{i}.txt")  # Tên file hợp đồng
        with open(file_name, "w") as file:
            file.write(contract_content)
        print(f"Đã tạo file hợp đồng giả: {file_name}")


# Đường dẫn thư mục để lưu các hợp đồng
output_folder = "D:/wordspace/PYTHON/do_an_chu_ky_so/data_fake/documents_fake"

# Tạo 1000 hợp đồng giả
create_fake_contracts(output_folder, 2000)

print("Đã tạo 2000 hợp đồng giả thành công!")
