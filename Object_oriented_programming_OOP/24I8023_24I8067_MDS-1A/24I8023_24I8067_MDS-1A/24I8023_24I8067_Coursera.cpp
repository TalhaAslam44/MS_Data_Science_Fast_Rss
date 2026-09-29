#include "24I8023_24I8067_Coursera.h"
#include <vector>
#include <map>
#include <set>
#include <iostream>
#include <algorithm>

using namespace std;

// Abstract class Person
Person::Person(const long& id, const string& name, const string& email)
    : id(id), name(name), email(email) {}

void Person::setId(long id) { this->id = id; }
void Person::setName(string name) { this->name = name; }
void Person::setEmail(string email) { this->email = email; }

long Person::getId() const { return id; }
string Person::getName() const { return name; }
string Person::getEmail() const { return email; }

// Group class methods
map<int, vector<Student*>> Group::groups;

Group:: Group(int groupID, const std::string& groupName) {
        this->groupID = groupID;
        this->groupName = groupName;
    }

void Group::addMemberToGroup(int groupID, Student* student) {
    groups[groupID].push_back(student);
    cout << "Student " << student->getName() << " added to Group " << groupID << ".\n";
}

void Group::removeMemberFromGroup(int groupID, Student* student) {
    if (groups.find(groupID) != groups.end()) {
        auto& members = groups[groupID];
        members.erase(remove(members.begin(), members.end(), student), members.end());
        cout << "Student " << student->getName() << " removed from Group " << groupID << ".\n";
    } else {
        cout << "Group " << groupID << " does not exist.\n";
    }
}

void Group::displayGroupMembers(int groupID) {
    if (groups.find(groupID) != groups.end()) {
        cout << "Members of Group " << groupID << ":\n";
        for (const auto& member : groups[groupID]) {
            cout << "- " << member->getName() << "\n";
        }
    } else {
        cout << "Group " << groupID << " does not exist.\n";
    }
}

void Group::initiateDiscussion(int groupID, const string& topic) {
    if (groups.find(groupID) != groups.end()) {
        cout << "Group " << groupID << " is discussing: " << topic << "\n";
    } else {
        cout << "Group " << groupID << " does not exist.\n";
    }
}

ostream& operator<<(ostream& out, const Group& group) {
    out << "Group ID: " << group.groupID << "\n"
        << "Group Name: " << group.groupName;
    return out;
}

istream& operator>>(istream& in, Group& group) {
    cout << "Enter Group ID: ";
    in >> group.groupID;
    in.ignore();
    cout << "Enter Group Name: ";
    getline(in, group.groupName);
    return in;
}

// Student class methods
Student::Student(const long& id, const string& name, const string& email,
                 const long& studentId, const string& enrollmentDate)
    : Person(id, name, email), studentId(studentId), enrollmentDate(enrollmentDate), group(nullptr) {}

void Student::addCompletedCourse(const std::string& course) {
    completedCourses.push_back(course);
}

void Student::enrollInCourse(const string& course) {
    cout << name << " has enrolled in " << course << " course." << endl;
    completedCourses.push_back(course);
}

void Student::submitAssignment(const string& assignment) {
    cout << name << " has submitted the assignment " << assignment << endl;
}

void Student::checkProgress() const {
    cout << name << "'s completed courses: ";
    for (const auto& course : completedCourses) {
        cout << course << " ";
    }
    cout << endl;
}

void Student::viewCertification() const {
    cout << name << "'s Certifications: ";
    for (const auto& course : completedCourses) {
        cout << "Certification for " << course << " ";
    }
    cout << endl;
}

void Student::displayInfo() const {
    cout << "Student Name: " << name << "\nStudent ID: " << studentId
         << "\nEnrollment Date: " << enrollmentDate << "\nEmail: " << email << endl;
}

string Student::getRole() const {
    return "Student";
}

void Student::sendNotification(const string& message) const {
    cout << "Notification to Student " << name << ": " << message << endl;
}

void Student::receiveNotification(const Notification& notification) {
    notifications.push_back(notification);
    cout << "Notification sent to student: " << getName() << endl;
}

void Student::displayNotifications() const {
    cout << "\nNotifications for student: " << getName() << endl;
    for (const auto& notification : notifications) {
        notification.displayNotification();
    }
}

void Student::submitAssignment(Assignment* assignment, int score) {
    assignment->submit(this, score);
}

