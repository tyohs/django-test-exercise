from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='love_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='wow_count',
            field=models.IntegerField(default=0),
        ),
    ]
