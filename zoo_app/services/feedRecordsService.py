import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from zoo_app.models.feedRecordsModel import FeedRecordModel
from zoo_app.models.animalsModels import AnimalModel

logger = logging.getLogger(__name__)


class FeedRecordService:
    # Tạo feedRecord
    @staticmethod
    def create_feed_record(validated_data):
        try:
            animal_id = validated_data.get("animal")
            if not animal_id:
                raise ValidationError("Animal ID is required")

            try:
                animal = AnimalModel.objects.get(id=animal_id.id)
            except ObjectDoesNotExist:
                raise ValidationError(f"Animal with ID {animal_id} not found")
            feed_record = FeedRecordModel.objects.create(**validated_data)
            logger.info(f"Created feed record for animal: {animal.name}")
            return feed_record
        except ValidationError as ve:
            logger.warning(f"Validation error creating feed record: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Error creating feed record: {str(e)}")
            raise ValidationError(f"Can not create feed record: {str(e)}")

    # Lấy danh sách feedRecord cho animal
    @staticmethod
    def review_list_feed_record():
        try:
            records = FeedRecordService.objects.all()
            logger.info("List all feed record")
            return records
        except Exception as e:
            logger.error(f"Error listing feed records: {str(e)}")
            raise ValidationError(f"Can not list feed records: {str(e)}")
    # Lấy danh sách feedRecord theo id

    @staticmethod
    def get_feed_record_by_id(idRecord):
        try:
            record = FeedRecordModel.objects.get(id=idRecord)
            logger.info(f"Retrieved feed record ID: {idRecord}")
            return record
        except ObjectDoesNotExist:
            logger.warning(f"Feed record not found: {idRecord}")
            raise ValidationError(f"Feed record with ID {idRecord} not found")
        except Exception as e:
            logger.error(f"Error retrieving feed record: {str(e)}")
            raise ValidationError(f"Can not get feed record: {str(e)}")

    # Cập nhật feedRecod
    @staticmethod
    def update_feed_record(idRecord, validated_data):
        try:
            record = FeedRecordModel.objects.get(id=idRecord)
            for key, value in validated_data.items():
                setattr(record, key, value)
            record.save()
            logger.info(f"Updated feed record ID: {idRecord}")
            return record
        except ObjectDoesNotExist:
            logger.warning(f"Feed record not found for update: {idRecord}")
            raise ValidationError(f"Feed record with ID {idRecord} not found")
        except Exception as e:
            logger.error(f"Error updating feed record: {str(e)}")
            raise ValidationError(f"Can not update feed record: {str(e)}")

    # Xóa feedRecord
    @staticmethod
    def delete_feed_record(idRecord):
        try:
            record = FeedRecordModel.objects.get(id=idRecord)
            record.delete()
            logger.info(f"Delete feed record ID: {idRecord}")
        except ObjectDoesNotExist:
            logger.warning(f"Feed record not found for delete: {idRecord}")
            raise ValidationError(f"Feed record with ID {idRecord} not found")
        except Exception as e:
            logger.error(f"Error deleting feed record: {str(e)}")
            raise ValidationError(f"Can not delete feed record: {str(e)}")