void Student::takeAssessment(Assessment* assessment, int score) {
    assessment->takeAssessment(this, score);
}

void Student::joinGroup(int groupID) {
    Group::addMemberToGroup(groupID, this);
}

bool Student:: operator== (const Student& other) const {
    return (id == other.id && name == other.name && email == other.email);
}

Student& Student::operator=(const Student& other) {
    if (this != &other) {
        id = other.id;
        name = other.name;
        email = other.email;
        studentId = other.studentId;
        enrollmentDate = other.enrollmentDate;
        completedCourses = other.completedCourses;
        notifications = other.notifications;
        group = other.group;
    }
    return *this;
}

ostream& operator<<(ostream& out, const Student& student) {
    out << "Student ID: " << student.getId() << "\n"
        << "Name: " << student.getName() << "\n"
        << "Email: " << student.getEmail() << "\n"
        << "Student ID: " << student.studentId << "\n"
        << "Enrollment Date: " << student.enrollmentDate;
    return out;
}

istream& operator>>(istream& in, Student& student) {
    cout << "Enter Student ID: ";
    in >> student.studentId;
    in.ignore();
    cout << "Enter Name: ";
    getline(in, student.name);
    cout << "Enter Email: ";
    getline(in, student.email);
    cout << "Enter Enrollment Date: ";
    getline(in, student.enrollmentDate);
    return in;
}

double& Student::operator[](int index) {
    if (index < 0 || index >= gpaRecords.size()) {
        cout << "Index out of bounds" << endl;
        static double dummyGPA = -1.0;  
        return dummyGPA; 
    } else {
        return gpaRecords[index]; 
    }
}

set<string> Student:: operator|(const Student& other) const {
        set<string> unionCourses (completedCourses.begin(), completedCourses.end());
        set<string> otherCourses (other.completedCourses.begin(), other.completedCourses.end());
        set<string> result;
        
        set_union(unionCourses.begin(), unionCourses.end(),
                  otherCourses.begin(), otherCourses.end(),
                  inserter(result, result.begin()));

        return result;
    }

set<string> Student:: operator&(const Student& other) const {
        set<string> intersectionCourses (completedCourses.begin(), completedCourses.end());
        set<string> otherCourses  (other.completedCourses.begin(), other.completedCourses.end());
        set<string> result;

        set_intersection(intersectionCourses.begin(), intersectionCourses.end(),
                         otherCourses.begin(), otherCourses.end(),
                         inserter(result, result.begin()));

        return result;
    }

// Module class methods
Module::Module(const string& moduleId, const string& moduleTitle, const vector<string>& contentSections)
    : moduleId(moduleId), moduleTitle(moduleTitle), contentSections(contentSections) {}

string Module::getModuleId() const {return moduleId;}

string Module::getModuleTitle() const {return moduleTitle;}

void Module::displayModuleDetails() const {
    cout << "Module Title: " << moduleTitle << "\nModule ID: " << moduleId << "\nContent Sections:\n";
    for (const auto& section : contentSections) {
        cout << "- " << section << "\n";
    }
}

void Module::assignModuleToCourse(Course* course) {
    course->addModule(*this);
}

bool Module::operator==(const Module& other) const {
    return (moduleId == other.moduleId && moduleTitle == other.moduleTitle);
}

Module& Module::operator=(const Module& other) {
    if (this != &other) {
        moduleId = other.moduleId;
        moduleTitle = other.moduleTitle;
        contentSections = other.contentSections;
    }
    return *this;
}

ostream& operator<<(ostream& out, const Module& module) {
    out << "Module ID: " << module.moduleId << "\n"
        << "Module Title: " << module.moduleTitle << "\n"
        << "Content Sections: ";
    for (const auto& section : module.contentSections) {
        out << section << " ";
    }
    return out;
}

istream& operator>>(istream& in, Module& module) {
    cout << "Enter Module ID: ";
    in >> module.moduleId;
    in.ignore();
    cout << "Enter Module Title: ";
    getline(in, module.moduleTitle);
    cout << "Enter Content Sections (space separated, end with a new line): ";
    string section;
    while (getline(in, section)) {
        if (section.empty()) break;
        module.contentSections.push_back(section);
    }
    return in;
}

// Course class methods
Course::Course(const string& courseTitle, const string& courseCode, const string& description) : courseTitle(courseTitle), courseCode(courseCode), description(description) {}

string Course:: getCourseTitle() const {return courseTitle;}

