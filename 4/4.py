from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///files.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    files = relationship(
        "File",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")

    def __repr__(self):
        return f"<File id={self.id} filename={self.filename}>"


def run_migration():
    Base.metadata.create_all(bind=engine)
    print("Migration successful")


def crud_test():
    db = SessionLocal()

    user = User(username="fatemeh")
    db.add(user)
    db.commit()
    db.refresh(user)

    file1 = File(
        filename="report.pdf",
        path="/uploads/report.pdf",
        owner=user
    )

    db.add(file1)
    db.commit()

    users = db.query(User).all()
    files = db.query(File).all()

    print("Users:", users)
    print("Files:", files)

    file1.filename = "final_report.pdf"
    db.commit()

    updated_file = db.query(File).first()
    print("Updated file:", updated_file)

    db.delete(user)
    db.commit()

    remaining_files = db.query(File).all()
    print("Remaining files:", remaining_files)

    db.close()


if __name__ == "__main__":
    run_migration()
    crud_test()
