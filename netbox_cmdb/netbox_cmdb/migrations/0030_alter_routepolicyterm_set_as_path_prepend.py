# Generated by Django 4.0.8 on 2023-05-05 12:23

from django.db import migrations, models


def calculateNbPrepend(apps, schema):
    Policy = apps.get_model("netbox_cmdb", "RoutePolicyTerm")
    ASN = apps.get_model("netbox_cmdb", "ASN")

    for p in Policy.objects.all():
        if p.set_as_path_prepend:
            prepend_path = p.set_as_path_prepend.split(" ")
            asn = ASN.objects.get(number=prepend_path[0])
            if not asn:
                asn = ASN.objects.create(number=prepend_path[0], organization_name="internal")

            p.set_as_path_prepend_repeat = len(prepend_path)
            p.set_as_path_prepend_asn = asn
            p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_cmdb', '0029_vrf'),
    ]

    operations = [
        migrations.AddField(
            model_name='routepolicyterm',
            name='set_as_path_prepend_repeat',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='routepolicyterm',
            name='set_as_path_prepend_asn',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.PROTECT, related_name='%(class)slocal_asn', to='netbox_cmdb.asn'),
        ),
        migrations.RunPython(calculateNbPrepend),
        migrations.RemoveField(
            model_name='routepolicyterm',
            name='set_as_path_prepend',
        ),
    ]