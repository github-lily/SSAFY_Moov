

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_profile_img_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
