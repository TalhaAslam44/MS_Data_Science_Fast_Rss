#ifndef COURSERA_H
#define COURSERA_H

#include <ctime>
#include <vector>
#include <string>
#include <set>
#include <map>
using namespace std;

// Forward Declarations
class Student;
class Instructor;
class Notification;
class Assignment;
class Assessment;
class Course;
class Admin;

// Person class (Abstract Base Class)
class Person {

protected:
    long id;
    string name, email;

public:
    Person(const long& id, const string& name, const string& email);
    void setId(long id);
    void setName(string name);
    void setEmail(string email);
    long getId() const;
    string getName() const;
    string getEmail() const;

    virtual void displayInfo() const = 0; // Pure virtual function
    virtual string getRole() const = 0; // Pure virtual function
    virtual void sendNotification(const string& message) const = 0; // Pure virtual function
};

// Group class
class Group {

private:
    int groupID;
    string groupName;
    static map<int, vector<Student*>> groups;

public:
    Group(int groupID, const string& groupName);
    static void addMemberToGroup(int groupID, Student* student);
    static void removeMemberFromGroup(int groupID, Student* student);
    static void displayGroupMembers(int groupID);
    static void initiateDiscussion(int groupID, const string& topic);
    friend ostream& operator<<(ostream& out, const Group& group);
    friend istream& operator>>(istream& in, Group& group);
};

// Student Class (Derived from base class Person)
class Student : public Person {

private:
    long studentId;
    string enrollmentDate;
    vector<string> completedCourses;
    Group* group;
    vector<Notification> notifications; 
    vector<double> gpaRecords;
public:
    Student(const long& id, const string& name, const string& email, const long& studentId, const string& enrollmentDate);
    void addCompletedCourse(const std::string& course);
    void enrollInCourse(const string& course);
    void submitAssignment(const string& assignment); 
    void checkProgress() const;
    void viewCertification() const;
    void displayInfo() const override;
    string getRole() const override;
    void sendNotification(const string& message) const override;
    void receiveNotification(const Notification& notification);
    void displayNotifications() const;
    void submitAssignment(Assignment* assignment, int score);
    void takeAssessment(Assessment* assessment, int score);
    void joinGroup(int groupID);
    bool operator== (const Student& other) const;
    Student& operator=(const Student& other);
    friend ostream& operator<<(ostream& out, const Student& student);
    friend istream& operator>>(istream& in, Student& student);
    double& operator[](int index);
    set<string> operator|(const Student& other) const;
    set<string> operator&(const Student& other) const;
};

// Module Class (Composition with class Course)
class Module {
private:
    string moduleId, moduleTitle;
    vector<string> contentSections;

public:
    Module(const string& moduleId, const string& moduleTitle, const vector<string>& contentSections);
    string getModuleId() const;
    string getModuleTitle() const;
    void displayModuleDetails() const;
    void assignModuleToCourse(Course* course);
    bool operator==(const Module& other) const;
    Module& operator=(const Module& other);
    friend ostream& operator<<(ostream& out, const Module& module);
    friend istream& operator>>(istream& in, Module& module);
};

// Course class
class Course {

private:
    string courseTitle, courseCode, description;
    vector<Module> modules;
    Instructor* instructor;
    set<Student*> students;

public:
    Course(const string& courseTitle, const string& courseCode, const string& description);
    string getCourseTitle() const;
    void addModule(const Module& module);
    void assignInstructor(Instructor* inst);
    void enrollStudent(Student* student);
    void displayCourseDetails() const;
    void issueCertificate(Student* student);
    bool operator== (const Course& other) const;
    Course& operator=(const Course& other);
    friend ostream& operator<<(ostream& out, const Course& course);
    friend istream& operator>>(istream& in, Course& course);
    Course& operator+(Student* student);
    Course& operator-(Student* student);
};

