from typing import Optional, Dict, Any, List
from django.contrib.auth.hashers import make_password, check_password
from zoo_app.models import Managers
from zoo_app.serializers.createManagerDto import CreateManagerDto
from zoo_app.serializers.updateManagerDto import UpdateManagerDto


class managersService:
    # Tạo manager mới (chỉ manager được thực hiện)
    def createManager(self, dto: CreateManagerDto) -> Dict[str, Any]:
        # Thêm try/except
        try:
            # Kiểm tra userName đã tồn tại trong database chưa.
            existing_user = Managers.objects.filter(
                userName=dto.userName).first()
            if existing_user:
                return {
                    "status": "error",
                    "message": f"The login name {dto.userName} already exists",
                    "data": None
                }
            # Kiểm tra id có trùng không.
            existing_id = Managers.objects.filter(id=dto.id).first()
            if existing_id:
                return {
                    "status": "error",
                    "message": f"Manager with id {dto.id} already exists",
                    "data": None
                }

            # Mã hóa mật khẩu.
            hashes_password = make_password(dto.password)
            # Tạo object mới cho class Manager.
            manager = Managers(
                id=dto.id,
                name=dto.name,
                userName=dto.userName,
                password=hashes_password,
                role=dto.role
            )

            manager.save()  # Lưu vào database.

            # Lấy data và lưu data dạng dict.
            data = manager.to_dict()

            # Ẩn password và userName.
            if "password" in data:
                data.pop("password")
            if "userName" in data:
                data.pop("userName")

            # Trả về return.
            return {
                "status": "success",
                "message": "Manager created successfully",
                "data": data
            }
        except Exception as e:
            # Trả về thông báo khi có lỗi.
            return {
                "status": "error",
                "message": f" Error creating manager: {str(e)}",
                "data": None
            }

    def reviewManager(self) -> Dict[str, Any]:
        # Thêm try/except
        try:
            # Lấy toàn bộ danh sách manager.
            managers = Managers.objects.all()
            # Không có manager nào thì trả về danh sách rỗng.
            if not managers.exists():
                return {
                    "status": "error",
                    "message": "There is no managers in the system",
                    "data": []
                }

            result_list = []
            # Duyệt qua từng managers
            for m in managers:
                # Chuyển thàng dict cho dễ đọc.
                inf = m.to_dict()

                # Ẩn userName và password.

                if "password" in inf:
                    inf.pop("password")
                if "userName" in inf:
                    inf.pop("userName")

                result_list.append(inf)  # Thêm kết quả vào result.

            # Trả về all class Manager.
            return {
                "status": "success",
                "message": "Get manager list successfully",
                "data": result_list
            }

        except Exception as e:
            # Nếu có lỗi trả về thông tin lỗi.
            return {
                "status": "error",
                "message": f"Error when getting manager: {str(e)}",
                "data": []
            }

    def updateManager(self, id: str, dto: UpdateManagerDto) -> Dict[str, Any]:
        # Thêm try/except.
        try:
            # Tìm manager có id tương ứng.
            manager = Managers.objects.filter(id=id).first()
            # Không thấy trả về lỗi.
            if manager is None:
                return {
                    "status": "error",
                    "message": f"Manager with id {id} not found",
                    "data": None
                }
            # Nếu có userName mới kiểm tra có trùng không.
            if dto.userName is not None:
                if dto.userName != manager.userName:
                    # Kiểm trong database của manager có trùng userName muốn cập nhật không.
                    conflict_user = Managers.objects.filter(
                        userName=dto.userName).exclude(id=id).first()
                    if conflict_user is not None:
                        return {
                            "status": "error",
                            "message": f"The login name {dto.userName} is already exists",
                            "data": None
                        }
                    # Cạp nhật userName mới.
                    manager.userName = dto.userName
            # Cập nhật password mới thì hash password
            if dto.password is not None:
                manager.password = make_password(dto.password)
            # Cập nhật tên mới.
            if dto.name is not None:
                manager.name = dto.name
            # Cập nhật vai trò mới.
            if dto.role is not None:
                manager.role = dto.role
            manager.save()  # Lưu lại.
            data = manager.to_dict()
            # Ẩn userName và password.
            if "password" in data:
                data.pop("password")
            if "userName" in data:
                data.pop("userName")

            # Trả về thông tin.
            return {
                "status": "success",
                "message": "Manager information updated successfully",
                "data": data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error updating manager: {str(e)}",
                "data": None
            }

    def deleteManager(self, id: str) -> Dict[str, Any]:
        # Thêm try/except
        try:
            # Tìm manager càn xóa.
            manager = Managers.objects.filter(id=id).first()
            # Không tìm thấy thì none
            if manager is None:
                return {
                    "status": "error",
                    "message": f"Manager with id {id} not found",
                    "data": None
                }
            # Tìm thấy thì xóa.
            manager.delete()

            # Trả về xác nhận sau khi xóa.
            return {
                "status": "success",
                "message": "Manager deleted successfully",
                "data": None
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error deleting manager: {str(e)}",
                "data": None
            }
