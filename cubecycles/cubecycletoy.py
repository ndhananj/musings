#This python file is mean to just create a text based visualization of
# Rubik's cube-like objects

from copy import copy
class Operation(object):
    def __init__(self):
        pass
    def execute(self,obj):
        pass

class Rotation(Operation):
    AXES=["x","y","z"]
    ANGLES=[0,90,180,270]

    def __init__(self,axis,angle):
        if(axis in Rotation.AXES):
            self.axis=Rotation.AXES.index(axis)
        if(angle in Rotation.ANGLES):
            self.angle=angle

    def __repr__(self):
        return "rot{0}{1}".format(self.angle,Rotation.AXES[self.axis])

    def execute(self,ro):
        numTimes=self.angle/Rotation.ANGLES[1]
        retVal=ro
        for time in range(numTimes):
            retVal=retVal.baseRotation(self.axis)
        return retVal

ROTATIONS={}
for axis in Rotation.AXES:
    for angle in Rotation.ANGLES:
        ROTATIONS["rot{0}{1}".format(angle,axis)]=Rotation(axis,angle)

class RotatingObj(object):
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

    def baseRotation(self,axis):
        return self;

    def rot(self,rotation):
        return rotation.execute(self)


class Vec(RotatingObj):
    def __init__(self,x,y,z):
        super(self.__class__,self).__init__()
        self.v=[x,y,z]

    def __copy__(self):
        return Vec(self.v[0],self.v[1],self.v[2])

    def __repr__(self):
        return "({0},{1},{2})".format(self.v[0],self.v[1],self.v[2])

    def __int__(self):
        return (1+self.v[0])+((1+self.v[1])+(1+self.v[2])*3)*3

    def baseRotation(self,axis):
        v=list(self.v)
        v[(axis+1)%3]=-self.v[(axis+2)%3]
        v[(axis+2)%3]=self.v[(axis+1)%3]
        return Vec(v[0],v[1],v[2])

class FaceDir(RotatingObj):

    def __init__(self,rightVec,upVec,outVec):
        super(self.__class__,self).__init__()
        self.vecs=[rightVec,upVec,outVec]

    def __repr__(self):
        return "({0}\n{1},\n{2})".format(self.vecs[0],self.vecs[1],self.vecs[2])

    def __copy__(self):
        return FaceDir(self.vecs[0],self.vecs[1],self.vecs[2])

    def baseRotation(self,axis):
        return FaceDir(
        self.vecs[0].baseRotation(axis),
        self.vecs[1].baseRotation(axis),
        self.vecs[2].baseRotation(axis))

    FACES = ["Front", "Right", "Back", "Left", "Top", "Bottom"]
    ROT_NEEDED = [None, "rot90y", "rot180y", "rot270y", "rot270x", "rot90x"]

    @staticmethod
    def Front():
        retVal= FaceDir(
        Vec(1,0,0),
        Vec(0,1,0),
        Vec(0,0,1))
        retVal.intVal=FaceDir.FACES.index("Front")
        return retVal

    @staticmethod
    def makeIdxFace(idx):
        if(idx in range(len(FaceDir.ROT_NEEDED))):
            tmp = FaceDir.Front()
            if(None==FaceDir.ROT_NEEDED[idx]):
                return tmp
            else:
                retVal = tmp.rot(ROTATIONS[FaceDir.ROT_NEEDED[idx]])
                retVal.intVal=idx
                return retVal
        else:
            print "Trying to make unknown face:\n"
            print " pick idx in {0} ".format(range(len(FaceDir.ROT_NEEDED)))
            print "\n or name in {0}".format(FaceDir.FACES)
            return None

    @staticmethod
    def makeNamedFace(name):
        try:
            return FaceDir.makeIdxFace(FaceDir.FACES.index(name))
        except ValueError as e:
            print "Chose from {0}".format(FaceDir.FACES)
            raise e

FACES={}
for face in FaceDir.FACES:
    FACES[face]=FaceDir.makeNamedFace(face)

class LabeledRotatingObj(RotatingObj):
    def __init__(self,label,ro):
        super(self.__class__,self).__init__()
        self.intVal=int(ro)
        self.label=label
        self.ro=ro

    def __repr__(self):
        return "{0}:{1}".format(self.label,self.ro)

    def __copy__(self):
        return LabeledRotatingObj(self.label,self.ro)

    def baseRotation(self,axis):
        return self.ro.baseRotation(axis)

    def setLabel(self,label):
        self.label=label

    def getLabel(self):
        return self.label


class SectionedGrid(RotatingObj):
    def __init__(self,face,rows,cols):
        super(self.__class__,self).__init__()
        self.intVal=int(face)*rows*cols
        self.face=FACES
        self.rows=rows
        self.cols=cols
        self.grid=[]
        for row in range(rows):
            self.grid.append([])
            for col in range(cols):
                label = self.intVal+row*cols+col
                self.grid[row].append(LabeledRotatingObj(label,face))

    def __repr__(self):
        return str(self.grid)

    def __str__(self):
        return str([list(map(lambda(x):x.getLabel(),x)) for x in self.grid])

    def baseRotation(self,axis):
        return SectionedGrid(self.face.baseRotation(),self.rows,self.cols)

class FaceSectionedCube(RotatingObj):
    def __init__(self,dim):
        super(self.__class__,self).__init__()
        self.faces={k: SectionedGrid(v,dim,dim) for k,v in FACES.items()}

    def __repr__(self):
        return str(self.faces)