void Course::addModule(const Module& module) {
    modules.push_back(module);
}

void Course::assignInstructor(Instructor* inst) {
    instructor = inst;
    cout << "Instructor assigned to course: " << courseTitle << "\n";
}

void Course::enrollStudent(Student* student) {
    students.insert(student);
    cout << "Student enrolled in course: " << courseTitle << "\n";
}

void Course::displayCourseDetails() const {
    cout << "Course Title: " << courseTitle << "\nCourse Code: " << courseCode << "\nDescription: " << description << "\n";
    if (instructor) {
        cout << "Instructor: Assigned\n";
    } else {
        cout << "Instructor: Not assigned\n";
    }
    cout << "Number of enrolled students: " << students.size() << "\n";
    cout << "Modules:\n";
    for (const auto& module : modules) {
        module.displayModuleDetails();
    }
}

void Course::issueCertificate(Student* student) {
    if (students.find(student) != students.end()) {
        string certID = courseCode + "-" + to_string(rand() % 10000);
        string issueDate = "2024-12-01";
        Certificate certificate(certID, issueDate, courseTitle, student->getName());
        cout << "Certificate issued to " << student->getName() << " for completing course: " << courseTitle << "\n";
        certificate.displayCertificate();
    } else {
        cout << "Error: Student is not enrolled in the course: " << courseTitle << "\n";
    }
}

bool Course::operator==(const Course& other) const {
    return (courseCode == other.courseCode && courseTitle == other.courseTitle);
}

Course& Course::operator=(const Course& other) {
    if (this != &other) {
        courseTitle = other.courseTitle;
        courseCode = other.courseCode;
        description = other.description;
        modules = other.modules;
        instructor = other.instructor;
        students = other.students;
    }
    return *this;
}

ostream& operator<<(ostream& out, const Course& course) {
    out << "Course Title: " << course.courseTitle << "\n"
        << "Course Code: " << course.courseCode << "\n"
        << "Description: " << course.description;
    return out;
}

istream& operator>>(istream& in, Course& course) {
    cout << "Enter Course Title: ";
    getline(in, course.courseTitle);
    cout << "Enter Course Code: ";
    getline(in, course.courseCode);
    cout << "Enter Course Description: ";
    getline(in, course.description);
    return in;
}

Course& Course:: operator+(Student* student) {
        students.insert(student); 
        return *this;
    }

Course& Course:: operator-(Student* student) {
        students.erase(student); 
        return *this;
    }

// Instructor class methods
Instructor::Instructor(const long& id, const string& name, const string& email, const long& employeeId, const string& department) : Person(id, name, email), employeeId(employeeId), department(department) {}

void Instructor::createAssignment(const string& courseName, const string& assignmentName) {
    cout << "Instructor " << name << " has created assignment '" << assignmentName << "' for course " << courseName << ".\n";
}

void Instructor::gradeSubmission(const string& studentName, const string& courseName, int grade) {
    cout << "Instructor " << name << " has graded " << studentName << "'s submission for course " << courseName << " with grade: " << grade << ".\n";
}

void Instructor::monitorStudentProgress(const string& studentName, const string& courseName) {
    cout << "Instructor " << name << " is monitoring progress of student " << studentName << " in course " << courseName << ".\n";
}

void Instructor::issueCertification(const string& studentName, const string& courseName) {
    cout << "Instructor " << name << " has issued certification to " << studentName << " for completing course " << courseName << ".\n";
}

void Instructor::assignCourse(Course* course) {
    assignedCourses.push_back(course);
    cout << "Instructor " << name << " is now assigned to course " << course->getCourseTitle() << ".\n";
}

void Instructor::displayInfo() const {
    cout << "Instructor Name: " << name << "\nEmployee ID: " << employeeId
         << "\nDepartment: " << department << "\nEmail: " << email << endl;
}

string Instructor::getRole() const {
    return "Instructor";
}

void Instructor::sendNotification(const string& message) const {
    cout << "Notification to Instructor " << name << ": " << message << endl;
}

void Instructor::receiveNotification(const Notification& notification) {
    notifications.push_back(notification);
    cout << "Notification sent to instructor: " << getName() << endl;
}

void Instructor::displayNotifications() const {
    cout << "\nNotifications for instructor: " << getName() << endl;
    for (const auto& notification : notifications) {
        notification.displayNotification();
    }
}

