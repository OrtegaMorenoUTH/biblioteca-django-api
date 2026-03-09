import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_project.settings')
django.setup()

from django.contrib.auth.models import User
from libros.models import Autor, Categoria, Libro, Prestamo


def crear_usuario_admin():
    """Crear usuario administrador si no existe"""
    print("\nCreando usuario administrador...")

    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@biblioteca.com',
            'is_staff': True,
            'is_superuser': True
        }
    )

    if created:
        user.set_password('admin123')
        user.save()
        print("  ✓ Usuario admin creado (usuario: admin | contraseña: admin123)")
    else:
        print("  • Usuario admin ya existe")

    return user


def crear_categorias():
    """Crear categorías"""
    print("\nCreando categorías...")

    categorias_data = [
        {'nombre': 'Ficción', 'descripcion': 'Novelas y cuentos de ficción'},
        {'nombre': 'Fantasía', 'descripcion': 'Mundos imaginarios y literatura fantástica'},
        {'nombre': 'Misterio', 'descripcion': 'Suspenso, crimen e investigación'},
        {'nombre': 'Terror', 'descripcion': 'Literatura de horror'},
        {'nombre': 'Historia', 'descripcion': 'Historia y biografías'},
    ]

    for data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nombre=data['nombre'],
            defaults=data
        )
        if created:
            print(f"  ✓ Categoría '{categoria.nombre}' creada")


def crear_autores():
    """Crear autores"""
    print("\nCreando autores...")

    autores_data = [
        {
            'nombre': 'Gabriel',
            'apellido': 'García Márquez',
            'fecha_nacimiento': date(1927, 3, 6),
            'pais_origen': 'Colombia',
            'biografia': 'Premio Nobel de Literatura 1982.'
        },
        {
            'nombre': 'Isabel',
            'apellido': 'Allende',
            'fecha_nacimiento': date(1942, 8, 2),
            'pais_origen': 'Chile',
            'biografia': 'Autora chilena de fama mundial.'
        },
        {
            'nombre': 'Jorge Luis',
            'apellido': 'Borges',
            'fecha_nacimiento': date(1899, 8, 24),
            'pais_origen': 'Argentina',
            'biografia': 'Escritor y poeta argentino.'
        },
        {
            'nombre': 'Octavio',
            'apellido': 'Paz',
            'fecha_nacimiento': date(1914, 3, 31),
            'pais_origen': 'México',
            'biografia': 'Premio Nobel de Literatura 1990.'
        },
        {
            'nombre': 'Mario',
            'apellido': 'Vargas Llosa',
            'fecha_nacimiento': date(1936, 3, 28),
            'pais_origen': 'Perú',
            'biografia': 'Premio Nobel de Literatura 2010.'
        },
    ]

    for data in autores_data:
        autor, created = Autor.objects.get_or_create(
            nombre=data['nombre'],
            apellido=data['apellido'],
            defaults=data
        )
        if created:
            print(f"  ✓ Autor '{autor.nombre_completo}' creado")


def crear_libros(usuario_admin):
    """Crear libros"""
    print("\nCreando libros...")

    ficcion = Categoria.objects.get(nombre='Ficción')

    garcia = Autor.objects.get(apellido='García Márquez')
    allende = Autor.objects.get(apellido='Allende')
    borges = Autor.objects.get(apellido='Borges')
    paz = Autor.objects.get(apellido='Paz')
    vargas = Autor.objects.get(apellido='Vargas Llosa')

    libros_data = [
        {
            'titulo': 'Cien años de soledad',
            'isbn': '9780307474728',
            'autor': garcia,
            'categoria': ficcion,
            'fecha_publicacion': date(1967, 5, 30),
            'paginas': 471,
            'descripcion': 'Obra cumbre del realismo mágico.',
            'stock': 5,
            'precio': Decimal('399.00'),
            'valoracion': Decimal('4.9'),
            'creado_por': usuario_admin
        },
        {
            'titulo': 'El amor en los tiempos del cólera',
            'isbn': '9780307387738',
            'autor': garcia,
            'categoria': ficcion,
            'fecha_publicacion': date(1985, 1, 1),
            'paginas': 368,
            'descripcion': 'Historia de amor a lo largo de décadas.',
            'stock': 3,
            'precio': Decimal('349.00'),
            'valoracion': Decimal('4.7'),
            'creado_por': usuario_admin
        },
        {
            'titulo': 'La casa de los espíritus',
            'isbn': '9788401242281',
            'autor': allende,
            'categoria': ficcion,
            'fecha_publicacion': date(1982, 1, 1),
            'paginas': 433,
            'descripcion': 'Saga familiar con realismo mágico.',
            'stock': 4,
            'precio': Decimal('329.00'),
            'valoracion': Decimal('4.6'),
            'creado_por': usuario_admin
        },
        {
            'titulo': 'Ficciones',
            'isbn': '9780802130303',
            'autor': borges,
            'categoria': ficcion,
            'fecha_publicacion': date(1944, 1, 1),
            'paginas': 174,
            'descripcion': 'Cuentos filosóficos y metafísicos.',
            'stock': 2,
            'precio': Decimal('289.00'),
            'valoracion': Decimal('4.8'),
            'creado_por': usuario_admin
        },
        {
            'titulo': 'El laberinto de la soledad',
            'isbn': '9786071613578',
            'autor': paz,
            'categoria': ficcion,
            'fecha_publicacion': date(1950, 1, 1),
            'paginas': 191,
            'descripcion': 'Ensayo sobre la identidad mexicana.',
            'stock': 2,
            'precio': Decimal('259.00'),
            'valoracion': Decimal('4.5'),
            'creado_por': usuario_admin
        },
    ]

    for data in libros_data:
        libro, created = Libro.objects.get_or_create(
            isbn=data['isbn'],
            defaults=data
        )
        if created:
            print(f"  ✓ Libro '{libro.titulo}' creado")


def crear_prestamos():
    """Crear préstamos de ejemplo"""
    print("\nCreando préstamos...")

    usuario = User.objects.filter(is_superuser=False).first()
    libro = Libro.objects.first()

    if not usuario or not libro:
        print("  ⚠ No hay usuarios o libros suficientes para crear préstamos")
        return

    prestamo, created = Prestamo.objects.get_or_create(
        libro=libro,
        usuario=usuario,
        defaults={
            'fecha_devolucion_esperada': date.today() + timedelta(days=7),
            'estado': Prestamo.ACTIVO,
            'notas': 'Préstamo de prueba'
        }
    )

    if created:
        print(f"  ✓ Préstamo creado para '{libro.titulo}'")


def ejecutar_seed():
    print("\n🚀 INICIANDO CARGA DE DATOS")
    admin = crear_usuario_admin()
    crear_categorias()
    crear_autores()
    crear_libros(admin)
    crear_prestamos()
    print("\n✅ CARGA DE DATOS COMPLETADA\n")


if __name__ == '__main__':
    ejecutar_seed()