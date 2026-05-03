from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, related_name='credentials', to=settings.AUTH_USER_MODEL),
        ),
    ]
