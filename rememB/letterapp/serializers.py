from rest_framework import serializers
from .models import *

class LetterSerializer(serializers.ModelSerializer):
    #user=serializers.ReadOnlyField(source='user.uuid')
    class Meta:
        model=Letter
        fields=('id','user','letter_from','content','imgfolder_no','img_no','position_x','position_y','created_at')


class LetterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Letter
        exclude=['created_at']

class LetterSumSerializer(serializers.ModelSerializer):
    class Meta:
        model=Letter
        fields=['id','user','letter_from','imgfolder_no','img_no','position_x','position_y']
