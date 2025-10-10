from typing import Optional, Dict, Any, List
from django.contrib.auth.hashers import make_password, check_password
from zoo_app.models import Managers
from zoo_app.serializers.createManagerDto import CreateManagerDto
from zoo_app.serializers.updateManagerDto import UpdateManagerDto


class managersService:
    # Tạo manager mới (chỉ manager được thực hiện)
    def createManager(self, dto: CreateManagerDto) -> Dict[str, Any]:
        # Kiểm tra userName đã tồn tại trong database chưa.
        existing_user = Managers.object.filter(userName=dto.userName).first()
        if existing_user is not None:
            # Tìm thấy user có userName trùng lặp thì báo lỗ và dừng lại.
            raise ValueError(f"The login name {dto.userName} already exists")
        # Kiểm tra id có bị trùng không
        existing_id = Managers.object.filter(id=dto.id).first()
        if existing_id is not None:
            raise ValueError(f"Manager has Id {dto.id} already exists")
        # Mã hóa mật khẩu trước khi lưu
        hashed_password = make_password(dto.password)
        # Tạo object Maneger và gán giá trị
        manager = Managers(
            id=dto.id,
            name=dto.name,
            userName=dto.userName,
            password=hashed_password,  # Lưu hash
            role=dto.role
        )

        # Lưu vào database
        manager.save()

        # Trả về thông tin đã tạo (không để password để bảo vệ)
        return {
            "message": "Created manager successful",
            "data": manager.to_dict()
        }

    def reviewManager(self) -> List[Dict[str, Any]]:
        """Lấy toàn bộ danh sách manager trong database
           Trả về dạng dữ liệu List of Dict
           Không trả về password."""
        managers = Managers.object.all()
        if not managers:
            return []
        # Duyệt từng Managers, chuyển thành dict và thêm list vào result.
        result_list = []
        for manager in managers:
            # Mỗi lần duyệt thêm vào danh sách.
            manager_inf = manager.to_dict()
            result_list.append(manager_inf)

        # Trả về danh sách đầy đủ sau khi duyệt xong.
        return result_list

    def updateManager(self, id: str, dto: UpdateManagerDto) -> Optional[Dict[str, Any]]:
        # Cập nhất thông tin manager có id tương ứng
        # Tìm Manager có id tương ứng.
        manager = Managers.object.fliter(id=id).first()
        # Không tìm thấy trả về None
        if manager is None:
            return None

        # Có userName mới kiểm tra đã có ai sử dụng chưa.
        if dto.userName is not None:
            if dto.userName != manager.userName:
                # Kiểm tra có manager đã sử dụng userName này chưa.
                conflict_user = Managers.object.filter(
                    userName=dto.userName).exclude(id=id).first()
                if conflict_user is not None:
                    # Nếu có báo lỗi.
                    raise ValueError(
                        f"The login {dto.userName} already exists")
                # Nếu không trùng thì cập nhật userName mới
                manager.userName = dto.userName
        # Nếu có password mới thì hash lại
        if dto.password is not None:
            hashed_pw = make_password(dto.password)
            manager.password = hashed_pw
        # Nếu có name mới thì cập nhật
        if dto.name is not None:
            manager.name = dto.name
        # Nếu có role mới thì cập nhật
        if dto.role is not None:
            manager.role = dto.role

        # Lưu các thay đổi vào database
        manager.save()

        # Trả về result không hiện password
        return {
            "message": "Manager updated successful",
            "data": manager.to_dict()
        }

    def deleteManager(self, id: str) -> bool:
        # Xóa manager theo id
        # Tìm manager có id bạn muốn del
        manager = Managers.object.filter(id=id).first()
        # Không tìm thấy trả về False.
        if manager is None:
            return False
        # Nếu tìm thấy thì xóa và trả về True
        manager.delete()
        return True