void Instructor::assignGrade(Assessment* assessment, int grade) {
    assessment->assignGrade(grade);
}

bool Instructor::operator==(const Instructor& other) const {
    return (id == other.id && name == other.name && email == other.email);
}

Instructor& Instructor::operator=(const Instructor& other) {
    if (this != &other) {
        id = other.id;
        name = other.name;
        email = other.email;
        employeeId = other.employeeId;
        department = other.department;
        assignedCourses = other.assignedCourses;
        notifications = other.notifications;
    }
    return *this;
}

ostream& operator<<(ostream& out, const Instructor& instructor) {
    out << "Instructor ID: " << instructor.getId() << "\n"
        << "Name: " << instructor.getName() << "\n"
        << "Email: " << instructor.getEmail() << "\n"
        << "Employee ID: " << instructor.employeeId << "\n"
        << "Department: " << instructor.department;
    return out;
}

istream& operator>>(istream& in, Instructor& instructor) {
    cout << "Enter Employee ID: ";
    in >> instructor.employeeId;
    in.ignore();
    cout << "Enter Name: ";
    getline(in, instructor.name);
    cout << "Enter Email: ";
    getline(in, instructor.email);
    cout << "Enter Department: ";
    getline(in, instructor.department);
    return in;
}

// Methods for Notification class
Notification:: Notification(const long& notificationId, const string& message, const string& dateSent, vector<string> recipients) : notificationId(notificationId), message(message), dateSent(dateSent), recipients(recipients) {}
    
void Notification:: displayNotification() const {
    cout << "Notification ID: " << notificationId << "\nMessage: " << message
             << "\nDate Sent: " << dateSent << "\nRecipients: ";
    for (const auto& recipient : recipients) {
        cout << recipient << " ";
    }
    cout << endl;
    }

long Notification::getNotificationId() const { return notificationId; }

string Notification::getMessage() const { return message; }

string Notification::getDateSent() const { return dateSent; }

bool Notification::operator==(const Notification& other) const {
    return (notificationId == other.notificationId && message == other.message && dateSent == other.dateSent);
    }

Notification& Notification::operator=(const Notification& other) {
    if (this != &other) {
        notificationId = other.notificationId;
        message = other.message;
        dateSent = other.dateSent;
        recipients = other.recipients;
    }
    return *this;
    }

ostream& operator<<(ostream& out, const Notification& notification) {
    out << "Notification ID: " << notification.notificationId << "\n"
        << "Message: " << notification.message << "\n"
        << "Date Sent: " << notification.dateSent << "\n"
        << "Recipients: ";
    for (const auto& recipient : notification.recipients) {
        out << recipient << " ";
    }
    out << "\n";
    return out;
}

istream& operator>>(istream& in, Notification& notification) {
    cout << "Enter Notification ID: ";
    in >> notification.notificationId;
    in.ignore();
    cout << "Enter Message: ";
    getline(in, notification.message); 
    cout << "Enter Date Sent: ";
    getline(in, notification.dateSent); 
    cout << "Enter number of recipients: ";
    int numRecipients;
    in >> numRecipients;
    in.ignore();
    notification.recipients.clear();
    for (int i = 0; i < numRecipients; ++i) {
        cout << "Enter recipient " << i + 1 << ": ";
        string recipient;
        getline(in, recipient);
        notification.recipients.push_back(recipient);
    }
    return in;
}

// Public methods for Admin class
Admin :: Admin(const long& id, const string& name, const string& email, const long& adminId, const vector<string>& privileges, const string& department)
        : Person(id, name, email), adminId(adminId), privileges(privileges), department(department) {}

void Admin::addCourse(const string &courseName)
    {
        cout << "Admin " << getName() << " has added the course: " << courseName << ".\n";
    }

void Admin:: removeCourse(const string& courseName) {
        cout << "Admin " << getName() << " has removed the course: " << courseName << ".\n";
    }

void Admin:: assignInstructor(const string& instructorName, const string& courseName) {
        cout << "Admin " << getName() << " has assigned instructor " << instructorName << " to course " << courseName << ".\n";
    }

void Admin:: generateReports() const {
        cout << "Admin " << getName() << " is generating system reports.\n";
    }

void Admin:: manageCertificates(const string& studentName, const string& courseName) {
        cout << "Admin " << getName() << " has managed certification for " << studentName  << " in course " << courseName << ".\n";
    }

