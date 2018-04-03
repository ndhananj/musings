#This python file is mean to just create a text based visualization of
# Rubik's cube-like objects

from copy import copy
class CCT_Rotation(object):
    AXES=["x","y","z"]
    ANGLES=[0,90,180,270]

    def __init__(self,axis,angle):
        if(axis in CCT_Rotation.AXES):
            self.axis=CCT_Rotation.AXES.index(axis)
        if(angle in CCT_Rotation.ANGLES):
            self.angle=angle

    def __repr__(self):
        return "rot{0}{1}".format(self.angle,CCT_Rotation.AXES[self.axis])

    def execute(self,ro):
        numTimes=self.angle/CCT_Rotation.ANGLES[1]
        retVal=ro
        for time in range(numTimes):
            retVal=retVal.baseRotation(self.axis)
        return retVal

CCT_ROTATIONS={}
for axis in CCT_Rotation.AXES:
    for angle in CCT_Rotation.ANGLES:
        CCT_ROTATIONS["rot{0}{1}".format(angle,axis)]=CCT_Rotation(axis,angle)

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

    def baseRotation(self,axis):
        return self;

    def rot(self,rotation):
        return rotation.execute(self)


class CCT_Vec(CCT_RotatingObj):
    def __init__(self,x,y,z):
        super(self.__class__,self).__init__()
        self.v=[x,y,z]

    def __copy__(self):
        return CCT_Vec(self.v[0],self.v[1],self.v[2])

    def __repr__(self):
        return "({0},{1},{2})".format(self.v[0],self.v[1],self.v[2])

    def __int__(self):
        return (1+self.v[0])+((1+self.v[1])+(1+self.v[2])*3)*3

    def baseRotation(self,axis):
        v=list(self.v)
        v[(axis+1)%3]=-self.v[(axis+2)%3]
        v[(axis+2)%3]=self.v[(axis+1)%3]
        return CCT_Vec(v[0],v[1],v[2])

class CCT_FaceDir(CCT_RotatingObj):

    def __init__(self,rightVec,upVec,outVec):
        super(self.__class__,self).__init__()
        self.vecs=[rightVec,upVec,outVec]

    def __repr__(self):
        return "({0}\n{1},\n{2})".format(self.vecs[0],self.vecs[1],self.vecs[2])

    def __copy__(self):
        return CCT_FaceDir(self.vecs[0],self.vecs[1],self.vecs[2])

    def baseRotation(self,axis):
        return CCT_FaceDir(
        self.vecs[0].baseRotation(axis),
        self.vecs[1].baseRotation(axis),
        self.vecs[2].baseRotation(axis))

    FACES = ["Front", "Right", "Back", "Left", "Top", "Bottom"]
    ROT_NEEDED = [None, "rot90y", "rot180y", "rot270y", "rot270x", "rot90x"]

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
                retVal = tmp.rot(CCT_ROTATIONS[CCT_FaceDir.ROT_NEEDED[idx]])
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

    def baseRotation(self,axis):
        return self.ro.baseRotation(axis)

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
