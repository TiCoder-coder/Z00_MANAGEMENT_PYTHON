from rest_framework import serializers
from zoo_app.models.animalsModels import Animal
from zoo_app.models.enclosuresModel import Enclosure
from zoo_app.enums.enums import Gender, HealthStatus
class CreateAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 
                  'name', 
                  'age', 
                  'species', 
                  'gender', 
                  'weight', 
                  'healthStatus', 
                  'enclosureId',
                  'createAt', 
                  'updateAt'
                ] 
    id=serializers.CharField(min_length=3, max_length=100, required=True)   
    name=serializers.CharField(min_length=3, max_length=100, required=True)
    age=serializers.IntegerField(min_value=0, required=True)
    species=serializers.CharField(min_length=3, max_length=100, required=True)
    gender=serializers.ChoiceField(choices=Gender.choices(), required=True)
    weight=serializers.FloatField(min_value=0, required=True)
    healthStatus=serializers.ChoiceField(choices=HealthStatus.choices(), required=True)
    enclosureId = serializers.PrimaryKeyRelatedField(queryset=Enclosure.objects.all(), source='enclosure',required=True)
    createAt=serializers.DateTimeField(read_only=True)
    updateAt=serializers.DateField(read_only=True)
    def validate(self, attrs):
        """
        Xác thực liên kết giữa các trường
        """
        # Lấy giá trị hiện tại từ instance nếu có
        age = getattr(self.instance, 'age', 0) if self.instance else 0
        weight = getattr(self.instance, 'weight', 0) if self.instance else 0
        species = getattr(self.instance, 'species', '') if self.instance else ''
        
        # Xác thực tỷ lệ tuổi vs cân nặng để đảm bảo hợp lý
        if age is not None and weight is not None:
            # Kiểm tra cả hai đều là số hợp lệ
            if age == 0 and weight > 50:  # Động vật non nhỏ không nên quá nặng
                raise serializers.ValidationError("Newborn animals typically weigh less than 50kg")
            
            # Kiểm tra tỷ lệ tuổi và cân nặng hợp lý
            if age > 0 and weight > 0:
                # Tỷ lệ cân nặng/tuổi không nên quá cao (ví dụ: 1000kg/tuổi)
                if weight / age > 1000:
                    raise serializers.ValidationError("Weight to age ratio seems unrealistic")
            
            # Kiểm tra động vật trưởng thành phải có cân nặng đủ
            if age > 5 and weight < 1:
                raise serializers.ValidationError("Adult animals should weigh at least 1kg")
        
        # Kiểm tra tính nhất quán của dữ liệu về tuổi thọ theo loài
        if species and age is not None:
            # Một số loài có tuổi thọ tối đa khác nhau
            species_lower = species.lower()
            
            # Dictionary định nghĩa tuổi thọ tối đa cho các loài
            max_ages = {
                'elephant': 70,
                'lion': 25,
                'tiger': 26,
                'bear': 40,
                'turtle': 150,
                'tortoise': 150,
                'parrot': 80,
                'eagle': 30,
                'monkey': 40,
                'gorilla': 50,
                'dog': 20,
                'cat': 20,
                'rabbit': 12,
                'hamster': 4
            }
            
            for animal_type, max_age in max_ages.items():
                if animal_type in species_lower and age > max_age:
                    raise serializers.ValidationError(
                        f"{animal_type.capitalize()}s typically don't live beyond {max_age} years"
                    )
        
        return attrs
