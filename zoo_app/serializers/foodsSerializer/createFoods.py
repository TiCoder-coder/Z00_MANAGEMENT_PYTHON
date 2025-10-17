from rest_framework import serializers
from zoo_app.models.foodsModel import Food 
class CreateFoodsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            'idFood',
            'nameFood',
            'typeFood',
            'caloriesPerUnit'
        ]
    idFood=serializers.CharField(min_length=3, max_length=100, required=True, help_text="Mã định danh duy nhất cho loại thức ăn")
    nameFood=serializers.CharField(min_length=3, max_length=100, required=True, help_text="Tên loại thức ăn")
    typeFood=serializers.ChoiceField(choices=Food.choices(), required=True, help_text="Loại thức ăn (thịt, rau, hạt, ...)")
    caloriesPerUnit=serializers.FloatField(min_value=0, max_value=300, required=True, help_text="Lượng calo mỗi đơn vị thức ăn")
    def validate_nameFood(self, value):
        """
        Đảm bảo không trùng tên thức ăn
        """
        if Food.objects.filter(nameFood__iexact=value).exists():
            raise serializers.ValidationError("This food name already exists.")
        return value
