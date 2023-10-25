def test():
    from scriptorium.database import get_db
    from scriptorium.users import service as users_service

    db = next(get_db())
    users_service.get_all_users(db)
    assert 1 == 1
