import pytest
from accounts.models import User, UserManager
from units.models import Unite

@pytest.mark.django_db
def test_user_create_agent_requires_unite():
    u = Unite.objects.create(nom="U1", type="cp")
    user = User(username="joe", role=User.ROLE_AGENT, unite=u)
    user.set_password("pass")
    user.save()
    assert user.unite == u

@pytest.mark.django_db
def test_superuser_has_admin_role():
    su = User.objects.create_superuser("admin", "a@b.com", "pass")
    assert su.role == User.ROLE_ADMIN
    assert su.is_staff and su.is_superuser
