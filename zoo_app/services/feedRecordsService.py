from zoo_app.models import FeedRecord, Food, Animals
from zoo_app.serializers.createFeedRecordDto import CreateFeedRecordDto
from zoo_app.serializers.updateFeedRecordDto import UpdateFeedRecordDto


class feedRecordsService:
    # Lớp này dùng xử lí toàn bộ cho bảng feedrecords

    # Tạo mới FeedRecord
    def createFeedrecord(self, dto: CreateFeedRecordDto):
        # Thêm try/except
        try:
            # Kiểm tra có trùng idFeedRecord.
            existed = FeedRecord.objects.filter(
                idFeedRecord=dto.idFeedRecord).first()
            if existed:
                return {
                    "status": "error",
                    "message": f"FeedRecord with id {dto.idFeedRecord} already exists"
                }
            # kiểm tra food có tồn tại không.
            food_exists = Food.objects.filter(idFood=dto.idFood).first()
            if not food_exists:
                return {
                    "status": "error",
                    "message": f"FoodID {dto.idFood} in feed record not found"
                }
            # Kiểm tra animal có tồn tại.
            animal_exists = Animals.objects.filter(
                id=dto.animalIdFeedRecord).first()
            if not animal_exists:
                return {
                    "status": "error",
                    "message": f"AnimalId {dto.animalIdFeedRecord} in feed record not found"
                }

            new_record = FeedRecord(
                idFeedRecord=dto.idFeedRecord,
                animalIdFeedRecord=dto.animalIdFeedRecord,
                foodId=dto.foodId,
                quantity=dto.quantity,
                feedAt=dto.feedAt
            )

            new_record.save()

            return {
                "status": "success",
                "message": "FeedRecord created successfully",
                "data": {
                    "idFeedRecord": new_record.idFeedRecord,
                    "animalIdFeedRecord": new_record.animalIdFeedRecord,
                    "foodId": new_record.foodId,
                    "quantity": new_record.quantity,
                    "feedAt": new_record.feedAt
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def reviewFeedrecord(self):
        # kiểm tra try/except
        try:
            records = FeedRecord.objects.all()
            if not records:
                return {
                    "status": "success",  # API hoạt động bình thường.
                    "message": "No feed records found",
                    "hasData": False,
                    "data": [],
                }
            data = []
            for r in records:
                data.append({
                    "idFeedRecord": r.idFeedRecord,
                    "animalIdFeedRecord": r.animalIdFeedRecord,
                    "foodId": r.foodId,
                    "quantity": r.quantity,
                    "feedAt": r.feedAt
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

    def updateFeedRecord(self, idFeedRecord: str, dto: UpdateFeedRecordDto):
        # Thêm try/excpet
        try:
            record = FeedRecord.objects.filter(
                idFeedRecord=idFeedRecord).first()
            if not record:
                return {
                    "status": "error",
                    "message": f"FeedRecord with id {idFeedRecord} not found"
                }

            # Kiểm tra foodId
            if dto.foodId:
                food_exists = Food.objects.filter(idFood=dto.foodId).first()
                if not food_exists:
                    return {
                        "status": "error",
                        "message": f"FoodId {dto.foodId} not found"
                    }
                record.foodId = dto.foodId

            # Kiểm tra animalId.
            if dto.animalIdFeedRecord:
                animal_exists = Animals.objects.filter(
                    id=dto.animalIdFeedRecord).first()
                if not animal_exists:
                    return {
                        "status": "error",
                        "message": f"AnimalId {dto.animalIdFeedRecord} not found"
                    }
                record.animalIdFeedRecord = dto.animalIdFeedRecord

            # Cập nhật quantity và feedAt
            if dto.quantity is not None:
                record.quantity = dto.quantity
            if dto.feedAt is not None:
                record.feedAt = dto.feedAt

            record.save()  # Lưu vào database.

            return {
                "status": "success",
                "message": "FeedRecord updated successfully",
                "data": {
                    "idFeedRecord": record.idFeedRecord,
                    "animalFeedRecord": record.animalFeedRecord,
                    "foodId": record.foodId,
                    "quantity": record.quantity,
                    "feedAt": record.feedAt
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def deleteFeedRecord(self, idFeedRecord: str):
        # Thêm try/except
        try:
            record = FeedRecord.objects.filter(
                idFeedRecord=idFeedRecord).first()
            if not record:
                return {
                    "status": "error",
                    "message": f"FeedRecord with id {idFeedRecord} not found"
                }
            record.delete()
            return {
                "status": "success",
                "message": f"FeedRecord with id {idFeedRecord} delete successfully"
            }
        except Exception as e:
            return {
                "status": "erros",
                "message": str(e)
            }
