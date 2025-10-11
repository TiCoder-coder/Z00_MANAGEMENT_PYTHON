from datetime import datetime
from django.utils import timezone
from zoo_app.models import Animals, Enclosures
from zoo_app.serializers.createAnimalDto import CreateAnimalDto
from zoo_app.serializers.updateAnimalDto import UpdateAnimalDto
from django.core.exceptions import ObjectDoesNotExist


class animalService:
    # Tạo động vật mới.
    def createAnimals(self, dto: CreateAnimalDto):
        # Input: dto (CreateAnimalDto)

        # Thêm try/except tránh vỡ API.
        try:
            enclosure = Enclosures.objects.get(idEnclosure=dto.enclosureId)
            # Kiểm tra trùng id animal
            if Animals.objects.filter(id=dto.id).exists():
                return {
                    "status": "error",
                    "message": f"Animal with id {dto.id} already exists"
                }
            animal = Animals(
                id=dto.id,
                name=dto.name,
                age=dto.age,
                species=dto.species,
                gender=dto.gender,
                weight=dto.weight,
                healthStatus=dto.healthStatus,
                enclosureId=dto.enclosureId,
                createAt=timezone.now(),
                updateAt=timezone.now()
            )
            # Lưu vào database.
            animal.save()

            # Sửa lại đoạn này return toàn bộ thông tin.
            return {
                "status": "success",
                "data": {
                    "id": animal.id,
                    "name": animal.name,
                    "age": animal.age,
                    "species": animal.species,
                    "gender": animal.gender,
                    "weight": animal.weight,
                    "healthStatus": animal.healthStatus,
                    "enclosureId": animal.enclosureId,
                    # Chuyển dữ liệu sang str để phù hợp trong json.
                    "createAt": str(animal.createAt),
                    "updateAt": str(animal.updateAt)
                }
            }
        except ObjectDoesNotExist:
            return {
                "status": "error",
                "message": f"Enclosure with id {dto.enclosureId} not found"
            }
        except Exception as e:
            # Luôn trẻ về json khi có lỗi.
            return {
                "status": "error",
                "message": str(e)
            }

    # Lấy danh sách animal
    def reviewAnimals(self):
        # Sửa đoạn này thêm try/except
        try:
            animals = Animals.objects.all()
            data = []
            for ani in animals:
                data.append({
                    "id": ani.id,
                    "name": ani.name,
                    "age": ani.age,
                    "species": ani.species,
                    "gender": ani.gender,
                    "weight": ani.weight,
                    "healthStatus": ani.healthStatus,
                    "enclosureId": ani.enclosureId,
                    "createAt": str(ani.createAt),
                    "updateAt": str(ani.updateAt)
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

    def updateAnimals(self, id: str, dto: UpdateAnimalDto):
        try:
            animal = Animals.objects.get(id=id)
            # Kiểm tra enclosure có tồn tại không.
            if dto.enclosureId and not Enclosures.objects.filter(idEnclosure=dto.enclosureId).exists():
                return {
                    "status": "error",
                    "message": f"Enclosure with id {dto.enclosureId} not found"
                }

            if dto.name:
                animal.name = dto.name
            if dto.age:
                animal.age = dto.age
            if dto.species:
                animal.species = dto.species
            if dto.gender:
                animal.gender = dto.gender
            if dto.weight:
                animal.weight = dto.weight
            if dto.healthStatus:
                animal.healthStatus = dto.healthStatus
            if dto.enclosureId:
                animal.enclosureId = dto.enclosureId

            animal.updateAt = timezone.now()
            animal.save()

            # return toàn bộ thông tin sau khi update
            return {
                "status": "success",
                "data": {
                    "id": animal.id,
                    "name": animal.name,
                    "age": animal.age,
                    "species": animal.species,
                    "gender": animal.gender,
                    "weight": animal.weight,
                    "healthStatus": animal.healthStatus,
                    "enclosureId": animal.enclosureId,
                    "createAt": str(animal.createAt),
                    "updateAt": str(animal.updateAt)
                }
            }

        except ObjectDoesNotExist:
            return {
                "status": "error",
                "message": f"Animal with id {id} not found"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)  # Thông báo lỗi trong json.
            }

    def deleteAnimals(self, id: str):
        try:
            animal = Animals.objects.get(id=id)
            animal.delete()

            # Thêm return trả về thông tin khi xóa thành công.
            return {
                "status": "success",
                "message": f"Animal with id {id} delete successfully",
                "data": {
                    "deleteId": id,
                    "deleteName": animal.name,
                    "species": animal.species
                }
            }
        except ObjectDoesNotExist:
            return {
                "status": "error",
                "message": f"Animal with id {id} not found"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
