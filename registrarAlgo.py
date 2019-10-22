# let's see what happens
import itertools

#class declarations
class Student:
    def __init__(self, id, prefs):
        self.id = id
        self.prefs = prefs
        self.cousesAssigned = []

    def __str__(self):
        return str(self.id) + " " + str(self.prefs[0]) + " " + str(self.prefs[1]) + " " + str(self.prefs[2]) + " " + str(self.prefs[3])

    def __repr__(self):
        return str(self)

class Room:
    """These objects represent each room. It's field is the capacity of the room"""

    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

    def __str__(self):
        return str(self.id) + " " + str(self.capacity)
        # return "Room id: " + self.id + " , capacity: " + self.capacity

    def __repr__(self):
        return str(self)

class Course:
    def __init__(self, id, teacher):
        self.id = id
        self.teacher = teacher
        self.students = []
        self.period = 0
        self.room = 0

    def __str__(self):
        return str(self.id) + " " + str(self.teacher) + " " + str(self.students)

    def __repr__(self):
        return str(self)

class Period:
    """A period is a list of the classes in that period."""

    def __init__(self, id):
        self.id = id
        self.courses = []

    def __str__(self):
        return str(self.id) + " " + str(self.courses)

    def __repr__(self):
        return str(self)

numStudents, numPeriods, numRooms, numCourses, numTeachers = 0,0,0,0,0


rooms = []
courses = []

constraintsFile = open("demo_constraints.txt","r+")
numPeriods = int(((constraintsFile.readline()).split())[2])      #This should take the numPeriods from the constraintsFile
numRooms = int(((constraintsFile.readline()).split())[1])        #This should take the numRooms from the

# Rooms
for i in range(0,numRooms):
    ourLine = constraintsFile.readline()
    listOfOurLine = ourLine.split()
    rooms.append(Room(int(listOfOurLine[0]),int(listOfOurLine[1])))
    # print("Thing we just added: ", rooms[i])


# print(numRooms)
# print(rooms)

numCourses = int(((constraintsFile.readline()).split())[1])
numTeachers = int(((constraintsFile.readline()).split())[1])

# print("your numCourses: ", numCourses)
# print("your numTeachers: ", numTeachers)

# Courses
for i in range(0,numCourses):
    ourLine = constraintsFile.readline()
    listOfOurLine = ourLine.split()
    courses.append(Course(int(listOfOurLine[0]),int(listOfOurLine[1])))       #adds the course wiht id and teacher


# Students
prefsFile = open("demo_studentprefs.txt","r+")
numStudents = int(((prefsFile.readline()).split())[1])      #This should take the numStudents from the prefsFile

students = []

for i in range(0,numStudents):
    ourLine = prefsFile.readline()
    listOfOurLine = ourLine.split()
    students.append(Student(int(listOfOurLine[0]), map(int, listOfOurLine[1:5])))


#preprocessing - create conflict matrix

conflicts = {}
#keys are comma separated, no parenthesis pairs
#main diagonal is popularity of each class
for pair in itertools.product(range(1, numCourses + 1), repeat = 2):
    conflicts[pair] = 0

for stu in students:
    for pair in itertools.product(stu.prefs, repeat = 2):
        conflicts[pair] += 1

# print(conflicts)

#preprocessing - sort list of classes by popularity score

courses.sort(key = lambda c: -conflicts[c.id, c.id])
print(courses)


#preprocessing - sort Rooms in order of decreasing capacity

rooms.sort(key = lambda r: -r.capacity)
# print(rooms)

periods = [Period(i) for i in range(1, numPeriods + 1)]

#main algorithm

#assign each class in classes to a time slot

for course in courses:
    cost = {} #dictionary of costs of assigning course to each period
    for period in periods:
        cost[period.id] = sum([conflicts[course.id, c.id] for c in period.courses])
    #the above could have been one line, but readability
    first = min(periods[0], periods[1], key = lambda p: cost[p.id])         #first is the lowest cost period that we could add course to
    second = max(periods[0], periods[1], key = lambda p: cost[p.id])        #first is the lowest cost period that we could add course to
    for period in periods[2:]:
        second = first if cost[period.id] < cost[first.id] else (period if cost[period.id] < cost[second.id] else second)
        first = period if cost[period.id] < cost[first.id] else first

    for c in first.courses:
        if course.teacher == c.teacher:
            second.courses += [course]
            course.period = second.id
            break
    else:
        first.courses += [course]
        course.period = first.id

for p in periods:
    print(p.courses)


"""good"""
#For each time slot T
    #let C' be the list of courses assigned to T
        #For each i in range (1,numClasses)
            #Assign course ci from C' to room ri
for period in periods:
    bigC = period.courses       #The list of classes in the period
    for i in range(1,len(bigC)):
        (courses[bigC[i].id]).room = (rooms[i]).id

print(periods)
"""end good"""


#For each student s in S:
    #For each course c in s's course list:
        #Let r and t be the room and time to which c is assigned
        #If the number of students assigned to c is less than r capacity and s is not already assigned to another course in t:
            #Assign s to c (both ways)

for student in students:
    for course in student.prefs:
        room = course.room # room of c
        period = course.period # period of c
        busyPeriods = []
        for c in student.coursesAssigned:
            busyPeriods.append(c.period)
        if ((len(course.students) < room.capacity) and (not (period in busyPeriods))):
            course.students.append(student)
            student.coursesAssigned.append(course)


#That could be all!
#What do we write to the output file?
