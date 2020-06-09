from rest_framework import serializers
from assets import models
# DRF的异常处理模块
from rest_framework.views import exception_handler


class UserSerializer(serializers.ModelSerializer):
    # 为了健壮性和安全性考虑，自定义字段名不要和model原字段相同，相同可能有问题
    # 序列化的字段如果是中文的，为了显示中文，后面在视图里面必须ensure_ascii=False
    type = serializers.CharField(source='get_user_type_display')  # row.get_user_type_display()内部帮我们加括号调用
    group = serializers.CharField(source='group.group_name')
    # 业务线，与用户是多对多关系
    business_lines = serializers.SerializerMethodField()

    def get_business_lines(self, rows):
        business_lines_obj = rows.business.all()   # 多对多关系，把用户关联的所有业务线对象拿到
        ret = []
        for item in business_lines_obj:
            ret.append({'name': item.name, 'business_manager': item.business_manager})
        return ret

    class Meta:
        model = models.UserProfile
        field = ('name', 'password', 'type', 'group', 'business_lines', 'phone')
        extra_kwargs = {
            'name': {
                'required': True,
                'error_messages': {
                    'required': '这是必填项'
                }
            },
            'password': {
                'required': True,
                'write_only': True,
                'min_length': 6,
                'error_messages': {
                    'required': '这是必填项',
                    'min_length': '密码至少为6位'
                }
            }
        }

    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("手机号格式错误")

    def validate(self, attrs):
        group = attrs.get('group')
        if models.UserGroupProfile.objects.filter(group_name=group):
            raise serializers.ValidationError('请检查组名是否正确')


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.UserGroupProfile
        field = '__all__'
