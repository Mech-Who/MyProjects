"""
- 我们定义了一个接口来创建对象，但是工厂本身并不负责创建对象，
    是将这一任务交由子类来完成，即子类决定了要实例化哪些类。
- Factory方法的创建是通过继承而不是通过实例化来完成的
- 工厂方法使设计更加具有可定制性。它可以返回相同的实例或子类，
    而不是某种类型的对象（就像在简单工厂方法中的那样）。
"""
from abc import ABCMeta, abstractmethod

class Section(metaclass=ABCMeta):
    @abstractmethod
    def describe(self):
        pass

class PersonalSection(Section):
    def describe(self):
        print("Album Section")

class AlbumSection(Section):
    def describe(self):
        print("Album Section")

class PatentSection(Section):
    def describe(self):
        print("Patent Section")

class PublicationSection(Section):
    def describe(self):
        print("Publication Section")

class Profile(metaclass=ABCMeta):
    def __init__(self):
        self.sections = []
        self.createProfile()
    
    @abstractmethod
    def createProfile(self):
        pass
    def getSections(self):
        return self.sections
    def addSections(self, section):
        self.sections.append(section)
    
class linkedin(Profile):
    def createProfile(self):
        self.addSections(PersonalSection())
        self.addSections(PatentSection())
        self.addSections(AlbumSection())

class facebook(Profile):
    def createProfile(self):
        self.addSections(PersonalSection())
        self.addSections(AlbumSection())

if __name__ == "__main__":
    profile_type = input("Which Profile you'd like to create?[LinkedIn or FaceBook]")
    profile = eval(profile_type.lower())()
    print("Creating Profile..", type(profile).__name__)
    print("Profile has sections --", profile.getSections())
