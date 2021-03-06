# Generated by Django 3.0.2 on 2020-03-11 23:53

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(help_text='填写用户名', max_length=32, unique=True, verbose_name='用户账号')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='名称s')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '广告位置表',
                'verbose_name_plural': '广告位置表',
            },
        ),
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='客户名称')),
                ('agent', models.CharField(blank=True, max_length=32, null=True, verbose_name='代理商')),
                ('sort', models.SmallIntegerField(choices=[(0, '直客'), (1, '代客')], default=0, verbose_name='客户类型')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '客户表',
                'verbose_name_plural': '客户表',
            },
        ),
        migrations.CreateModel(
            name='ChargeSort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=32, null=True, verbose_name='名称')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '计费类型表',
                'verbose_name_plural': '计费类型表',
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='媒体名称')),
                ('agent', models.CharField(blank=True, max_length=32, null=True, verbose_name='代理商')),
                ('sort', models.SmallIntegerField(choices=[(0, '直媒'), (1, '代媒')], default=0, verbose_name='媒体类型')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '媒体表',
                'verbose_name_plural': '媒体表',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('launch_date', models.DateTimeField(blank=True, null=True, verbose_name='投放日期')),
                ('ad_url', models.CharField(blank=True, max_length=1024, null=True, verbose_name='广告链接')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('status', models.SmallIntegerField(choices=[(0, '未执行'), (1, '执行中'), (2, '已完成')], default=0, verbose_name='状态')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('a_charge_sort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ad_sort2plan', to='tgsAdmin.ChargeSort', verbose_name='广告计费类型')),
                ('advertiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgsAdmin.Advertiser', verbose_name='客户')),
                ('m_charge_sort', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m_sort2plan', to='tgsAdmin.ChargeSort', verbose_name='媒体计费类型')),
                ('m_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tgsAdmin.AdLocation', verbose_name='位置')),
            ],
            options={
                'verbose_name': '计划表',
                'verbose_name_plural': '计划表',
            },
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=32, null=True, verbose_name='名称')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '广告端口表',
                'verbose_name_plural': '广告端口表',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
        ),
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_unit_price', models.FloatField(blank=True, null=True, verbose_name='媒体广告位单价')),
                ('a_unit_price', models.FloatField(blank=True, null=True, verbose_name='广告单价')),
                ('plan_launch_count', models.BigIntegerField(blank=True, null=True, verbose_name='预计投放量')),
                ('budget', models.BigIntegerField(blank=True, null=True, verbose_name='预计成本')),
                ('m_exposure_count', models.BigIntegerField(blank=True, null=True, verbose_name='媒体-曝光量')),
                ('m_click_count', models.BigIntegerField(blank=True, null=True, verbose_name='媒体-点击量')),
                ('m_click_rate', models.FloatField(blank=True, null=True, verbose_name='媒体-点击率')),
                ('m_settlement_count', models.BigIntegerField(blank=True, null=True, verbose_name='媒体-结算数')),
                ('m_statement_status', models.SmallIntegerField(choices=[(0, '未对账'), (1, '已对账')], default=0, verbose_name='媒体对账状态')),
                ('m_checkout_time', models.DateTimeField(blank=True, null=True, verbose_name='媒体对账时间')),
                ('a_exposure_count', models.BigIntegerField(blank=True, null=True, verbose_name='客户-曝光量')),
                ('a_click_count', models.BigIntegerField(blank=True, null=True, verbose_name='客户-点击量')),
                ('a_click_rate', models.FloatField(blank=True, null=True, verbose_name='客户-点击率')),
                ('a_week_rate', models.FloatField(blank=True, null=True, verbose_name='客户-七日唤醒率')),
                ('a_settlement_count', models.BigIntegerField(blank=True, null=True, verbose_name='客户-结算数')),
                ('a_statement_status', models.SmallIntegerField(choices=[(0, '未对账'), (1, '已对账')], default=0, verbose_name='客户对账状态')),
                ('a_checkout_time', models.DateTimeField(blank=True, null=True, verbose_name='客户对账时间')),
                ('cost', models.FloatField(blank=True, null=True, verbose_name='实际成本')),
                ('income', models.FloatField(blank=True, null=True, verbose_name='收入')),
                ('profit', models.FloatField(blank=True, null=True, verbose_name='利润')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('plan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tgsAdmin.Plan', verbose_name='计划')),
            ],
            options={
                'verbose_name': '结算表',
                'verbose_name_plural': '结算表',
            },
        ),
        migrations.AddField(
            model_name='plan',
            name='m_port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tgsAdmin.Port', verbose_name='端口'),
        ),
        migrations.AddField(
            model_name='plan',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgsAdmin.Media', verbose_name='媒体'),
        ),
        migrations.CreateModel(
            name='MediaStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='截至时间')),
                ('cost', models.FloatField(verbose_name='成本')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgsAdmin.Media', verbose_name='媒体')),
            ],
            options={
                'verbose_name': '媒体对账表',
                'verbose_name_plural': '媒体对账表',
            },
        ),
        migrations.CreateModel(
            name='AdvertStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='截至时间')),
                ('income', models.FloatField(verbose_name='收入')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('advertiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgsAdmin.Advertiser', verbose_name='广告')),
            ],
            options={
                'verbose_name': '客户对账表',
                'verbose_name_plural': '客户对账表',
            },
        ),
    ]
