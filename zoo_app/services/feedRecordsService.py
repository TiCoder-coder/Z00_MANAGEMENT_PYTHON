from zoo_app.models import FeedRecord, Food, Animals
from zoo_app.serializers.createFeedRecordDto import CreateFeedRecordDto
from zoo_app.serializers.updateFeedRecordDto import UpdateFeedRecordDto


class feedRecordsService:
    # Hàm tạo feedrecord.
    def createFeedrecord(self, dto: CreateFeedRecordDto):
        # Kiểm tra feedrecord đã tồn tại chưa.
        try:
            existed = FeedRecord.objects.filter(
                idFeedRecord=dto.idFeedRecord).first()
            if existed:
                return {
                    "status": "error",
                    "message": f"FeedRecord with id {dto.idFeedRecord} already exists"
                }
            food_exists = Food.objects.filter(idFood=dto.idFood).first()
            if not food_exists:
                return {
                    "status": "error",
                    "message": f"FoodID {dto.idFood} in feed record not found"
                }
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
            new_record.save()  # Lưa vào database.

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
    # Hàm trả về danh sách feedrecord.

    def reviewFeedrecord(self):
        # Kiểm tra danh sách feedrecord đã tồn tại chưa và trả về danh sách feedrecord.
        try:
            records = FeedRecord.objects.all()
            if not records:
                return {
                    "status": "success",
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
    # Hàm cập nhật thông tin cho feedrecord.

    def updateFeedRecord(self, idFeedRecord: str, dto: UpdateFeedRecordDto):
        # Kiểm tra feedrecord đã tồn tại chưa và cập nhật.
        try:
            record = FeedRecord.objects.filter(
                idFeedRecord=idFeedRecord).first()
            if not record:
                return {
                    "status": "error",
                    "message": f"FeedRecord with id {idFeedRecord} not found"
                }
            if dto.foodId:
                food_exists = Food.objects.filter(idFood=dto.foodId).first()
                if not food_exists:
                    return {
                        "status": "error",
                        "message": f"FoodId {dto.foodId} not found"
                    }
                record.foodId = dto.foodId
            if dto.animalIdFeedRecord:
                animal_exists = Animals.objects.filter(
                    id=dto.animalIdFeedRecord).first()
                if not animal_exists:
                    return {
                        "status": "error",
                        "message": f"AnimalId {dto.animalIdFeedRecord} not found"
                    }
                record.animalIdFeedRecord = dto.animalIdFeedRecord
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
    # Hàm xóa feedrecord.

    def deleteFeedRecord(self, idFeedRecord: str):
        # Kiểm tra feedrecord cần xóa có tồn tại chưa.
        try:
            record = FeedRecord.objects.filter(
                idFeedRecord=idFeedRecord).first()
            if not record:
                return {
                    "status": "error",
                    "message": f"FeedRecord with id {idFeedRecord} not found"
                }
            record.delete()  # Xóa feedrecord.
            return {
                "status": "success",
                "message": f"FeedRecord with id {idFeedRecord} delete successfully"
            }
        except Exception as e:
            return {
                "status": "erros",
                "message": str(e)
            }
