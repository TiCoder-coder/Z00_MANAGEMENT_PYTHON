from zoo_app.models import Foods
from zoo_app.serializers.createFoodDto import CreateFoodDto
from zoo_app.serializers.updateFoodDto import UpdateFoodDto


class foodService:
    # Hàm tạo food.
    def createFood(self, dto: CreateFoodDto):
        # Kiểm tra food đã tồn tại chưa và trả vế danh sách food.
        try:
            if Foods.objects.filter(idFood=dto.idFood).exists():
                return {
                    "status": "error",
                    "message": f"Food with id {dto.idFood} already exists"
                }
            new_food = Foods(
                idFood=dto.idFood,
                nameFood=dto.nameFood,
                typeFood=dto.typeFood,
                caloriesPerUnit=dto.caloriesPerUnit
            )
            new_food.save()  # Lưu vào database.
            return {
                "status": "success",
                "message": "Food created successfully",
                "data": {
                    "idFood": new_food.idFood,
                    "nameFood": new_food.nameFood,
                    "typeFood": new_food.typeFood,
                    "caloriesPerUnit": new_food.caloriesPerUnit
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    # Hàm trả về danh sách food.

    def reviewFood(self):
        # Kiểm tra danh sách food có tồn tại chưa và trả về kết quả.
        try:
            foods = Foods.objects.all()
            data = []
            for f in foods:
                data.append({
                    "idFood": f.idFood,
                    "nameFood": f.nameFood,
                    "typeFood": f.typeFood,
                    "caloriesPerUnit": f.caloriesPerUnit
                })
            return {
                "status": "success",
                "message": "Food list retrieved successfully",
                "data": data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    # Hàm cập nhật thông tin food.

    def updateFood(self, idFood: str, dto: UpdateFoodDto):
        # Kiểm tra food cần cập nhật đã tồn tại và trả về kết quả.
        try:
            food = Foods.objects.filter(idFood=idFood).first()
            if not food:
                return {
                    "status": "error",
                    "message": f"Food with id {idFood} not found"
                }
            if dto.nameFood is not None:
                food.nameFood = dto.nameFood
            if dto.typeFood is not None:
                food.typeFood = dto.typeFood
            if dto.caloriesPerUnit is not None:
                food.caloriesPerUnit = dto.caloriesPerUnit

            food.save()  # Lưu vào database.
            return {
                "status": "success",
                "message": "Food updated successfully",
                "data": {
                    "idFood": food.idFood,
                    "nameFood": food.nameFood,
                    "typeFood": food.typeFood,
                    "caloriesPerUnit": food.caloriesPerUnit
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    # Hàm xóa food.

    def deleteFood(self, idFood: str):
        # Kiểm tra giá trị food cần xóa đã tồn tại chưa.
        try:
            food = Foods.objects.filter(idFood=idFood).first()
            if not food:
                return {
                    "status": "error",
                    "message": f"Food with id {idFood} not found"
                }

            food.delete()  # Xóa food.
            return {
                "status": "success",
                "message": f"Food with id {idFood} deleted successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
