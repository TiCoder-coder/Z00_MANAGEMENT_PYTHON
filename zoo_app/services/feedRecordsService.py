from zoo_app.models import FeedRecord, Food, Animals
from zoo_app.serializers.createFeedRecordDto import CreateFeedRecordDto
from zoo_app.serializers.updateFeedRecordDto import UpdateFeedRecordDto


class feedRecordsService:
    # Lớp này dùng xử lí toàn bộ cho bảng feedrecords
    def createFeedrecord(self, dto: CreateFeedRecordDto):
        # Kiểm tra idFeedRecord có bị trùng không.
        existed = FeedRecord.object.filter(
            idFeedRecord=dto.idFeedRecord).first()
        if existed:
            raise ValueError(
                f"FeedRecord with id {dto.idFeedRecord} already exists")
        # Kiểm tra food tồn tại không.
        food_exists = Food.object.filter(idFood=dto.foodId).first()
        if not food_exists:
            raise ValueError(f"FoodID {dto.foodId} in feed record not found")
        # Kiểm tra animal có tồn tại không.
        animal_exists = Animals.object.filter(
            id=dto.animalIdFeedRecord).first()
        if not animal_exists:
            raise ValueError(
                f"AnimalId {dto.animalIdFeedRecord} in feed record not found")

        # Tạo mới FeedRecord
        new_record = FeedRecord(
            idFeedRecord=dto.idFeedRecord,
            animalIdFeedRecord=dto.animalFeedRecord,
            foodId=dto.foodId,
            quantity=dto.quantity,
            feedAt=dto.feedAt
        )
        new_record.save()

        return {
            "idFeedRecord": new_record.idFeedRecord,
            "animalIdFeedRecord": new_record.animalIdFeedRecord,
            "foodId": new_record.foodId,
            "quantity": new_record.quantity,
            "feedAt": new_record.feedAt
        }

    def reviewFeedrecord(self):
        # Trae về toàn bộ danh dách FeedRecord hiện có.
        records = FeedRecord.object.all()
        return list(records.values())  # Chuyển queryset về dánh sách dict

    def updateFeedRecord(self, idFeedRecord: str, dto: UpdateFeedRecordDto):
        # Kiểm tra FeedRecord có tồn tại không.
        record = FeedRecord.object.filter(idFeedRecord=idFeedRecord).first()
        if not record:
            return None
        # Kiểm tra idFood nếu có.
        if dto.idFood:
            food_exists = Food.objetc.filter(idFood=dto.foodId).first()
            if not food_exists:
                raise ValueError(f"FoodId {dto.foodId} not found")
            record.foodId = dto.foodId
        # Kiểm tra animalId
        if dto.animalIdFeedRecord:
            animal_exists = Animals.object.filter(
                id=dto.animalIdFeedRecord).first()
            if not animal_exists:
                raise ValueError(
                    f"AnimalId {dto.animalIdFeedRecord} not found")
            record.animalIdFeedRecord = dto.animalIdFeedRecord
        # Cập nhật quantity và feedAt
        if dto.quantity:
            record.quantity = dto.quantity
        if dto.feedAt:
            record.feedAt = dto.feedAt

        # Lưu lại
        record.save()
        # Trả về dict
        return {
            "idFeedRecord": record.idFeedRecord,
            "animalIdFeedRecord": record.animalIdFeedRecord,
            "foodId": record.foodId,
            "quantity": record.quantity,
            "feedAt": record.feedAt
        }

    def deleteFeedRecord(self, idFeedRecord: str):
        # Xóa FeedRecord nếu nó tồn tại.
        record = FeedRecord.object.filter(idFeedRecord=idFeedRecord).first()
        if not record:
            return False
        record.delete()
        return True
