from zoo_app.models import Foods
from zoo_app.serializers.createFoodDto import CreateFoodDto
from zoo_app.serializers.updateFoodDto import UpdateFoodDto


class foodService:
    # Tạo mới loại thức ăn
    def createFood(self, dto: CreateFoodDto):
        # Thêm try/except
        try:
            # Kiểm tra idFood đã tồn tại.
            if Foods.objects.filter(idFood=dto.idFood).exists():
                return {
                    "status": "error",
                    "message": f"Food with id {dto.idFood} already exists"
                }
            # Tạo object mới và lưu vào database
            new_food = Foods(
                idFood=dto.idFood,
                nameFood=dto.nameFood,
                typeFood=dto.typeFood,
                caloriesPerUnit=dto.caloriesPerUnit
            )
            new_food.save()

            # Trả về dữ liệu vừa tạo.
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

    def reviewFood(self):
        # Thêm try/except
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

            # Trả về danh sách
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

    def updateFood(self, idFood: str, dto: UpdateFoodDto):
        # Thêm try/except
        try:
            food = Foods.objects.filter(idFood=idFood).first()
            if not food:
                return {
                    "status": "error",
                    "message": f"Food with id {idFood} not found"
                }

            # Cập nhật từng filed nếu có giá trị.
            if dto.nameFood is not None:
                food.nameFood = dto.nameFood
            if dto.typeFood is not None:
                food.typeFood = dto.typeFood
            if dto.caloriesPerUnit is not None:
                food.caloriesPerUnit = dto.caloriesPerUnit

            food.save()

            # Trả về dict
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

    def deleteFood(self, idFood: str):
        # Thêm try/except
        try:
            # Kiểm tra idFood có tồn tại không.
            food = Foods.objects.filter(idFood=idFood).first()
            if not food:
                return {
                    "status": "error",
                    "message": f"Food with id {idFood} not found"
                }

            food.delete()

            # Trả về thông tin xóa thành công.
            return {
                "status": "success",
                "message": f"Food with id {idFood} deleted successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