// Instructor Class (Derived from base class Person)
class Instructor : public Person {

private:
    long employeeId;
    string department;
    vector<Course*> assignedCourses;
    vector<Notification> notifications;

public:
    Instructor(const long& id, const string& name, const string& email, const long& employeeId, const string& department);
    void createAssignment(const string& courseName, const string& assignmentName);
    void gradeSubmission(const string& studentName, const string& courseName, int grade);
    void monitorStudentProgress(const string& studentName, const string& courseName);
    void issueCertification(const string& studentName, const string& courseName);
    void assignCourse(Course* course);
    void displayInfo() const override;
    string getRole() const override;
    void sendNotification(const string& message) const override;
    void receiveNotification(const Notification& notification);
    void displayNotifications() const;
    void assignGrade(Assessment* assessment, int grade);
    bool operator== (const Instructor& other) const;
    Instructor& operator=(const Instructor& other);
    friend ostream& operator<<(ostream& out, const Instructor& instructor);
    friend istream& operator>>(istream& in, Instructor& instructor);
};

// Notification class
class Notification {

private:
    long notificationId;
    string message;
    string dateSent;
    vector<string> recipients;

public:
    Notification(const long& notificationId, const string& message, const string& dateSent, vector<string> recipients);
    void displayNotification() const;
    long getNotificationId() const;
    string getMessage() const;
    string getDateSent() const;
    bool operator==(const Notification& other) const;
    Notification& operator=(const Notification& other);
    friend ostream& operator<<(ostream& out, const Notification& notification);
    friend istream& operator>>(istream& in, Notification& notification);
};

// Admin class derived from base class Person
class Admin : private Person {

private:
    long adminId;
    vector<string> privileges;
    string department;

public:
    Admin(const long& id, const string& name, const string& email, const long& adminId, const vector<string>& privileges, const string& department);
    void addCourse(const string& courseName);
    void removeCourse(const string& courseName);
    void assignInstructor(const string& instructorName, const string& courseName);
    void generateReports() const;
    void manageCertificates(const string& studentName, const string& courseName);
    void sendSystemNotification(const string& message, const vector<string>& recipients);
    void displayInfo() const override;
    string getRole() const override;
    void sendNotification(const string& message) const override;
    bool operator==(const Admin& other) const;
    Admin& operator=(const Admin& other);
    friend ostream& operator<<(ostream& out, const Admin& admin);
    friend istream& operator>>(istream& in, Admin& admin);
};

// Assignment Class
class Assignment {

private:
    int assignmentId;
    string description;
    int maxScore;
    string dueDate;
    map<Student*, int> studentSubmissions;
    Instructor* instructor;

public:
    Assignment(const int& id, const string& desc, int maxScore, const string& dueDate, Instructor* instr);
    void assignGrade(int grade);
    void submit(Student* student, int score);
    void gradeSubmission(Student* student, int score);
    void displayDetails() const;
    void displaySubmissions() const;
    bool operator==(const Assignment& other) const;
    Assignment& operator=(const Assignment& other);
    Assignment operator+(const Assignment& other) const;
    friend ostream& operator<<(ostream& out, const Assignment& assignment);
    friend istream& operator>>(istream& in, Assignment& assignment);
};

// Assessment Class
class Assessment {

private:
    int assessmentId;
    string assessmentType;
    int totalMarks;
    map<Student*, int> studentScores;

public:
    Assessment(const int& id, const string& type, int marks);
    void assignGrade(int grade);
    void takeAssessment(Student* student, int score);
    void displayScores() const;
    void displayDetails() const;
    bool operator==(const Assessment& other) const;
    Assessment& operator=(const Assessment& other);
    friend ostream& operator<<(ostream& out, const Assessment& assessment);
    friend istream& operator>>(istream& in, Assessment& assessment);
};

// Certificate Class
class Certificate {

private:
    string certificateId;
    string issueDate;
    string courseTitle;
    string recipientName;

public:
    Certificate(const string& id, const string& date, const string& course, const string& recipient);
    void displayCertificate() const;
    bool operator==(const Certificate& other) const;
    Certificate& operator=(const Certificate& other);
    friend ostream& operator<<(ostream& out, const Certificate& certificate);
    friend istream& operator>>(istream& in, Certificate& certificate);
};

#endif
