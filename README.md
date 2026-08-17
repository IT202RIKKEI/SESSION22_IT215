# Phân biệt `Depends` và `dependencies` trong FastAPI

## 1. Bảng so sánh nhanh

| Tiêu chí | `Depends(...)` (Trong tham số hàm) | `dependencies=[...]` (Trong Decorator / Router) |
| :--- | :--- | :--- |
| **Mục đích** | **Lấy dữ liệu** trả về từ Dependency để dùng tiếp. | **Kiểm tra / Xác thực** (Gác cổng), không cần dữ liệu. |
| **Giá trị `return`** | Gán trực tiếp vào biến trong hàm. | Bị bỏ qua, không truyền vào thân hàm. |
| **Phạm vi áp dụng** | Từng hàm/endpoint cụ thể cần dữ liệu. | Từng endpoint hoặc toàn bộ một `APIRouter`. |

---

## 2. Code mẫu thực tế

### Trường hợp 1: Cần lấy dữ liệu User / Payload (`Depends`)
```python
@account_router.get("/balance")
def get_balance(payload: dict = Depends(get_current_payload)):
    # Dùng được biến payload bên trong hàm để query DB
    user_id = payload.get("sub")
    return {"user_id": user_id}
```

### Trường hợp 2: Chỉ cần kiểm tra đăng nhập (`dependencies`)
```python
# Cách A: Gán cho 1 Endpoint cụ thể
@account_router.post("/transfer", dependencies=[Depends(get_current_payload)])
def transfer_money():
    return {"message": "Giao dịch thành công"}

# Cách B: Khóa toàn bộ các API trong Router
account_router = APIRouter(
    prefix="/account",
    tags=["QUẢN LÝ TÀI KHOẢN"],
    dependencies=[Depends(get_current_payload)]  # Tất cả API bên dưới đều bắt buộc có Token
)
```