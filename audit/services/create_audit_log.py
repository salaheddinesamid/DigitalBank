from ..models import AuditLog


def create_audit_log(
        user,
        action,
        entity,
        entity_id,
        ip_address=None,
        details=None
):
    AuditLog.objects.create(
        user=user,
        entity=entity,
        action=action,
        entity_id=entity_id,
        ip_address=ip_address,
        details=details
    )
