# AWS Secure Landing Zone CLI Native

Plantillas CloudFormation JSON de referencia para entornos aislados `dev` y `prod`. El repositorio está **preparado solo localmente**: no se ha desplegado, validado por AWS ni contrastado con una cuenta. No se necesitan ni guardan credenciales para las verificaciones locales.

## Diseño implementado

- VPC de dos AZ con subredes públicas, de aplicación y de datos; un NAT en dev y uno por AZ en prod.
- Repositorio ECR inmutable, escaneo al publicar y política de ciclo de vida.
- Tareas ECS Fargate privadas detrás de un ALB HTTPS; ARN del certificado e imagen inmutable son entradas futuras del operador.
- Aurora PostgreSQL Serverless v2 cifrada, secreto generado en Secrets Manager, clave KMS dedicada con rotación, respaldo de 7 días y lector opcional en prod.
- Plantilla opcional de CloudTrail, Config, GuardDuty y Security Hub a nivel de cuenta; desactivada en ambos entornos.
- Validación local de JSON/contratos, pruebas unitarias y plan informativo de stacks.

No están implementados VPC endpoints, Flow Logs, WAF, CloudFront, DNS, presupuestos, alarmas/SNS de CloudWatch ni compilación de imagen de aplicación. Las propiedades de seguridad describen la intención de las plantillas, no controles ya desplegados. Consulta [arquitectura](docs/ARCHITECTURE.md) y [decisiones de diseño](docs/DESIGN-DECISIONS.md).

## Inicio rápido local

Requiere Python 3.10 o posterior (la evidencia registrada indica Python 3.13.15). No requiere AWS CLI.

```powershell
python scripts/preflight.py --environment dev
python scripts/preflight.py --environment prod
python scripts/plan.py --environment dev
python -m unittest discover -s tests -v
```

Escáneres locales opcionales: instala `cfn-lint` y Checkov según la [guía de instalación y operación](docs/DEPLOYMENT.md); preflight los ejecuta si están disponibles. `--strict-scanners` convierte la ausencia de alguno en error. `plan.py` es informativo y no crea change sets.

Los puntos de entrada `deploy.py`, `verify.py` y `destroy.py` actualmente terminan con `BLOCKED` y nunca invocan AWS. La preparación local no incluye `aws configure`, `aws login`, STS, CloudFormation remoto, comandos AWS remotos ni inspección de credenciales.

## Costos, retención y cleanup

El modelo asume 730 horas al mes. Dev tiene un NAT, una tarea y un escritor Aurora; prod tiene dos NAT, dos tareas, escritor y lector. El costo real depende de precios regionales, bytes NAT, tráfico hacia internet/entre AZ, LCU del ALB, ACU/I/O/almacenamiento/respaldo de Aurora, logs, secretos, solicitudes KMS y almacenamiento de imágenes. Antes de aprobar, genera estimaciones fechadas para dev y prod con AWS Pricing Calculator; las cifras ilustrativas anteriores no son una cotización.

Los logs de aplicación retienen 30 días; backups automáticos Aurora, 7 días. El bucket de auditoría opcional elimina objetos a los 2.555 días (aprox. siete años) y mantiene versionado; revisa requisitos legales, versiones no actuales y retención antes de activarlo. ECR conserva 30 imágenes. Aurora prod tiene protección contra eliminación; el cleanup futuro debe resolver primero retención de backups/evidencia y manejo de esa protección. Consulta la [lista predeploy/postdeploy/cleanup](docs/DEPLOYMENT.md).

## CI e identidad

GitHub Actions ejecuta solo validaciones locales y escáneres IaC con `contents: read`. No hay tarea de despliegue, rol AWS, clave estática ni permiso `id-token: write`. Agrega OIDC solo con política IAM revisada y limitada a repositorio/ref, y aprobación explícita del despliegue.

## Documentación

- [Preparación, límites local/AWS, requisitos, costos y cleanup](docs/DEPLOYMENT.md)
- [Arquitectura](docs/ARCHITECTURE.md) · [fases](docs/PHASES.md) · [decisiones](docs/DESIGN-DECISIONS.md)
- [Estado de evidencia](docs/evidence/local-validation.md)

## Licencia

MIT. Consulta [LICENSE](LICENSE).