void Admin:: sendSystemNotification(const string& message, const vector<string>& recipients) {
        string dateSend = "2024-12-01";  // Hardcoded date
        Notification notification(rand(), message, dateSend, recipients);
        cout << "Notification sent by Admin: " << message << "\n";
    }

void Admin:: displayInfo() const {
        cout << "Admin Info:\n"  << "Name: " << name << "\nEmail: " << email   << "\nID: " << id << "\nAdmin ID: " << adminId  << "\nPrivileges: ";
    }

string Admin:: getRole() const {
        return "Admin";
    }

void Admin:: sendNotification(const string& message) const {
        cout << "System Notification sent by Admin: " << message << "\n";
    }

bool Admin::operator==(const Admin& other) const {
    return (id == other.id && name == other.name && email == other.email && adminId == other.adminId);
    }

Admin& Admin::operator=(const Admin& other) {
    if (this != &other) {
        id = other.id;
        name = other.name;
        email = other.email;
        adminId = other.adminId;
        privileges = other.privileges;
        department = other.department;
    }
    return *this;
    }

ostream& operator<<(ostream& out, const Admin& admin) {
    out << "Admin ID: " << admin.getId() << "\n"
        << "Name: " << admin.getName() << "\n"
        << "Email: " << admin.getEmail() << "\n"
        << "Admin ID: " << admin.adminId << "\n"
        << "Privileges: ";
    for (const auto& privilege : admin.privileges) {
        out << privilege << " ";
    }
    return out;
}

istream& operator>>(istream& in, Admin& admin) {
    cout << "Enter Admin ID: ";
    in >> admin.adminId;
    in.ignore();
    cout << "Enter Name: ";
    getline(in, admin.name);
    cout << "Enter Email: ";
    getline(in, admin.email);
    cout << "Enter Privileges (space separated, end with a new line): ";
    string privilege;
    while (getline(in, privilege)) {
        if (privilege.empty()) break;
        admin.privileges.push_back(privilege);
    }
    return in;
}

// Methods for Assignment Class
Assignment :: Assignment(const int& id, const string& desc, int maxScore, const string& dueDate, Instructor* instr) : assignmentId(id), description(desc), maxScore(maxScore), dueDate(dueDate), instructor(instr) {}

void Assignment::assignGrade(int grade) {
    maxScore = grade;
}

void Assignment :: submit(Student* student, int score) {
        if (score <= maxScore) {
            studentSubmissions[student] = score;
            cout << "Student " << student->getName() << " submitted assignment: " << assignmentId << " with score: " << score << endl;
        } else {
            cout << "Error: Score exceeds maximum allowed score (" << maxScore << ")!" << endl;
        }
    }

void Assignment :: gradeSubmission(Student* student, int score) {
        if (studentSubmissions.find(student) != studentSubmissions.end()) {
            if (score <= maxScore) {
                studentSubmissions[student] = score;
                cout << "Instructor " << instructor->getName() << " graded assignment: " << assignmentId << " for student: " << student->getName() << " with score: " << score << endl;
            } else {
                cout << "Error: Grade exceeds maximum allowed score (" << maxScore << ")!" << endl;
            }
        } else {
            cout << "Error: No submission found for student: " << student->getName() << endl;
        }
    }

void Assignment :: displayDetails() const {
        cout << "Assignment ID: " << assignmentId << "\nDescription: " << description << "\nMax Score: " << maxScore << "\nDue Date: " << dueDate << endl;
    }

void Assignment :: displaySubmissions() const {
        cout << "Submissions for Assignment " << assignmentId << ":\n";
        for (const auto& [student, score] : studentSubmissions) {
            cout << "Student: " << student->getName() << ", Score: " << score << endl;
        }
    }

bool Assignment::operator==(const Assignment& other) const {
    return (assignmentId == other.assignmentId && description == other.description);
    }

Assignment& Assignment::operator=(const Assignment& other) {
    if (this != &other) {
        assignmentId = other.assignmentId;
        description = other.description;
        maxScore = other.maxScore;
        dueDate = other.dueDate;
        instructor = other.instructor;
        studentSubmissions = other.studentSubmissions;
    }
    return *this;
    }

Assignment Assignment:: operator+(const Assignment& other) const {
        return Assignment(0, "Combined Assignment", this->maxScore + other.maxScore, "N/A", nullptr);
    }

