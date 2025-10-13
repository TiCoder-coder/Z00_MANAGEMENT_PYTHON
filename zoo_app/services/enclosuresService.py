from zoo_app.models import Enclosures
from django.core.exceptions import ObjectDoesNotExist
from zoo_app.serializers.createEnclosureDto import CreateEnclosureDto
from zoo_app.serializers.updateEnclosureDto import UpdateEnclosureDto

# Hàm tạo chuồng mới.


class enclosureService:
    def createEnclosure(self, dto: CreateEnclosureDto):
        # Kiểm tra enclosure đã được tạo chưa.
        try:
            existed = Enclosures.objects.filter(
                idEnclosure=dto.idEnclosure).first()
            if existed:
                return {
                    "status": "error",
                    "message": f"Enclosure with id {dto.idEnclosure} already exists"
                }

            enclosure = Enclosures(
                idEnclosure=dto.idEnclosure,
                nameEnclosure=dto.nameEnclosure,
                areaSize=dto.areaSize,
                climate=dto.climate,
                capacity=dto.capacity
            )
            enclosure.save()  # Lưu vào database
            return {
                "status": "success",
                "data": {
                    "idEnclosure": enclosure.idEnclosure,
                    "nameEnclosure": enclosure.nameEnclosure,
                    "areaSize": enclosure.areaSize,
                    "climate": enclosure.climate,
                    "capacity": enclosure.capacity
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    # Hàm lấy danh sách enclosure.

    def reviewEnclosure(self):
        # Lấy danh sách enclosure và in ra lỗi nếu có.
        try:
            enclosures = Enclosures.objects.all()
            data = []

            for e in enclosures:
                data.append({
                    "idEnclosure": e.idEnclosure,
                    "nameEnclosure": e.nameEnclosure,
                    "areaSize": e.areaSize,
                    "climate": e.climate,
                    "capacity": e.capacity
                })
            return {
                "status": "success",
                "data": data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    # Hàm cập nhật thông tin cho enclosure.

    def updateEnclosure(self, idEnclosure: str, dto: UpdateEnclosureDto):
        # Kiểm tra enclosure muốn update đã tồn tại chưa.
        try:
            enclosure = Enclosures.objects.filter(
                idEnclosure=idEnclosure).first()
            if not enclosure:
                return {
                    "status": "error",
                    "message": f"Enclosure with id {idEnclosure} not found"
                }
            if dto.nameEnclosure:
                enclosure.nameEnclosure = dto.nameEnclosure
            if dto.areaSize:
                enclosure.areaSize = dto.areaSize
            if dto.climate:
                enclosure.climate = dto.climate
            if dto.capacity:
                enclosure.capacity = dto.capacity

            enclosure.save()  # Lưu thay đổi vào database.
            return {
                "status": "success",
                "data": {
                    "idEnclosure": enclosure.idEnclosure,
                    "nameEnclosure": enclosure.nameEnclosure,
                    "areaSize": enclosure.areaSize,
                    "climate": enclosure.climate,
                    "capacity": enclosure.capacity
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    # Hàm xóa enclosure.

    def deleteEnclosure(self, idEnclosure: str):
        # Kiểm tra enclosure cần xóa có tồn tại chưa.
        try:
            enclosure = Enclosures.objects.filter(
                idEnclosure=idEnclosure).first()
            if not enclosure:
                return {
                    "status": "error",
                    "message": f"Enclosure with id {idEnclosure} not found"
                }
            delete_inf = {
                "deleteId": enclosure.idEnclosure,
                "deleteName": enclosure.nameEnclosure,
                "areaSize": enclosure.areaSize,
                "climate": enclosure.climate,
                "capacity": enclosure.capacity
            }

            enclosure.delete()  # Xóa enclosure.
            return {
                "status": "success",
                "message": f"Enclosure with id {idEnclosure} delete successfully",
                "data": delete_inf
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
