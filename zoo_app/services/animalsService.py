from django.core.exceptions import ObjectDoesNotExist
from zoo_app.models.animalsModels import AnimalsModel
from rest_framework.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)


class AnimalService:
    # Tạo mới animal
    @staticmethod
    def create_animal(validated_data):
        try:
            animal = AnimalsModel.objects.create(**validated_data)
            logger.info(f"Created animal: {animal.name}")
            return {
                "status": "success",
                "message": "Animal created successfully.",
                "data": animal
            }
        except Exception as e:
            logger.error(f"Error creating animal: {e}")
            raise ValidationError(f"Error creating animal: {str(e)}")

    # Lấy tất cả animal
    @staticmethod
    def review_get_all_animal():
        try:
            animals = AnimalsModel.objects.all()
            logger.info("Fetched all animals")
            return animals
        except Exception as e:
            logger.error(f"Error fetching animals: {e}")
            raise ValidationError(f"Error fetching animals: {str(e)}")

    # Lấy 1 animal theo id
    @staticmethod
    def review_animal_by_id(idAnimal):
        try:
            animal = AnimalsModel.objects.get(id=idAnimal)
            logger.info(f"Found animal with id {idAnimal}")
            return animal
        except ObjectDoesNotExist:
            logger.warning(f"Animal witd id {idAnimal} not found")
            raise ValidationError(f"Animla with id {idAnimal} not found")
        except Exception as e:
            logger.error(f"Error getting animal {idAnimal}: {e}")
            raise ValidationError(f"Error getting animal: {str(e)}")

    # Cập nhật animal

    @staticmethod
    def update_animal(idAnimal, validated_data):
        try:
            animal = AnimalsModel.objects.get(id=idAnimal)
            for key, value in validated_data.items():
                setattr(animal, key, value)
            animal.save()
            logger.info(f"Update animal {idAnimal}")
            return {
                "status": "success",
                "message": "Animal updated successfully",
                "data": animal
            }
        except ObjectDoesNotExist:
            logger.warning(f"Animal with id {idAnimal} nt found for update")
            raise ValidationError(f"Animal with id {idAnimal} not found")
        except Exception as e:
            logger.error(f"Error updating animal {idAnimal}: {e}")
            raise ValidationError(f"Error updating animal: {str(e)}")

    # Xóa animal
    @staticmethod
    def delete_animal(idAnimal):
        try:
            animal = AnimalsModel.objects.get(id=idAnimal)
            animal.delete()
            logger.info(f"Delete animal {idAnimal}")
            return {
                "status": "success",
                "message": f"Animal with id {idAnimal} delete successfully"
            }
        except ObjectDoesNotExist:
            logger.warning(f"Animal with id {idAnimal} not found for delete")
            raise ValidationError(f"Animla with id {idAnimal} not found")
        except Exception as e:
            logger.error(f"Error deleting animal {idAnimal}: {e}")
            raise ValidationError(f"Error deleting animal: {str(e)}")
