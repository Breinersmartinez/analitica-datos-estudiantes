# Guía para trabajar con tu fork

## Remotos configurados
- `upstream` = Repositorio original del profesor: `git@github.com:juliangarzon/analitica-datos-estudiantes.git` (solo lectura / sin push)
- `origin`    = Tu fork: `git@github.com:Breinersmartinez/analitica-datos-estudiantes.git` (aquí subes tus cambios)

## 1) Traer actualizaciones del profesor (cada vez que publiquen una clase)
```bash
git checkout main
git fetch upstream
git merge upstream/main  # o git rebate upstream/main
git push origin main
```

## 2) Trabajar en tus actividades
```bash
git checkout main
git pull origin main
git checkout -b claseXX-mis-actividades
# trabaja...
git add <archivos>
git commit --m "feat(claseXX): descripción"
git push -u origin claseXX-mis-actividades
``

## 3) Entregar o guardar
Solo sube a `origin`. Nunca hages `push` hacia `upstream`.

## Reglas de oro
- Trabaja siempre en ramas aparte, nunca directamente en `main`.
- Traer desde `upstream`, subir en `origin`.
- No editar archivos gener
### EOF
