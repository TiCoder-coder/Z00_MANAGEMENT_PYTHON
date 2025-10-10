from zoo_app.models import Foods
from zoo_app.serializers.createFoodDto import CreateFoodDto
from zoo_app.serializers.updateFoodDto import UpdateFoodDto


class foodService:
    # Tạo mới loại thức ăn
    def createFood(self, dto: CreateFoodDto):
        # Kiểm tra idFood đã tồn tại trong database chưa.
        existed = Foods.object.filter(idFood=dto.idFood).first()
        if existed:
            raise ValueError(f"Food with id {dto.idFood} already exists")

        # Nếu chưa tồn tại tại object mới và lưu vào database
        new_food = Foods(
            idFood=dto.idFood,
            nameFood=dto.nameFood,
            typeFood=dto.typeFood,
            caloriesPerUnit=dto.caloriesPerUnit
        )
        new_food.save()  # Lưu object vào mongodb

        # Trả về dữ liệu vừa tạo
        return {
            "idFood": dto.idFood,
            "nameFood": dto.nameFood,
            "typeFood": dto.typeFood,
            "caloriesPerUnit": dto.caloriesPerUnit
        }

    def reviewFood(self):
        # Xuất thông tin tất cả thức ăn.
        foods = Foods.object.all()  # Lây toàn bộ document trong collection foods
        # Nếu không có dữ liệu trả về mảng rỗng
        if not foods:
            return []
        # Trả về danh sách dict
        result = []
        for food in foods:
            result.append(food.to_dict())
        return result

    def updateFood(self, idFood: str, dto: UpdateFoodDto):
        # Dùng để cập nhật thông tin (chỉ manager mới được phép)
        # Kiểm tra idFood có tồn tại không.
        food = Foods.object.filter(idFood=idFood).first()
        if not food:
            return None
        # Cập nhật từng filed nếu dto tồn tại
        if dto.nameFood:
            food.nameFood = dto.nameFood
        if dto.typeFood:
            food.typeFood = dto.typeFood
        if dto.caloriesPerUnit:
            food.caloriesPerUnit = dto.carloriesPerUnit

        # Lưu thay đổi.
        food.save()

        # Trả vê thông tin sau khi cập nhật.
        return {
            "idFood": idFood,
            "nameFood": food.nameFood,
            "typeFood": food.typeFood,
            "caloriesPerUnit": food.caloriesPerUnit
        }

    def deleteFood(self, idFood: str):
        # Dùng để xóa 1 loại thức ăn (chỉ manager được phép)
        # Kiểm tra idFood có tồn tại không.

        food = Foods.object.filter(idFood=idFood).first()
        if not food:
            return False

        food.delete()
        return True
