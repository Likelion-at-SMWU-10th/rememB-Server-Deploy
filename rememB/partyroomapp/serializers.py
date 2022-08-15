from rest_framework import serializers
from letterapp.models import *

class PartyroomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Letter
        fields=(
            'id',
            'user',
            'imgfolder_no',
            'img_no',
            'position_x',
            'position_y'
        )
