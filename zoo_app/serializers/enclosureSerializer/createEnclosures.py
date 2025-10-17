from rest_framework import serializers
from zoo_app.models.enclosuresModel import Enclosure
from zoo_app.enums.enums import Climate
class CreateEnclosuresSerializers(serializers.ModelSerializer):
    class Meta:
        model = Enclosure
        fields = [
            'idEnclosure',
            'nameEnclosure',
            'areaSize',
            'climate',
            'capacity'
                ]         
    idEnclosure=serializers.CharField(min_length=3, max_length=100, required=True, help_text="Mã chuồng trại, duy nhất trong hệ thống")
    nameEnclosure=serializers.CharField(min_length=3, max_length=100, required=True, help_text="Tên chuồng trại")
    areaSize=serializers.CharField(min_length=3, max_length=50, required=True, help_text="Diện tích chuồng")
    climate=serializers.ChoiceField(choices=Climate.choices(), required=True, help_text="Khí hậu của chuồng")
    capacity=serializers.FloatField(min_value=0, required=True, help_text="Sức chứa tối đa của chuồng")
    def validate_nameEnclosure(self, value):
        """
        Không cho phép trùng tên chuồng
        """
        if Enclosure.objects.filter(nameEnclosure__iexact=value).exists():
            raise serializers.ValidationError("Tên chuồng trại đã tồn tại.")
        return value

    def validate_areaSize(self, value):
        """
        Kiểm tra định dạng diện tích
        """
        try:
            size = float(value.replace("m²", "").strip()) if isinstance(value, str) else float(value)
            if size <= 0:
                raise serializers.ValidationError("Diện tích phải lớn hơn 0.")
        except ValueError:
            raise serializers.ValidationError("Giá trị diện tích không hợp lệ.")
        return value
    
    def validate_idEnclosure(self, value):
        """
        Kiểm tra tính duy nhất của id
        """
        if Enclosure.objects.filter(idEnclosure=value).exists():
            raise serializers.ValidationError("Mã chuồng trại đã tồn tại.")
        return value
