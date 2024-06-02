# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Calificaciones(models.Model):
    id_pedido = models.OneToOneField('Pedidos', models.DO_NOTHING, db_column='id_pedido', primary_key=True)
    cal_cliente = models.IntegerField(blank=True, null=True)
    cal_despachador = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calificaciones'


class Clientes(models.Model):
    nombre = models.CharField(max_length=30)
    email = models.CharField(unique=True, max_length=45)
    clave = models.CharField(max_length=100)
    fono = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'clientes'


class Comunas(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    provincia = models.CharField(max_length=30, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comunas'


class Deliverys(models.Model):
    nombre = models.CharField(unique=True, max_length=30)
    vigencia = models.BooleanField()
    fono = models.CharField(unique=True, max_length=12)
    tiempo_despacho = models.IntegerField()
    precio_unitario = models.IntegerField(blank=True, null=True)
    precio_mensual = models.IntegerField(blank=True, null=True)
    precio_anual = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deliverys'


class Despachadores(models.Model):
    nombre = models.CharField(max_length=30)
    fono = models.CharField(unique=True, max_length=12)

    class Meta:
        managed = False
        db_table = 'despachadores'


class Direcciones(models.Model):
    direccion = models.TextField(unique=True)
    cut_comuna = models.ForeignKey(Comunas, models.DO_NOTHING, db_column='cut_comuna', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direcciones'


class DireccionesClientes(models.Model):
    id_direccion = models.OneToOneField(Direcciones, models.DO_NOTHING, db_column='id_direccion', primary_key=True)  # The composite primary key (id_direccion, id_cliente) found, that is not supported. The first column is selected.
    id_cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'direcciones_clientes'
        unique_together = (('id_direccion', 'id_cliente'),)


class Pedidos(models.Model):
    id = models.IntegerField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    id_delivery = models.ForeignKey(Deliverys, models.DO_NOTHING, db_column='id_delivery', blank=True, null=True)
    id_despachador = models.ForeignKey(Despachadores, models.DO_NOTHING, db_column='id_despachador', blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField(blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos'


class PedidosPlatos(models.Model):
    id_pedido = models.OneToOneField(Pedidos, models.DO_NOTHING, db_column='id_pedido', primary_key=True)  # The composite primary key (id_pedido, id_plato) found, that is not supported. The first column is selected.
    id_plato = models.ForeignKey('PlatosRestaurantes', models.DO_NOTHING, db_column='id_plato')
    id_sucursal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos_platos'
        unique_together = (('id_pedido', 'id_plato'),)


class Platos(models.Model):
    nombre = models.CharField(unique=True, max_length=40)
    descripcion = models.TextField(blank=True, null=True)
    estilo = models.CharField(max_length=30)
    restriccion = models.CharField(max_length=30, blank=True, null=True)
    ingredientes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'platos'


class PlatosRestaurantes(models.Model):
    id = models.IntegerField(primary_key=True)
    id_plato = models.ForeignKey(Platos, models.DO_NOTHING, db_column='id_plato', blank=True, null=True)
    id_restaurante = models.ForeignKey('Restaurantes', models.DO_NOTHING, db_column='id_restaurante', blank=True, null=True)
    disponibilidad = models.BooleanField()
    porciones = models.IntegerField(blank=True, null=True)
    precio = models.IntegerField()
    tiempo_prep = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'platos_restaurantes'


class Restaurantes(models.Model):
    nombre = models.CharField(unique=True, max_length=30)
    vigencia = models.BooleanField()
    estilo = models.CharField(max_length=30)
    repartoming = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurantes'


class Sucursales(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    id_restaurante = models.ForeignKey(Restaurantes, models.DO_NOTHING, db_column='id_restaurante')
    sucursal = models.CharField(max_length=30)
    direccion = models.TextField()  # The composite primary key (direccion, id_restaurante) found, that is not supported. The first column is selected.
    fono = models.CharField(max_length=12)
    id_comuna = models.ForeignKey(Comunas, models.DO_NOTHING, db_column='id_comuna', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sucursales'
        unique_together = (('direccion', 'id_restaurante'),)


class SucursalesComunas(models.Model):
    id_sucursal = models.OneToOneField(Sucursales, models.DO_NOTHING, db_column='id_sucursal', primary_key=True)  # The composite primary key (id_sucursal, id_comuna) found, that is not supported. The first column is selected.
    id_comuna = models.ForeignKey(Comunas, models.DO_NOTHING, db_column='id_comuna')

    class Meta:
        managed = False
        db_table = 'sucursales_comunas'
        unique_together = (('id_sucursal', 'id_comuna'),)


class Suscripciones(models.Model):
    id = models.AutoField(primary_key=True)
    id_cliente = models.OneToOneField(Clientes, models.DO_NOTHING, db_column='id_cliente')  # The composite primary key (id_cliente, id_delivery) found, that is not supported. The first column is selected.
    id_delivery = models.ForeignKey(Deliverys, models.DO_NOTHING, db_column='id_delivery')
    ultimo_pago = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    ciclo = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suscripciones'
        unique_together = (('id_cliente', 'id_delivery'),)
