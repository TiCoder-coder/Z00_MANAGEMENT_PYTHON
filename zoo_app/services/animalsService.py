from datetime import datetime
from zoo_app.models import Animals, Enclosures
from zoo_app.serializers.createAnimalDto import CreateAnimalDto
from zoo_app.serializers.updateAnimalDto import UpdateAnimalDto
from django.core.exceptions import ObjectDoesNotExist


class animalService:
    # Tạo động vật mới.
    def createAnimals(self, dto: CreateAnimalDto):
        # Input: dto (CreateAnimalDto)
        # Kiểm tra enclusure có tồn tại không.
        try:
            enclosure = Enclosures.object.get(idEnclosure=dto.enclusoreId)
        except ObjectDoesNotExist:
            raise Exception(f"Enclosure with id {dto.enclosureId} not found")
        # Kiểm tra id của animal có trùng khi thêm vào animal mới không.
        if Animals.object.filter(id=dto.id).exists():
            raise Exception(f"Animal wit id {dto.id} already exists")
        # Tạo đối tượng animal mới.
        animal = Animals(
            id=dto.id,
            name=dto.name,
            age=dto.age,
            species=dto.species,
            gender=dto.gender,
            weight=dto.weight,
            healthStatus=dto.healthStatus,
            enclosureId=enclosure.idEnclosure,
            createAt=datetime.now(),
            updateAt=datetime.now()
        )
        animal.save()  # Lưu vào mongodb
        # Output ra json
        return {
            "message": "Animal created successfully",
            "data": {
                "id": animal.id,
                "name": animal.name,
                "species": animal.species,
                "enclosureId": animal.enclosureId
            }
        }

    # Xuất toàn bộ danh sách animal
    def reviewAnimals(self):
        """Lấy toàn bộ danh sách animal trong database
           Nếu không có animal nào thì trả về rỗng."""
        animasl = Animals.object.all()
        result = []
        # Dùng vòng lặp để duyệt qua từng animal và đưa vào list
        for ani in animasl:
            result.append({
                "id": ani.id,
                "name": ani.name,
                "species": ani.species,
                "gender": ani.gender,
                "healthStatus": ani.healthStatus
            })
        return result

    # Cập nhật thông tin cho animal
    def updateAnimals(self, id: str, dto: UpdateAnimalDto):
        # Input: id, dto.
        # Kiểm tra animal có tồn tại không.
        try:
            animal = Animals.object.get(id=id)
        except ObjectDoesNotExist:
            raise Exception(f"Animal with id {id} not found")

        # Nếu enclosure có trong dot, kiểm tra sự tồn tại.
        if dto.enclosureId:
            if not Enclosures.object.filter(idEnclosure=dto.enclosureId).exists():
                raise Exception(
                    f"Enclosure with id {dto.enclosureId} not found")
        # Cập nhật từng field nếu dto có giá trị. Kiểm tra để tánh None
        if dto.name:
            animal.name = dto.name
        if dto.age:
            animal.age = dto.age,
        if dto.species:
            animal.species = dto.species,
        if dto.gender:
            animal.gender = dto.gender,
        if dto.weight:
            animal.weight = dto.weight,
        if dto.healthStatus:
            animal.healthStatus = dto.healthStatus
        if dto.enclosureId:
            animal.enclosureId = dto.enclosureId

        # Cập nhật thời gian thay đổi
        animal.updatAt = datetime.now()
        animal.save()

        # id: mã con vật vừa mới update
        # updateAt: thời gian update. Ép thành chuối string để đưa vào JSON
        return {
            "message": "Animal updated successfully",
            "data": {
                "id": id,
                "updateAt": str(animal.updateAt)
            }
        }

    def deleteAnimal(self, id: str):
        # Input: id
        # Kiểm tra animal có tồn tại không
        try:
            animal = Animals.object.get(id=id)
            animal.delete()
            return {"message": f"Animal with id {id} deleted successfully"}
        except ObjectDoesNotExist:
            raise Exception(f"Animal with id {id} not found")
