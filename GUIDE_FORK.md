# Guía para trabajar with tu fork

## Remotos configurados
- `upstream` = Repositorio original del profesor: `git@github.com:juliangarzon/analitica-datos-estudiantes.git` (solo lectura, push bloqueado)
- `origin`    = Tu fork: `git@github.com:Breinersmartinez/analitica-datos-estudiantes.git` (aquí subes tus cambios)

## 1) Traer actualizaciones del profesor (cada vez que publiquen una clase)
```bash
git checkout main
git fetch upstream
git merge upstream/main  # o git rebase upstream/main
git push origin main
```

## 2) Trabajar in tus actividades
```bash
git checkout main
git pull origin main
git checkout -b claseXX-mis-actividades
# trabaja
git add <archivos>
git commit -m "feat(claseXX): descripción"
git push -u origin claseXX-mis-actividades
```

## 3) Entregar o guardar
Solo sube a `origin`. Nunca hagas `push` hacia `upstream`.

## Reglas de oro
- Trabaja siempre en ramas aparte, nunca directamente en `main`.
- Trae desde `upstream`, sube a `origin`.
- No edites archivos generados por el profesor (se sobrescriben al publicar). Crea tus propios archivos.
- Usa `git status` antes de `git add`.
