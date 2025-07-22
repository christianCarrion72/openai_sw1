# Docker Setup para IA-SW1

Este proyecto incluye configuración Docker optimizada para un despliegue ligero y eficiente.

## Requisitos

- Docker
- Docker Compose
- Archivo `.env` con tu `OPENAI_API_KEY`

## Configuración

1. Asegúrate de tener tu archivo `.env` con la clave de OpenAI:
   ```
   OPENAI_API_KEY=tu_clave_aqui
   ```

## Comandos Docker

### Levantar el proyecto
```bash
docker-compose up --build
```

### Levantar en segundo plano
```bash
docker-compose up -d --build
```

### Ver logs
```bash
docker-compose logs -f
```

### Detener el proyecto
```bash
docker-compose down
```

### Reconstruir la imagen
```bash
docker-compose build --no-cache
```

## Acceso a la aplicación

Una vez levantado, la aplicación estará disponible en:
- **URL**: http://localhost:5000

## Endpoints disponibles

- `POST /query` - Para consultas de texto
- `POST /analyze-image` - Para análisis de imágenes

## Optimizaciones incluidas

- **Imagen base ligera**: Python 3.11-slim
- **Cache de dependencias**: Las dependencias se instalan antes que el código
- **Exclusión de archivos**: .dockerignore optimizado
- **Volúmenes de desarrollo**: Solo código fuente montado
- **Red personalizada**: Para mejor aislamiento

## Troubleshooting

### Si el contenedor no inicia:
1. Verifica que el archivo `.env` existe
2. Revisa los logs: `docker-compose logs`
3. Asegúrate de que el puerto 5000 no esté en uso

### Para desarrollo:
El volumen montado permite cambios en tiempo real en la carpeta `src/`.