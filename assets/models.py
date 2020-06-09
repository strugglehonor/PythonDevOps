from django.db import models


class Assets(models.Model):
    type = (
        ('server', '服务器'),
        ('security', '安全设备'),
        ('network', '网络设备')
    )
    status = (
        (0, '未使用'),
        (1, '已上线'),
        (2, '已下线'),
        (3, '已故障')
    )
    # 资产的唯一标识
    asset_flag = models.CharField(max_length=10, verbose_name='资产编号', unique=True)
    asset_manage_name = models.CharField(max_length=10, verbose_name='资产管理员')
    "这里应该是一对一关系的，不是外键"
    # server = models.ForeignKey(to='Servers', on_delete=models.CASCADE, related_name='asset')
    # office_device = models.ForeignKey(to='Offices', on_delete=models.CASCADE, related_name='asset')
    # network_device = models.ForeignKey(to='Network', on_delete=models.CASCADE, related_name='asset')
    asset_manage_ip = models.GenericIPAddressField(verbose_name='管理ip', blank=True, null=True)
    asset_type = models.CharField(max_length=10, choices=type, default='server', verbose_name='资产类型')
    asset_status = models.SmallIntegerField(choices=status, default=1, verbose_name='资产状态')
    asset_model = models.CharField(max_length=20, verbose_name='资产型号', null=True, blank=True)
    asset_purchase_time = models.DateField(verbose_name='资产的购买日期', null=True, blank=True)
    asset_expire_time = models.DateField(verbose_name='资产的过保日期', null=True, blank=True)
    asset_create_time = models.DateTimeField(auto_created=True, verbose_name='资产入库时间')
    asset_update_time = models.DateTimeField(auto_now_add=True, verbose_name='资产更新时间')
    # manufacturer = models.CharField(max_length=20, verbose_name='厂商', null=True, blank=True)
    manufacturer = models.ForeignKey(to='Manufacturer', verbose_name='厂商', on_delete=models.CASCADE)
    # 资产的位置，用机房和机柜号
    asset_city = models.CharField(max_length=10, verbose_name='资产所在城市')
    asset_idc = models.ForeignKey(to='IDC', on_delete=models.CASCADE, verbose_name='资产所在机房', blank=True, null=True)
    asset_cabinet = models.ForeignKey(to='Cabinet', on_delete=models.CASCADE, verbose_name='资产所在机柜', blank=True, null=True)
    asset_note = models.CharField(max_length=100, verbose_name='备注', blank=True, null=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name
        db_table = 'ops_assets'

    def __str__(self):
        return self.asset_flag


class Manufacturer(models.Model):
    name = models.CharField(max_length=20, verbose_name='厂商名字')
    phone = models.CharField(max_length=11, verbose_name='厂商联系电话')

    class Meta:
        verbose_name = '厂商表'
        verbose_name_plural = verbose_name
        db_table = 'ops_manufacturer'

    def __str__(self):
        return self.name


class IDC(models.Model):
    idc_address = models.CharField(max_length=50, verbose_name='机房地址')
    idc_name = models.CharField(max_length=10, verbose_name='机房名称', unique=True)
    idc_manager = models.CharField(max_length=10, verbose_name='机房的负责人')
    idc_telephone = models.CharField(max_length=11, verbose_name='负责人的电话')
    idc_note = models.CharField(max_length=100, verbose_name='备注', null=True, blank=True)

    class Meta:
        verbose_name = '机房表'
        verbose_name_plural = verbose_name
        db_table = 'ops_idc'

    def __str__(self):
        return self.idc_name


class Cabinet(models.Model):
    cabinet_number = models.CharField(max_length=10, verbose_name='机柜编号', unique=True)
    cabinet_floor = models.SmallIntegerField(verbose_name='机柜所在楼层', null=True, blank=True)
    cabinet_note = models.CharField(max_length=100, verbose_name='机柜备注', null=True, blank=True)
    idc = models.ForeignKey('IDC', on_delete=models.CASCADE, verbose_name='idc机房')

    class Meta:
        verbose_name = '机柜表'
        verbose_name_plural = verbose_name
        db_table = 'ops_cabinet'

    def __str__(self):
        return self.cabinet_number


class Servers(models.Model):
    type = (
        (0, '物理机'),
        (1, '虚拟机'),
        (2, '云主机')
    )
    # 管理ip已写在asset表中
    asset = models.OneToOneField(to='Assets', on_delete=models.CASCADE, related_name='server')
    server_type = models.SmallIntegerField(verbose_name='服务器类型')
    # 用户名和密码可能要加密存储，长度设置大一些
    username = models.CharField(max_length=100, verbose_name='管理用户')
    password = models.CharField(max_length=100, verbose_name='密码')
    # DecimalField是设置精度的十进制数字,max_digits表示数字的最大位数不能超过6，decimal_places表示小数的最大位数
    port = models.DecimalField(max_digits=6, decimal_places=0, default=22, verbose_name='ssh端口',
                               null=True, blank=True)
    # 宿主机，这是专门针对虚拟机设置的字段
    # host_on_nu = models.CharField(max_length=10, verbose_name='所属宿主机的编号')
    # on_delete的详细设置：https://www.jianshu.com/p/6240ed7dd3ea，NOT_PROVIDED表示删除关联数据，引发错误
    host_on = models.ForeignKey(to='self', on_delete=models.NOT_PROVIDED, blank=True, null=True,
                                related_name='host_on_server', verbose_name='宿主机')
    # 需要采集的服务器信息
    kernel = models.CharField(max_length=30, verbose_name='内核版本')
    system = models.CharField(max_length=30, verbose_name='系统版本')
    cpu_model = models.CharField(max_length=40, verbose_name='CPU型号')
    cpu_counts = models.SmallIntegerField(verbose_name='物理CPU个数')
    vcpu_counts = models.SmallIntegerField(verbose_name='逻辑CPU个数')

    class Meta:
        verbose_name = '服务器表'
        verbose_name_plural = verbose_name
        db_table = 'ops_server'

    def __str__(self):
        return self.asset.asset_flag


class NetworkCard(models.Model):
    status = (
        (0, '关闭'),
        (1, '开启'),
        (2, '故障')
    )
    server = models.ForeignKey('Servers', on_delete=models.CASCADE, related_name='networkCard')
    network_card_status = models.IntegerField(choices=status, default=1, verbose_name='网卡状态')
    network_card_name = models.CharField(max_length=10, verbose_name='网卡名称')
    network_card_ip = models.GenericIPAddressField(verbose_name='ip地址')
    network_card_gateway = models.GenericIPAddressField(verbose_name='网关地址')
    network_card_netmask = models.GenericIPAddressField(verbose_name='子网掩码')
    network_card_dns = models.GenericIPAddressField(verbose_name='DNS')
    network_card_mac = models.CharField(max_length=30, verbose_name='mac地址')

    class Meta:
        verbose_name = '网卡表'
        verbose_name_plural = verbose_name
        db_table = 'ops_network_card'


class Disk(models.Model):
    server = models.ForeignKey(to='Servers', on_delete=models.CASCADE,
                               related_name='disk', verbose_name='所在服务器')
    disk_volume = models.CharField(max_length=20, verbose_name='磁盘容量')
    disk_model = models.CharField(max_length=40, verbose_name='磁盘型号')
    disk_slot = models.CharField(max_length=8, verbose_name='磁盘插槽')
    disk_type = models.CharField(max_length=8, verbose_name='磁盘接口类型')

    class Meta:
        verbose_name = '硬盘表'
        verbose_name_plural = verbose_name
        db_table = 'ops_disk'


class Memory(models.Model):
    server = models.ForeignKey('Servers', on_delete=models.CASCADE,
                               related_name='memory', verbose_name='所在的服务器')
    memory_slot = models.CharField(max_length=10, verbose_name='内存插槽')
    memory_serial = models.CharField(max_length=100, verbose_name='内存序列号')
    memory_volume = models.CharField(max_length=8, verbose_name='内存total容量')
    memory_free = models.CharField(max_length=8, verbose_name='内存剩余量')
    memory_used = models.CharField(max_length=8, verbose_name='内存已使用量')
    memory_shared = models.CharField(max_length=8, verbose_name='内存shared')
    memory_available = models.CharField(max_length=8, verbose_name='可用内存')
    bufferAndCache = models.CharField(max_length=8, verbose_name='buffer/cache')

    class Meta:
        verbose_name = '内存表'
        verbose_name_plural = verbose_name
        db_table = 'ops_memory'


class Mainboard(models.Model):
    server = models.ForeignKey('Servers', on_delete=models.CASCADE,
                               related_name='mainboard', verbose_name='所在的服务器')
    mainboard_sn = models.CharField(max_length=100, verbose_name='主板序列号')
    mainboard_manufacturer = models.CharField(max_length=100, verbose_name='主板厂商')
    mainboard_model = models.CharField(max_length=100, verbose_name='主板型号')

    class Meta:
        verbose_name = '主板信息表'
        verbose_name_plural = verbose_name
        db_table = 'ops_mainboard'


class Security(models.Model):
    type = (
        (0, '防火墙'),
        (1, '网关'),
        (2, '其他')
    )
    security_type = models.SmallIntegerField(verbose_name='安全设备类型')
    asset = models.OneToOneField('Assets', on_delete=models.CASCADE, related_name='security')

    class Meta:
        verbose_name = '安全设备表'
        verbose_name_plural = verbose_name
        db_table = 'ops_security'


class Network(models.Model):
    """网络设备表"""
    type = (
        (0, 'wifi'),
        (1, 'vpn'),
        (2, '路由器'),
        (3, '交换机'),
        (4, '其他')
    )
    network_type = models.SmallIntegerField(choices=type, verbose_name='网络设备类型')
    asset = models.ForeignKey('Assets', on_delete=models.CASCADE, related_name='network_device')
    network_card = models.ForeignKey('NetworkCard', on_delete=models.CASCADE, related_name='network_device')

    class Meta:
        verbose_name = '网络设备表'
        verbose_name_plural = verbose_name
        db_table = 'network_device'


class Business(models.Model):
    # asset = models.ForeignKey(to='assets', on_delete=models.CASCADE, related_name=)
    """
    业务线表，一个资产可以属于多个业务线，一个业务线对应多个资产，属于多对多关系
    """
    name = models.CharField(max_length=20, verbose_name='业务线名称')
    asset = models.ManyToManyField(to='assets', related_name='business')
    business_manager = models.CharField(max_length=20, verbose_name='业务线的负责人')

    class Meta:
        verbose_name = '业务线表'
        verbose_name_plural = verbose_name
        db_table = 'business'


class UserProfile(models.Model):
    """
    用户信息
    """
    type = (
        (0, '普通管理员'),
        (1, '超级管理员')
    )
    name = models.CharField(max_length=20, verbose_name='管理员名字')
    password = models.CharField(max_length=64, verbose_name='登录密码')
    user_type = models.SmallIntegerField(verbose_name='用户类型', choices=type)
    # 一个用户要管理多个业务线的机器，一个业务线需要多个用户管理，是多对多关系
    business = models.ManyToManyField(to='Business', verbose_name='业务线')
    group = models.ManyToManyField(to='UserGroupProfile', verbose_name='所属组')
    phone = models.CharField(max_length=11, verbose_name='联系电话')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserGroupProfile(models.Model):
    """
    用户组信息
    """
    group_name = models.CharField(max_length=10, verbose_name='组名')

    class Meta:
        verbose_name = '用户组表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name
