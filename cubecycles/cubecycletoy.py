#This python file is mean to just create a text based visualization of
# Rubik's cube-like objects

from copy import copy

class CCT_RotatingObj(object):
    def __init__(self):
        self.intVal=-1

    def __int__(self):
        return self.intVal

    def __mul__(self,other):
        return int(self)*int(other)

    __rmul__ = __mul__

    def __add__(self,other):
        return int(self)+int(other)

    __radd__ = __add__

    def rot90x(self):
        return self

    def rot90y(self):
        return self

    def rot90z(self):
        return self

    def rot180x(self):
        return self.rot90x().rot90x()

    def rot180y(self):
        return self.rot90y().rot90y()

    def rot180z(self):
        return self.rot90z().rot90z()

    def rot270x(self):
        return self.rot180x().rot90x()

    def rot270y(self):
        return self.rot180y().rot90y()

    def rot270z(self):
        return self.rot180z().rot90z()


class CCT_Vec(CCT_RotatingObj):
    def __init__(self,x,y,z):
        super(self.__class__,self).__init__()
        self.x=x
        self.y=y
        self.z=z

    def __copy__(self):
        return CCT_RotatingObj(self.x,self.y,self.z)

    def __repr__(self):
        return "({0},{1},{2})".format(self.x,self.y,self.z)

    def __int__(self):
        return (1+self.x)+((1+self.y)+(1+self.z)*3)*3

    def rot90x(self):
        return CCT_Vec(self.x,-self.z,self.y)

    def rot90y(self):
        return CCT_Vec(self.z,self.y,-self.x)

    def rot90z(self):
        return CCT_Vec(-self.y,self.x,self.z)

class CCT_FaceDir(CCT_RotatingObj):

    def __init__(self,rightVec,upVec,outVec):
        super(self.__class__,self).__init__()
        self.rightVec=rightVec
        self.upVec=upVec
        self.outVec=outVec

    def __repr__(self):
        return "({0}\n{1},\n{2})".format(self.rightVec,self.upVec,self.outVec)

    def __copy__(self):
        return CCT_FaceDir(self.rightVec,self.upVec,self.outVec)

    def rot90x(self):
        return CCT_FaceDir(
        self.rightVec.rot90x(),
        self.upVec.rot90x(),
        self.outVec.rot90x())

    def rot90y(self):
        return CCT_FaceDir(
        self.rightVec.rot90y(),
        self.upVec.rot90y(),
        self.outVec.rot90y())

    def rot90z(self):
        return CCT_FaceDir(
        self.rightVec.rot90z(),
        self.upVec.rot90z(),
        self,outVev.rot90z())

    FACES = ["Front", "Right", "Back", "Left", "Top", "Bottom"]
    ROT_NEEDED = [None, "rot90y", "rot180y", "rot270y", "rot270y", "rot90y"]

    @staticmethod
    def Front():
        retVal= CCT_FaceDir(
        CCT_Vec(1,0,0),
        CCT_Vec(0,1,0),
        CCT_Vec(0,0,1))
        retVal.intVal=CCT_FaceDir.FACES.index("Front")
        return retVal

    @staticmethod
    def makeIdxFace(idx):
        if(idx in range(len(CCT_FaceDir.ROT_NEEDED))):
            tmp = CCT_FaceDir.Front()
            if(None==CCT_FaceDir.ROT_NEEDED[idx]):
                return tmp
            else:
                retVal = getattr(tmp,CCT_FaceDir.ROT_NEEDED[idx])()
                retVal.intVal=idx
                return retVal
        else:
            print "Trying to make unknown face:\n"
            print " pick idx in {0} ".format(range(len(CCT_FaceDir.ROT_NEEDED)))
            print "\n or name in {0}".format(CCT_FaceDir.FACES)
            return None

    @staticmethod
    def makeNamedFace(name):
        try:
            return CCT_FaceDir.makeIdxFace(CCT_FaceDir.FACES.index(name))
        except ValueError as e:
            print "Chose from {0}".format(CCT_FaceDir.FACES)
            raise e


    @staticmethod
    def Bottom():
        retVal=CCT_FaceDir.Front().rot90x()
        retVal.intVal=5
        return retVal

    @staticmethod
    def Right():
        retVal=CCT_FaceDir.Front().rot90y()
        retVal.intVal=1
        return retVal

    @staticmethod
    def Back():
        retVal=CCT_FaceDir.Front().rot180y()
        retVal.intVal=2
        return retVal

    @staticmethod
    def Left():
        retVal=CCT_FaceDir.Front().rot270y()
        retVal.intVal=3
        return retVal

    @staticmethod
    def Top():
        retVal=CCT_FaceDir.Front().rot270x()
        retVal.intVal=4
        return retVal


class CCT_LabeledRotatingObj(CCT_RotatingObj):
    def __init__(self,label,ro):
        super(self.__class__,self).__init__()
        self.intVal=int(ro)
        self.label=label
        self.ro=ro

    def __repr__(self):
        return "{0}:{1}".format(self.label,self.ro)

    def __copy__(self):
        return CCT_LabeledRotatingObj(self.label,self.ro)

    def rot90x(self):
        return self.ro.rot90x()

    def rot90y(self):
        return self.ro.rot90y()

    def rot90z(self):
        return self.ro.rot90z()

    def setLabel(self,label):
        self.label=label

    def getLabel(self):
        return self.label


class CCT_SectionedGrid(CCT_RotatingObj):
    def __init__(self,face,rows,cols):
        super(self.__class__,self).__init__()
        self.intVal=int(face)*rows*cols
        self.grid=[]
        for row in range(rows):
            self.grid.append([])
            for col in range(cols):
                label = self.intVal+row*cols+col
                self.grid[row].append(CCT_LabeledRotatingObj(label,face))

    def __str__(self):
        return str([list(map(lambda(x):x.getLabel(),x)) for x in self.grid])
