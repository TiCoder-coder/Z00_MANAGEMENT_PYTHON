import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from zoo_app.models.enclosuresModel import EnclosureModel

logger = logging.getLogger(__name__)


class EnclosureService:
    # Tạo mới enclosure
    @staticmethod
    def create_enclosure(validated_data):
        try:
            enclosure = EnclosureModel.objects.create(**validated_data)
            logger.info(f"Create enclosure: {enclosure.name}")
            return enclosure
        except Exception as e:
            logger.error(f"Error creating enclosure: {str(e)}")
            raise ValidationError(f"Can not create enclosure: {str(e)}")

    # Lấy danh sách enclosure
    @staticmethod
    def review_list_enclosure():
        try:
            enclosures = EnclosureModel.objects.all()
            logger.info("List all enclosure")
            return enclosures
        except Exception as e:
            logger.error(f"Error listing enclosures: {str(e)}")
            raise ValidationError(f"Can not list enclosures: {str(e)}")

    # Lấy enclosure theo id
    @staticmethod
    def get_enclosure_by_id(idEnclosure):
        try:
            enclosure = EnclosureModel.objects.get(id=idEnclosure)
            logger.info(f"Retrieved enclosure ID: {idEnclosure}")
            return enclosure
        except ObjectDoesNotExist:
            logger.warning(f"Enclosure not found: {idEnclosure}")
            raise ValidationError(f"Enclosure with ID {idEnclosure} not found")
        except Exception as e:
            logger.error(f"Error retrieving enclosure: {str(e)}")
            raise ValidationError(f"Can not get enclosure: {str(e)}")

    # Cập nhật enclosure
    @staticmethod
    def update_enclosure(idEnclosure, validated_data):
        try:
            enclosure = EnclosureModel.objects.get(id=idEnclosure)
            for key, value in validated_data.items():
                setattr(enclosure, key, value)
            enclosure.save()
            logger.info(f"Updated enclosure ID: {idEnclosure}")
            return enclosure
        except ObjectDoesNotExist:
            logger.warning(f"Emclosure not found for update: {idEnclosure}")
            raise ValidationError(f"Enclosure with ID {idEnclosure} not found")
        except Exception as e:
            logger.error(f"Error updating enclosure: {str(e)}")
            raise ValidationError(f"Can not update enclosure: {str(e)}")

    # Xóa enclosure
    @staticmethod
    def delete_enclosure(idEnclosure):
        try:
            enclosure = EnclosureModel.objects.get(id=idEnclosure)
            enclosure.delete()
            logger.info(f"Deleted enclosure ID: {idEnclosure}")
        except ObjectDoesNotExist:
            logger.warning(f"Enclosure not found for delete: {idEnclosure}")
            raise ValidationError(f"Enclosure with ID {idEnclosure} not found")
        except Exception as e:
            logger.error(f"Error deleting enclosure: {str(e)}")
            raise ValidationError(f"Can not delete enclosure: {str(e)}")
