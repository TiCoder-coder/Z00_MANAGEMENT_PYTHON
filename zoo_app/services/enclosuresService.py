from zoo_app.models import Enclosures
from django.core.exceptions import ObjectDoesNotExist
from zoo_app.serializers.createEnclosureDto import CreateEnclosureDto
from zoo_app.serializers.updateEnclosureDto import UpdateEnclosureDto


class enclosureService:
    # Hàm tạo enclosure(chuồng) mới.
    def createEnclosure(self, dto: CreateEnclosureDto):
        # Thêm try/except
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

            # Thêm return toàn bộ thông tin.
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

    def reviewEnclosure(self):
        # Thêm try/except
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

    def updateEnclosure(self, idEnclosure: str, dto: UpdateEnclosureDto):
        # Thêm try/except
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

            enclosure.save()

            # return toàn bộ thông tin.
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

    def deleteEnclosure(self, idEnclosure: str):
        try:
            enclosure = Enclosures.objects.filter(
                idEnclosure=idEnclosure).first()
            if not enclosure:
                return {
                    "status": "error",
                    "message": f"Enclosure with id {idEnclosure} not found"
                }

            # Lưu thông tin trả về sau khi del
            delete_inf = {
                "deleteId": enclosure.idEnclosure,
                "deleteName": enclosure.nameEnclosure,
                "areaSize": enclosure.areaSize,
                "climate": enclosure.climate,
                "capacity": enclosure.capacity
            }

            enclosure.delete()  # Lưu vào database

            # Thêm return chi tiết sau khi xóa thành công.
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
