from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from decimal import Decimal


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    nombre = models.CharField(max_length=100)     # ⬅ REDUCIDO
    apellido = models.CharField(max_length=100)   # ⬅ REDUCIDO
    fecha_nacimiento = models.DateField(null=True, blank=True)
    pais_origen = models.CharField(max_length=100, blank=True)
    biografia = models.TextField(blank=True)
    foto = models.URLField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre']
        unique_together = ('nombre', 'apellido')  # ✔ seguro ahora

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Libro(models.Model):

    DISPONIBLE = 'disponible'
    PRESTADO = 'prestado'
    MANTENIMIENTO = 'mantenimiento'
    PERDIDO = 'perdido'

    ESTADOS = [
        (DISPONIBLE, 'Disponible'),
        (PRESTADO, 'Prestado'),
        (MANTENIMIENTO, 'En Mantenimiento'),
        (PERDIDO, 'Perdido'),
    ]

    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255, blank=True)

    # unique ya crea índice → NO duplicamos
    isbn = models.CharField(max_length=13, unique=True)

    autor = models.ForeignKey(
        Autor,
        on_delete=models.PROTECT,
        related_name='libros'
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='libros'
    )

    editorial = models.CharField(max_length=200, blank=True)
    fecha_publicacion = models.DateField(null=True, blank=True)

    paginas = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )

    idioma = models.CharField(max_length=50, default='Español')
    descripcion = models.TextField(blank=True)
    imagen_portada = models.URLField(blank=True)

    stock = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)]
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=DISPONIBLE
    )

    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    valoracion = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[
            MinValueValidator(Decimal('0.00')),
            MaxValueValidator(Decimal('5.00'))
        ]
    )

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='libros_creados'
    )

    class Meta:
        verbose_name_plural = "Libros"
        ordering = ['-fecha_creacion']
        # ⛔ SIN ÍNDICES MANUALES (MySQL safe)

    def __str__(self):
        return f"{self.titulo} - {self.autor.nombre_completo}"

    @property
    def esta_disponible(self):
        return self.estado == self.DISPONIBLE and self.stock > 0


class Prestamo(models.Model):

    ACTIVO = 'activo'
    DEVUELTO = 'devuelto'
    ATRASADO = 'atrasado'
    PERDIDO = 'perdido'

    ESTADOS = [
        (ACTIVO, 'Activo'),
        (DEVUELTO, 'Devuelto'),
        (ATRASADO, 'Atrasado'),
        (PERDIDO, 'Perdido'),
    ]

    libro = models.ForeignKey(
        Libro,
        on_delete=models.PROTECT,
        related_name='prestamos'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='prestamos'
    )

    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ACTIVO
    )

    notas = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_prestamo']

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"