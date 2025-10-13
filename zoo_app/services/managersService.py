from typing import Optional, Dict, Any, List
from django.contrib.auth.hashers import make_password, check_password
from zoo_app.models import Managers
from zoo_app.serializers.createManagerDto import CreateManagerDto
from zoo_app.serializers.updateManagerDto import UpdateManagerDto


class managersService:
    # Tạo manager mới (chỉ manager được thực hiện)
    def createManager(self, dto: CreateManagerDto) -> Dict[str, Any]:
        # Kiểm tra các giá trị trong manager đã tồn tại chưa.
        try:
            existing_user = Managers.objects.filter(
                userName=dto.userName).first()
            if existing_user:
                return {
                    "status": "error",
                    "message": f"The login name {dto.userName} already exists",
                    "data": None
                }
            existing_id = Managers.objects.filter(id=dto.id).first()
            if existing_id:
                return {
                    "status": "error",
                    "message": f"Manager with id {dto.id} already exists",
                    "data": None
                }
            # Mã hóa mật khẩu.
            hashes_password = make_password(dto.password)
            manager = Managers(
                id=dto.id,
                name=dto.name,
                userName=dto.userName,
                password=hashes_password,
                role=dto.role
            )

            manager.save()  # Lưu vào database.
            data = manager.to_dict()
            if "password" in data:
                data.pop("password")
            if "userName" in data:
                data.pop("userName")

            return {
                "status": "success",
                "message": "Manager created successfully",
                "data": data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f" Error creating manager: {str(e)}",
                "data": None
            }
    # Hàm trả về danh sách manager.

    def reviewManager(self) -> Dict[str, Any]:
        # Kiểm tra danh sách manager đã tồn tại chưa. Nếu chưa có thì báo lỗi.
        try:
            managers = Managers.objects.all()
            if not managers.exists():
                return {
                    "status": "error",
                    "message": "There is no managers in the system",
                    "data": []
                }
            result_list = []
            for m in managers:
                inf = m.to_dict()
                if "password" in inf:
                    inf.pop("password")
                if "userName" in inf:
                    inf.pop("userName")

                result_list.append(inf)
            return {
                "status": "success",
                "message": "Get manager list successfully",
                "data": result_list
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error when getting manager: {str(e)}",
                "data": []
            }
    # Hàm cập nhật thông tin manager.

    def updateManager(self, id: str, dto: UpdateManagerDto) -> Dict[str, Any]:
        # Kiểm tra thông tin cập nhật đã tồn tại trong database chưa. Nếu chưa thì báo lỗi.
        try:
            manager = Managers.objects.filter(id=id).first()
            if manager is None:
                return {
                    "status": "error",
                    "message": f"Manager with id {id} not found",
                    "data": None
                }
            if dto.userName is not None:
                if dto.userName != manager.userName:
                    conflict_user = Managers.objects.filter(
                        userName=dto.userName).exclude(id=id).first()
                    if conflict_user is not None:
                        return {
                            "status": "error",
                            "message": f"The login name {dto.userName} is already exists",
                            "data": None
                        }
                    manager.userName = dto.userName
            if dto.password is not None:
                manager.password = make_password(dto.password)
            if dto.name is not None:
                manager.name = dto.name
            if dto.role is not None:
                manager.role = dto.role
            manager.save()  # Lưa vào database.
            data = manager.to_dict()
            if "password" in data:
                data.pop("password")
            if "userName" in data:
                data.pop("userName")
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
    # Hàm xóa thông tin manager.

    def deleteManager(self, id: str) -> Dict[str, Any]:
        # Kiểm tra manager cần xóa đã tồn tại trong database chưa.
        try:
            manager = Managers.objects.filter(id=id).first()
            if manager is None:
                return {
                    "status": "error",
                    "message": f"Manager with id {id} not found",
                    "data": None
                }
            manager.delete()  # Xóa manager.
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
