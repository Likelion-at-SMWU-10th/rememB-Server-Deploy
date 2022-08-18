from rest_framework import serializers
from .models import *

class LetterSerializer(serializers.ModelSerializer):
    #user=serializers.ReadOnlyField(source='user.uuid')
    class Meta:
        model=Letter
        fields=('id','user','content','imgfolder_no','img_no','position_x','position_y','created_at')


class LetterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Letter
        fields=('id','user','get_img','content')

class LetterSumSerializer(serializers.ModelSerializer):
    class Meta:
        model=Letter
        fields=['id','user','imgfolder_no','img_no','position_x','position_y',]
