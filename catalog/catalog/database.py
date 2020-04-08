# from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Session = db.sessionmaker(bind=db.engine)
#
#
# @contextmanager
# def session_scope(expire_on_commit=True):
#     """Database connection context manager."""
#     if not isinstance(expire_on_commit, bool):
#         raise ValueError(
#             f'Expire attr must be bool. Got {type(expire_on_commit)}'
#         )
#
#     session = Session()
#     session.expire_on_commit = expire_on_commit
#     try:
#         yield session
#         session.commit()
#     except:
#         session.rollback()
#         raise
#     finally:
#         session.close()
