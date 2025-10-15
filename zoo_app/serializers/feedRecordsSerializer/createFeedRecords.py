from rest_framework import serializers
from zoo_app.models.feedRecordsModel import FeedRecords
from zoo_app.models.animalsModels import Animal
from zoo_app.models.foodsModel import Food 
class CreateFeedRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedRecords
        fields = [
            'idFeedRecord', 
            'animalIdFeedRecord', 
            'foodId', 
            'quantity',
            'feedAt'
        ]
    idFeedRecord=serializers.CharField(min_length=3, max_length=100, required=True, help_text="Mã bản ghi cho lần cho ăn")
    animalIdFeedRecord = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.all(), required=True, help_text="ID động vật được cho ăn")
    foodId = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), required=True, help_text="ID loại thức ăn được sử dụng")
    quantity=serializers.IntegerField(min_value=0, required=True, help_text="Số lượng thức ăn")
    feedAt=serializers.DateTimeField(read_only=True, help_text="Thời điểm cho ăn")
