# let's see what happens
import itertools
import sys

#class declarations
class Student:
    def __init__(self, id, prefs):
        self.id = id
        self.prefs = prefs
        self.coursesAssigned = []

    def __str__(self):
        return str(self.id)# + " " + str(self.prefs[0]) + " " + str(self.prefs[1]) + " " + str(self.prefs[2]) + " " + str(self.prefs[3])

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
        return str(self.id) + "\t" + str(self.room) + "\t" + str(self.teacher) + "\t" + str(self.period) #+ "\t" + str(self.students)

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






if __name__=='__main__':

    try:
        constraintsPath    = sys.argv[1]
        prefsPath          = sys.argv[2]
        scheduleOutputPath = sys.argv[3]

    except IndexError:
        print('\nERROR: Argument missmatch\n'
              '\nCorrect usage is:'
              '\n"python3 registrarGroupProject.py <constraintsPath> <prefsPath> <scheduleOutputPath>"\n')
        exit(1)


    numStudents, numPeriods, numRooms, numCourses, numTeachers = 0,0,0,0,0


    rooms = []
    courses = []

    constraintsFile = open(constraintsPath,"r+")
    numPeriods = int(((constraintsFile.readline()).split())[2])      #This should take the numPeriods from the constraintsFile
    numRooms = int(((constraintsFile.readline()).split())[1])        #This should take the numRooms from the

    # Rooms
    for i in range(0,numRooms):
        ourLine = constraintsFile.readline()
        listOfOurLine = ourLine.split()
        rooms.append(Room(int(listOfOurLine[0]),int(listOfOurLine[1])))
        # print("Thing we just added: ", rooms[i])

    roomLookup = {r.id:r for r in rooms}

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

    courseLookup = {c.id:c for c in courses}

    # Students
    prefsFile = open(prefsPath,"r+")
    numStudents = int(((prefsFile.readline()).split())[1])      #This should take the numStudents from the prefsFile

    students = []

    for i in range(0,numStudents):
        ourLine = prefsFile.readline()
        listOfOurLine = ourLine.split()
        students.append(Student(int(listOfOurLine[0]), list(map(int, listOfOurLine[1:5]))))



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

    #preprocessing - sort Rooms in order of decreasing capacity

    rooms.sort(key = lambda r: -r.capacity)
    # print(rooms)

    periods = [Period(i) for i in range(1, numPeriods + 1)]

    #main algorithm

    #assign each class in classes to a time slot

    nonFull = periods.copy()

    for course in courses:
        cost = {} #dictionary of costs of assigning course to each period
        for period in nonFull:
            cost[period.id] = sum([conflicts[course.id, c.id] for c in period.courses])
        #the above could have been one line, but readability
        if len(nonFull) == 0:
            break
        elif len(nonFull) == 1:
            nonFull[0].courses += [course]
            course.period = nonFull[0].id
            if len(nonFull[0].courses) >= numRooms:
                nonFull.remove(nonFull[0])
            continue

        # NOTE: Replace the following 5 lines with a call to sort periods by increasing cost. Then, in the lines after, we can just iterate through periods like in the pseudocode
        first = min(nonFull[0], nonFull[1], key = lambda p: cost[p.id])         #first is the lowest cost period that we could add course to
        second = max(nonFull[0], nonFull[1], key = lambda p: cost[p.id])        #first is the lowest cost period that we could add course to
        for period in nonFull[2:]:
            second = first if cost[period.id] < cost[first.id] else (period if cost[period.id] < cost[second.id] else second)
            first = period if cost[period.id] < cost[first.id] else first

        # NOTE: This loop currently does not check to make sure that there is an available room before assigning course to the time's course list. Also, why arent we iterating through the list of periods in increasing order of cost, instead of just doing "first" and "second"
        for c in first.courses:
            if course.teacher == c.teacher:
                second.courses += [course]
                course.period = second.id
                if len(second.courses) >= numRooms:
                    nonFull.remove(second)
                break
        else:
            first.courses += [course]
            course.period = first.id
            if len(first.courses) >= numRooms:
                nonFull.remove(first)

    # for p in periods:
    #     print(p.courses)

    # For each time slot T
    #     let C' be the list of courses assigned to T
    #         For each i in range (1,numClasses)
    #             Assign course ci from C' to room ri
    for period in periods:
        bigC = period.courses       #The list of classes in the period
        print(bigC)
        for i in range(len(bigC)):
            room = rooms[i].id
            course = courseLookup[bigC[i].id]
            course.room = room

    # print(periods)


    # For each student s in S:
    #     For each course c in s's course list:
    #         Let r and t be the room and time to which c is assigned
    #         If the number of students assigned to c is less than r capacity and s is not already assigned to another course in t:
    #             Assign s to c (both ways)
    # print(students)
    for student in students:
        busyPeriods = []
        for course in map(lambda p: courseLookup[p], student.prefs):
            room = roomLookup[course.room] # room of c
            period = course.period # period of c
            # print("line 186!!!!")
            if ((len(course.students) < room.capacity) and (not (period in busyPeriods))):
                # print("in the if line 190!!!")
                course.students.append(student)         # for Course object
                student.coursesAssigned.append(course)  # for Student object
                busyPeriods.append(course.period)

    # for s in students:
    for c in courses:
        print(c.students)

    #That could be all!
    # What do we write to the output file?
    with open(scheduleOutputPath, 'w') as outputFile:
        outputFile.write("Course\tRoom\tTeacher\tTime\tStudents\n")
        for course in courses:
            outputFile.write(str(course) + "\t")
            outputFile.write(' '.join(map(lambda s: str(s.id), course.students)) + "\n")
            # for studentID in course.students:
            #     outputFile.write(studentID + " ")
