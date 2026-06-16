from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class DBUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    isAdmin = Column(Boolean, index=True, default=False)

class DBLibrary(Base):
    __tablename__ = 'library'
    libID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    fileType = Column(String)
    isPublic = Column(Boolean, default=False)  # ← NEW

class DBLibraryCollection(Base):
    __tablename__ = 'libraryCollection'
    libcolID = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    lib_id = Column(Integer, ForeignKey("library.libID"))

class DBMedia(Base):
    __tablename__ = 'media'
    mediaID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    title = Column(String, index=True)
    mimeType = Column(String, index=True)
    mediaURL = Column(String)
    coverURL = Column(String)
    lib_id = Column(Integer, ForeignKey("library.libID"))

class DBCategory(Base):
    __tablename__ = 'category'
    categoryID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

class DBCategoryPerMedia(Base):
    __tablename__ = 'categoryPerMedia'
    categoryPerMediaID = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.categoryID"))
    media_id = Column(Integer, ForeignKey("media.mediaID"))