ostream& operator<<(ostream& out, const Assignment& assignment) {
    out << "Assignment ID: " << assignment.assignmentId << "\n"
        << "Description: " << assignment.description << "\n"
        << "Max Score: " << assignment.maxScore << "\n"
        << "Due Date: " << assignment.dueDate;
    return out;
}

istream& operator>>(istream& in, Assignment& assignment) {
    cout << "Enter Assignment ID: ";
    in >> assignment.assignmentId;
    in.ignore();
    cout << "Enter Description: ";
    getline(in, assignment.description);
    cout << "Enter Max Score: ";
    in >> assignment.maxScore;
    in.ignore();
    cout << "Enter Due Date: ";
    getline(in, assignment.dueDate);
    return in;
}

// Methods of Assesment Class
    Assessment:: Assessment(const int& id, const string& type, int marks) : assessmentId(id), assessmentType(type), totalMarks(marks) {}

void Assessment:: assignGrade(int grade) {
        totalMarks = grade;
    }

void Assessment:: takeAssessment(Student* student, int score) {
        if (score <= totalMarks) {
            studentScores[student] = score;
            cout << "Student " << student->getName() << " took assessment: " << assessmentId << " and scored: " << score << endl;
        } else {
            cout << "Error: Score exceeds maximum marks (" << totalMarks << ")!" << endl;
        }
    }

void Assessment:: displayScores() const {
        cout << "Scores for Assessment " << assessmentId << " (" << assessmentType << "):\n";
        for (const auto& [student, score] : studentScores) {
            cout << "Student: " << student->getName() << ", Score: " << score << endl;
        }
    }

void Assessment:: displayDetails() const {
        cout << "Assessment ID: " << assessmentId << "\nType: " << assessmentType << "\nTotal Marks: " << totalMarks << endl;
    }

bool Assessment::operator==(const Assessment& other) const {
    return (assessmentId == other.assessmentId && assessmentType == other.assessmentType);
    }

Assessment& Assessment::operator=(const Assessment& other) {
    if (this != &other) {
        assessmentId = other.assessmentId;
        assessmentType = other.assessmentType;
        totalMarks = other.totalMarks;
        studentScores = other.studentScores;
    }
    return *this;
    }

ostream& operator<<(ostream& out, const Assessment& assessment) {
    out << "Assessment ID: " << assessment.assessmentId << "\n"
        << "Assessment Type: " << assessment.assessmentType << "\n"
        << "Total Marks: " << assessment.totalMarks;
    return out;
}

istream& operator>>(istream& in, Assessment& assessment) {
    cout << "Enter Assessment ID: ";
    in >> assessment.assessmentId;
    in.ignore();
    cout << "Enter Assessment Type: ";
    getline(in, assessment.assessmentType);
    cout << "Enter Total Marks: ";
    in >> assessment.totalMarks;
    return in;
}

// Methods of certificate Class
Certificate:: Certificate(const string& id, const string& date, const string& course, const string& recipient) : certificateId(id), issueDate(date), courseTitle(course), recipientName(recipient) {}

void Certificate:: displayCertificate() const {
        cout << "Certificate ID: " << certificateId << "\nIssue Date: " << issueDate << "\nCourse Title: " << courseTitle << "\nRecipient: " << recipientName << "\n";
    }

bool Certificate::operator==(const Certificate& other) const {
    return (certificateId == other.certificateId && issueDate == other.issueDate && courseTitle == other.courseTitle && recipientName == other.recipientName);
    }

Certificate& Certificate::operator=(const Certificate& other) {
    if (this != &other) {
        certificateId = other.certificateId;
        issueDate = other.issueDate;
        courseTitle = other.courseTitle;
        recipientName = other.recipientName;
    }
    return *this;
    }


ostream& operator<<(ostream& out, const Certificate& certificate) {
    out << "Certificate ID: " << certificate.certificateId << "\n"
        << "Issue Date: " << certificate.issueDate << "\n"
        << "Course Title: " << certificate.courseTitle << "\n"
        << "Recipient: " << certificate.recipientName;
    return out;
}

istream& operator>>(istream& in, Certificate& certificate) {
    cout << "Enter Certificate ID: ";
    getline(in, certificate.certificateId);
    cout << "Enter Issue Date: ";
    getline(in, certificate.issueDate);
    cout << "Enter Course Title: ";
    getline(in, certificate.courseTitle);
    cout << "Enter Recipient: ";
    getline(in, certificate.recipientName);
    return in;
}

