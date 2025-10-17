import logging
from django.core.exceptions import ObjectDoesNotExist
from zoo_app.models.managersModel import ManagerModel
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class ManagerService:
    # Tạo mới manager
    @staticmethod
    def create_manager(validated_data):
        try:
            manager = ManagerModel.objects.create(**validated_data)
            logger.info(f"Create manager: {manager.full_name}")
            return {
                "id": str(manager.id),
                "full_name": manager.full_name,
                "role": manager.role,
                "email": manager.email,
                "create_at": manager.create_at
            }
        except Exception as e:
            logger.info(f"Error creating manager: {str(e)}")
            raise ValidationError(f"Error creating manager: {str(e)}")

    # Lấy tất cả danh sách manager
    @staticmethod
    def review_list_manager():
        try:
            managers = ManagerModel.objects.all()
            result = []
            for m in managers:
                result.append({
                    "id": str(m.id),
                    "full_name": m.full_name,
                    "role": m.role,
                    "email": m.email,
                    "create_at": m.create_at
                })
            return result
        except Exception as e:
            raise ValidationError(f"Error fetching managers: {str(e)}")

    # Lấy danh sách manager bằng id
    @staticmethod
    def get_manager_by_id(idManager):
        try:
            manage = ManagerModel.objects.get(id=idManager)
            return {
                "id": str(manage.id),
                "full_name": manage.full_name,
                "role": manage.role,
                "email": manage.email,
                "create_at": manage.create_at
            }
        except ObjectDoesNotExist:
            raise ValidationError(f"Manager with id {idManager} not found")
        except Exception as e:
            raise ValidationError(f"Error getting managewr: {str(e)}")

    # Cập nhật thông tin manager
    @staticmethod
    def update_manager(idManager, validated_data):
        try:
            manager = ManagerModel.objects.get(id=idManager)
            for key, value in validated_data.items():
                setattr(manager, key, value)
            manager.save()
            logger.info(f"Updated manager: {manager.full_name}")
            return {
                "id": str(manager.id),
                "full_name": manager.full_name,
                "role": manager.role,
                "email": manager.email,
                "updated_at": manager.updated_at
            }
        except ObjectDoesNotExist:
            raise ValidationError(f"Manager with id {idManager} not found")
        except Exception as e:
            raise ValidationError(f"Error updating manager: {str(e)}")

    # Xóa thông tin manager
    @staticmethod
    def delete_manager(idManager):
        try:
            manager = ManagerModel.objects.get(id=idManager)
            manager.delete()
            return {
                "message": f"Deleted manager with id {idManager} successfully"
            }
        except ObjectDoesNotExist:
            raise ValidationError(f"Manager with id {idManager} not found")
        except Exception as e:
            raise ValidationError(f"Error deleting manager: {str(e)}")
