from rest_framework import serializers
from zoo_app.models import FeedRecords
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
import re

class UpdateFeedRecordsSerializer(serializers.ModelSerializer):
    """
    Serializer để cập nhật lịch sử cho ăn hiện có
    """
    
    class Meta:
        """
        Meta class cho UpdateFeedRecordsSerializer
        """
        model = FeedRecords
        fields = [
            'animalIdFeedRecord',
            'foodId',
            'quantity',
            'feedAt'
        ]
    
    def validate_animalIdFeedRecord(self, value):
        """
        Xác thực ID động vật tồn tại
        """
        if value is None:
            return value
            
        from zoo_app.models import Animals
        
        # Kiểm tra ID động vật không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Animal ID cannot be empty")
        
        # Kiểm tra ID động vật có định dạng hợp lệ
        if not re.match(r'^[a-zA-Z0-9\-_]+$', value.strip()):
            raise serializers.ValidationError("Animal ID can only contain letters, numbers, hyphens, and underscores")
        
        try:
            # Kiểm tra ID động vật tồn tại
            animal = Animals.objects.get(id=value)
            
            # Kiểm tra động vật có đang hoạt động không
            if hasattr(animal, 'isActive') and animal.isActive is False:
                raise serializers.ValidationError("Animal is not active")
            
            # Kiểm tra động vật có sức khỏe tốt không
            if hasattr(animal, 'healthStatus'):
                # Không cho ăn nếu động vật đã chết hoặc trong tình trạng nguy kịch
                critical_statuses = ['CRITICAL', 'DEAD', 'DECEASED']
                if animal.healthStatus.upper() in critical_statuses:
                    raise serializers.ValidationError(
                        f"Cannot feed animal with {animal.healthStatus} health status"
                    )
                
        except Animals.DoesNotExist:
            raise serializers.ValidationError("Animal with this ID does not exist")
        except Exception as e:
            raise serializers.ValidationError(f"Error validating animal: {str(e)}")
        
        return value.strip()
    
    def validate_foodId(self, value):
        """
        Xác thực ID thức ăn tồn tại
        """
        if value is None:
            return value
            
        from zoo_app.models import Foods
        
        # Kiểm tra ID thức ăn không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Food ID cannot be empty")
        
        # Kiểm tra ID thức ăn có định dạng hợp lệ
        if not re.match(r'^[a-zA-Z0-9\-_]+$', value.strip()):
            raise serializers.ValidationError("Food ID can only contain letters, numbers, hyphens, and underscores")
        
        try:
            # Kiểm tra ID thức ăn tồn tại
            food = Foods.objects.get(idFood=value)
            
            # Kiểm tra thức ăn có đang hoạt động không
            if hasattr(food, 'isActive') and food.isActive is False:
                raise serializers.ValidationError("Food is not active")
            
            # Kiểm tra thức ăn có hết hạn không
            if hasattr(food, 'expiryDate') and food.expiryDate:
                from django.utils import timezone
                today = timezone.now().date()
                if food.expiryDate < today:
                    raise serializers.ValidationError("Food has expired")
                    
        except Foods.DoesNotExist:
            raise serializers.ValidationError("Food with this ID does not exist")
        except Exception as e:
            raise serializers.ValidationError(f"Error validating food: {str(e)}")
        
        return value.strip()
    
    def validate_quantity(self, value):
        """
        Xác thực số lượng cho ăn
        """
        if value is None:
            return value
            
        # Kiểm tra số lượng cho ăn là số
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Quantity must be a number")
        
        # Kiểm tra số lượng cho ăn không âm
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        
        # Kiểm tra số lượng cho ăn không vượt quá 100
        if value > 100:
            raise serializers.ValidationError("Quantity cannot exceed 100 units")
        
        # Kiểm tra số lượng cho ăn không phải là số thập phân quá phức tạp
        if isinstance(value, float) and len(str(value).split('.')[-1]) > 2:
            raise serializers.ValidationError("Quantity cannot have more than 2 decimal places")
        
        return value
    
    def validate(self, attrs):
        """
        Xác thực liên kết giữa các trường
        """
        # Lấy giá trị hiện tại từ instance nếu có
        current_animal_id = getattr(self.instance, 'animalIdFeedRecord', None) if self.instance else None
        current_food_id = getattr(self.instance, 'foodId', None) if self.instance else None
        current_quantity = getattr(self.instance, 'quantity', 0) if self.instance else 0
        current_feed_at = getattr(self.instance, 'feedAt', None) if self.instance else None
        
        # Sử dụng giá trị mới nếu có, nếu không thì dùng giá trị hiện tại
        animal_id = attrs.get('animalIdFeedRecord', current_animal_id)
        food_id = attrs.get('foodId', current_food_id)
        quantity = attrs.get('quantity', current_quantity)
        feed_at = attrs.get('feedAt', current_feed_at)
        
        # Xác thực tính phù hợp của thức ăn với loài động vật
        if animal_id and food_id:
            from zoo_app.models import Animals, Foods
            try:
                animal = Animals.objects.get(id=animal_id)
                food = Foods.objects.get(idFood=food_id)
                
                # Kiểm tra thức ăn phù hợp với loài động vật
                if hasattr(food, 'isSuitableForSpecies') and not food.isSuitableForSpecies(animal.species):
                    raise serializers.ValidationError(
                        f"Food {food.nameFood} is not suitable for {animal.species}"
                    )
                
                # Kiểm tra số lượng phù hợp với kích thước động vật (nhắc nhở, không bắt buộc)
                if quantity and hasattr(animal, 'weight') and animal.weight:
                    if animal.weight < 5 and quantity > 10:  # Động vật rất nhỏ
                        raise serializers.ValidationError(
                            "Quantity seems too large for very small animal (under 5kg)"
                        )
                    elif animal.weight > 2000 and quantity < 5:  # Động vật rất lớn
                        raise serializers.ValidationError(
                            "Quantity seems too small for very large animal (over 2000kg)"
                        )
                
            except (Animals.DoesNotExist, Foods.DoesNotExist):
                raise serializers.ValidationError("Invalid animal or food ID")
            except Exception as e:
                raise serializers.ValidationError(f"Error validating animal-food compatibility: {str(e)}")
        
        # Kiểm tra không có bản ghi trùng lặp gần giống (trong vòng 1 phút)
        if animal_id and food_id and feed_at:
            from zoo_app.models import FeedRecords
            
            # Đảm bảo feed_at là datetime object
            if isinstance(feed_at, str):
                try:
                    feed_at = datetime.fromisoformat(feed_at.replace('Z', '+00:00'))
                except ValueError:
                    pass  # Đã được validate ở validate_feedAt
            
            if isinstance(feed_at, datetime):
                # Kiểm tra bản ghi trùng lặp (trừ bản ghi hiện tại nếu đang update)
                time_window_start = feed_at - timedelta(minutes=1)
                time_window_end = feed_at + timedelta(minutes=1)
                
                duplicate_query = FeedRecords.objects.filter(
                    animalIdFeedRecord=animal_id,
                    foodId=food_id,
                    feedAt__range=(time_window_start, time_window_end)
                )
                
                # Loại trừ bản ghi hiện tại nếu đang update
                if self.instance and hasattr(self.instance, 'idFeedRecord'):
                    duplicate_query = duplicate_query.exclude(idFeedRecord=self.instance.idFeedRecord)
                
                if duplicate_query.exists():
                    raise serializers.ValidationError(
                        "A similar feed record already exists within 1 minute of this time"
                    )
        
        return attrs
    
    def validate_feedAt(self, value):
        """
        Xác thực thời gian cho ăn
        """
        if value is None:
            return value
        
        # Nếu là string, chuyển đổi sang datetime
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                raise serializers.ValidationError(
                    "Invalid feedAt datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                )
        
        # Đảm bảo là timezone-aware
        if hasattr(value, 'tzinfo') and value.tzinfo is None:
            value = timezone.make_aware(value)
        
        # Kiểm tra không trong tương lai
        now = timezone.now()
        if value > now:
            raise serializers.ValidationError("Feed time cannot be in the future")
        
        # Kiểm tra không quá xa trong quá khứ (30 ngày)
        thirty_days_ago = now - timedelta(days=30)
        if value < thirty_days_ago:
            raise serializers.ValidationError(
                "Feed time cannot be more than 30 days in the past"
            )
        
        return value
    
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Cập nhật instance lịch sử cho ăn hiện có với transaction safety
        """
        # Kiểm tra instance có tồn tại không
        if not instance:
            raise serializers.ValidationError("Feed record instance not found")
        
        # Cập nhật instance lịch sử cho ăn hiện có
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
            else:
                raise serializers.ValidationError(f"Invalid field: {attr}")
        
        # Lưu instance
        instance.save()
        
        # Log thay đổi (có thể thêm vào đây)
        # logger.info(f"Feed record {instance.idFeedRecord} updated: {validated_data}")
        
        return instance
