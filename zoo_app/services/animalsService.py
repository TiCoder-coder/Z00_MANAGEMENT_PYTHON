from datetime import datetime
from django.utils import timezone
from zoo_app.models import Animals, Enclosures
from zoo_app.serializers.createAnimalDto import CreateAnimalDto
from zoo_app.serializers.updateAnimalDto import UpdateAnimalDto
from django.core.exceptions import ObjectDoesNotExist


class animalService:
    # Hàm tạo animal.
    def createAnimals(self, dto: CreateAnimalDto):
        # Kiểm tra enclosure có tồn tại không.
        try:
            enclosure = Enclosures.objects.get(idEnclosure=dto.enclosureId)
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

            animal.save()  # Lưu trữ vào database.
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
                "message": f"Enclosure with id {dto.enclosureId} not found"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    # Hàm lấy tất cả danh sách animal
    def reviewAnimals(self):
        # Kiểm tra báo lỗi nếu có và trả về danh sách animal vào database.
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

    # Hàm thêm thông tin animal vào database.
    def updateAnimals(self, id: str, dto: UpdateAnimalDto):
        # Kiểm tra animal có tồn tại không.
        try:
            animal = Animals.objects.get(id=id)
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

            # Trả về thông tin sau khi update.
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
                "message": str(e)
            }

    # Hàm xóa animal trong database.
    def deleteAnimals(self, id: str):
        # Kiểm tra animal có tồn tại không.
        try:
            animal = Animals.objects.get(id=id)
            animal.delete()  # Xóa animal.
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
