import logging
from django.core.exceptions import ObjectDoesNotExist
from zoo_app.models.foodsModel import FoodModel
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class FoodService:
    # Tạo thức ăn mới
    @staticmethod
    def create_food(validated_data):
        try:
            food = FoodModel.objets.create(**validated_data)
            logger.info(f"Create new food: {food.name}")
            return food
        except Exception as e:
            logger.error(f"Error creating food: {str(e)}")
            raise ValidationError(f"Can nnot food: {str(e)}")

    # Lấy tất cả danh sách thức ăn.
    @staticmethod
    def review_lis_foods():
        try:
            foods = FoodModel.objects.all()
            logger.info(f"List all foods")
            return foods
        except Exception as e:
            logger.error(f"Error listing foods: {str(e)}")
            raise ValidationError(f"Can not list foods: {str(e)}")
    # Lấy thức ăn theo id

    @staticmethod
    def get_food_by_id(idFood):
        try:
            food = FoodModel.objects.get(id=idFood)
            logger.info(f"Retrieved food ID: {idFood}")
            return food
        except ObjectDoesNotExist:
            logger.warning(f"Food not found: {idFood}")
            raise ValidationError(f"Food with ID {idFood} not found")
        except Exception as e:
            logger.error(f"Error retrieving food: {str(e)}")
            raise ValidationError(f"Can not get food: {str(e)}")

    # Cập nhật thông tin food
    @staticmethod
    def update_food(idFood, validated_data):
        try:
            food = FoodModel.objects.get(id=idFood)
            for key, value in validated_data.items():
                setattr(food, key, value)
            food.save()
            logger.info(f"Updated food ID: {idFood}")
            return food
        except ObjectDoesNotExist:
            logger.warning(f"Food not found for update: {idFood}")
            raise ValidationError(f"Food with ID {idFood} not found")
        except Exception as e:
            logger.error(f"Error updating food: {str(e)}")
            raise ValidationError(f"Can not update food: {str(e)}")

    # Xóa food
    @staticmethod
    def delete_food(idFood):
        try:
            food = FoodModel.objects.get(id=idFood)
            food.delete()
            logger.info(f"Delete food ID: {idFood}")
            return {
                "message": f"Deleted food with id {idFood} successfully"
            }
        except ObjectDoesNotExist:
            raise ValidationError(f"Food with id {idFood} not found")
        except Exception as e:
            raise ValidationError(f"Error deleting food: {str(e)}")
