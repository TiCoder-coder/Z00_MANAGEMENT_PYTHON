from zoo_app.models import Enclosures
from zoo_app.serializers.createEnclosureDto import CreateEnclosureDto
from zoo_app.serializers.updateEnclosureDto import UpdateEnclosureDto


class enclosureService:
    # Hàm tạo enclosure(chuồng) mới.
    def createEnclosure(self, dto: CreateEnclosureDto):
        # Kiểm tra enclosure đã tồn tại trong database chưa.
        # Nếu enclosire tồn tại trả về giá trị đầu idEnclosure trong Enclosure.
        existed = Enclosures.object.filter(idEnclosure=dto.idEnclosure).first()
        # Không có gì thì trả về rỗng.
        if existed:
            raise ValueError(
                f"Enclosure with id {dto.idEnclosure} already exists")
        # Chưa tồn tại thì tạo object Enclosure
        enclosure = Enclosures(
            idEnclosure=dto.idEnclosure,
            nameEnclosure=dto.nameEnclosure,
            areaSize=dto.areaSize,
            climate=dto.climate,
            capacity=dto.capacity
        )
        # Lưu vào database
        enclosure.save()
        # Trả về dữ liệu về dạng dict
        return {
            "idEnclosure": enclosure.idEnclosure,
            "nameEnclosure": enclosure.nameEnclosure,
            "areaSize": enclosure.areaSize,
            "climate": enclosure.climate,
            "capacity": enclosure.capacity
        }

    # Lấy toàn bộ danh sách enclosure trong database
    def reviewEnclosure(self):
        # Lấy toàn bộ dữ liệu trong collection Enclosure
        enclosures = Enclosures.object.all()
        # Nếu không có enclosures thì trả về mảng rỗng.
        if not enclosures:
            return []
        # Duyệt qua từng enclosures và chuyển thành dạng dữ liệu dict
        result = []
        for e in enclosures:
            result.append({
                "idEnclosure": e.idEclosure,
                "nameEnclosure": e.nameEnclosure,
                "areaSize": e.areaSize,
                "climate": e.climate,
                "capacity": e.capacity
            })
        return result

    def updateEnclosure(self, idEnclosure: str, dto: UpdateEnclosureDto):
        # Cập nhật thông tin cho 1 enclosure bằng idEnclosure
        # chỉ cập nhật những trường nào có trong dto

        # Tìm enclosure cần update
        enclosure = Enclosures.object.filter(idEnclosure=idEnclosure).first()
        if not enclosure:
            return None  # Không tìm thấy
        """Cập nhật từng filed nếu dto có giá trị
           Nếu dto không có giá trị thì bỏ qua nó."""
        if dto.nameEnclosure:
            enclosure.nameEnclosure = dto.nameEnclosure
        if dto.areaSize:
            enclosure.areaSize = dto.areaSize
        if dto.climate:
            enclosure.climate = dto.climate
        if dto.capacity:
            enclosure.capacity = dto.capacity

        enclosure.save()  # Lưu thay đổi.

        # Trả về dữ liệu sau khi update
        return {
            "idEnclosure": enclosure.idEnclosure,
            "nameEnclosure": enclosure.nameEnclosure,
            "areaSize": enclosure.areaSize,
            "climate": enclosure.climate,
            "capacity": enclosure.capacity
        }

    def deleteEnclosure(sele, idEnclosure: str):
        # Xóa 1 enclosure bằng idEnclosure
        # Kiểm tran enclosure có tồn tại không.
        enclosure = Enclosures.ogject.filter(idEnclosure=idEnclosure).first()
        if not enclosure:
            return False
        # Xóa nếu enclosure tồn tại
        enclosure.delete()
        return True
