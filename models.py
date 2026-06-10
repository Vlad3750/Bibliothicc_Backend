from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class DBUser(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    isAdmin = Column(Boolean, index=True)

class DBLibrary(Base):
    __tablename__ = 'library'

    libID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class DBLibraryCollection(Base):
    __tablename__ = 'libraryCollection'

    libcolID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    lib_id = Column(Integer, ForeignKey("library.libID"))

class DBFile(Base):
    __tablename__ = 'file'

    fileID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    title = Column(String, index=True)
    mimeType = Column(String, index=True)
    fileURL = Column(String)
    coverURL = Column(String)
    lib_ID = Column(Integer, ForeignKey("library.libID"))

class DBCategory(Base):
    __tablename__ = 'category'

    categoryID = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, index=True)

class DBCategoryPerFile(Base):
    __tablename__ = 'categoryPerFile'

    categoryPerFileID = Column(Integer, primary_key=True, index=True)
    category_ID = Column(Integer, ForeignKey("category.categoryID"))
    file_ID = Column(Integer, ForeignKey("file.fileID"))