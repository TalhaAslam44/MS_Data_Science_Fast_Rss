                    // This Project is done by two members 1. Haider Rasool Qadri (24I-8023) and 2. Talha Aslam (24I-8067).

#include "24I8023_24I8067_Coursera.h"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

/*
int main() {
    // Creating objects of Student type
    Student student1(1, "Alice", "alice@example.com", 12345, "01-12-2024");
    Student student2(2, "Bob", "bob@example.com", 67890, "02-12-2024");


    // Test ostream for Student
    cout << "Student 1 Details: " << student1 << endl;
    cout << "Student 2 Details: " << student2 << endl;

    // Add completed courses to students
    student1.addCompletedCourse("Object Oriented Programming");
    student1.addCompletedCourse("Data Structure");
    student2.addCompletedCourse("Data Structure");
    student2.addCompletedCourse("Database Management System");

    // Test '|' operator (Union of courses)
    cout << "Union of courses completed by Alice and Bob: ";
    for (const auto& course : (student1 | student2)) {
        cout << course << ", ";
    }
    cout << endl;

    // Test '&' operator (Intersection of courses)
    cout << "Intersection of courses completed by Alice and Bob: ";
    for (const auto& course : (student1 & student2)) {
        cout << course << ", ";
    }
    cout << endl;

  // Test [] operator for GPA
    student1[0] = 3.8;
    cout << "Alice's GPA: " << student1[0] << endl;

    // Test Course class operators
    Course course1("Computer Science", "CS101", "Description");
    Course course2("Data Structures", "CS102", "Description");

    // Test == operator
    if (course1 == course2) {
        cout << "Both the courses are same" << endl;
    } else {
        cout << "Both courses are different from each other" << endl;
    }

    // Test ostream for Course
    cout << "Course 1 Details: " << course1 << endl;
    cout << "Course 2 Details: " << course2 << endl;

    // Test Assignment class operators
    Instructor instructor1(1, "Dr. Smith", "smith@university.edu", 123, "Computer Science");
    Assignment assignment1(1, "Quiz 1", 50, "15-12-2014", &instructor1);
    Assignment assignment2(2, "Project", 100, "20-12-2024", &instructor1);

    Assignment combinedAssignment = assignment1 + assignment2;
    cout << "Combined Assignment Marks: " << combinedAssignment << endl;


    // Test ostream for Assignment
    cout << "Assignment 1 Details: " << assignment1 << endl;
    cout << "Assignment 2 Details: " << assignment2 << endl;
}
*/

int main() {
    int choice, subchoice;

    do {
        cout << "\n------ Coursera Management System ------\n";
        cout << "\n--- Main Menu ---\n";
        cout << "1. Manage Student\n";
        cout << "2. Manage Instructor\n";
        cout << "3. Manage Admin\n";
        cout << "4. Manage Course\n";
        cout << "5. Manage Module\n";
        cout << "6. Manage Assignment\n";
        cout << "7. Manage Assessment\n";
        cout << "8. Manage Certificates\n";
        cout << "9. Manage Notifications\n";
        cout << "10. Manage Groups\n";
        cout << "11. Exit the Program\n";

        cout << "Enter Your Choice: ";
        cin >> choice;

        switch (choice) {
        case 1: {
            Student s1(1, "Haider", "haider@gmail.com", 10, "12-12-2012");
            string courName, assignmentName;
            int score;

            do {
                cout << "\n--- Manage Students ---\n";
                cout << "1. Display Information of the Student\n";
                cout << "2. Enroll in Course\n";
                cout << "3. Submit Assignment\n";
                cout << "4. Check Progress\n";
                cout << "5. View Certification\n";
                cout << "6. Send Notification\n";
                cout << "7. Receive Notification\n";
                cout << "8. Join Group\n";
                cout << "9. Exit to Main Menu\n";

                cout << "Enter Your Choice: ";
                cin >> subchoice;

                switch (subchoice) {
                    case 1:
                        s1.displayInfo();
                        break;

                    case 2:
                        cout << "Enter course name: ";
                        cin.ignore();
                        getline(cin, courName);
                        s1.enrollInCourse(courName);
                        cout << "Student Enrolled in course successfully.\n";
                        break;

                    case 3:
                        cout << "Enter assignment name: ";
                        cin.ignore();
                        getline(cin, assignmentName);
                        s1.submitAssignment(assignmentName);
                        cout << "Assignment submitted successfully.\n";
                        break;

                    case 4:
                        s1.checkProgress();
                        break;

                    case 5:
                        s1.viewCertification();
                        break;

                    case 6:
                        {
                            string message;
                            cout << "Enter the notification message: ";
                            cin.ignore();
                            getline(cin, message);
                            long notificationId = 1;
                            string dateSent = "2024-12-07";
                            vector<string> recipients = {"haider@gmail.com"};
                            Notification notification(notificationId, message, dateSent, recipients);
                            s1.sendNotification(message);
                            cout << "Notification sent.\n";
                        }
                        break;

                    case 7:
                        {
                            long notificationId = 1;
                            string message = "This is a notification message.";
                            string dateSent = "2024-12-07";
                            vector<string> recipients = {"haider@gmail.com"};
                            Notification notification(notificationId, message, dateSent, recipients);
                            s1.receiveNotification(notification);
                            cout << "Notification received.\n";
                        }
                        break;

                    case 8:
                        int groupID;
                        cout << "Enter group ID: ";
                        cin >> groupID;
                        s1.joinGroup(groupID);
                        cout << "Joined group successfully.\n";
                        break;

                    case 9:
                        cout << "Returning to Main Menu...\n";
                        break;

                    default:
                        cout << "\nInvalid Choice. Try Again.\n";
                }
            } while (subchoice != 9);
            break;
        }

        case 2: {
            Instructor instructor(1, "Dr. Smith", "dr.smith@gmail.com", 1001, "Computer Science");
            string courseName, assignmentName, studentName;
            int grade;

            do {
                cout << "\n--- Manage Instructors ---\n";
                cout << "1. Display Information of the Instructor\n";
                cout << "2. Create Assignment\n";
                cout << "3. Grade Submission\n";
                cout << "4. Monitor Student Progress\n";
                cout << "5. Issue Certification\n";
                cout << "6. Assign Course\n";
                cout << "7. Send Notification\n";
                cout << "8. Receive Notification\n";
                cout << "9. Exit to Main Menu\n";

                cout << "Enter Your Choice: ";
                cin >> subchoice;

                switch (subchoice) {
                    case 1:
                        instructor.displayInfo();
                        break;

                    case 2:
                        cout << "Enter course name: ";
                        cin.ignore();
                        getline(cin, courseName);
                        cout << "Enter assignment name: ";
                        getline(cin, assignmentName);
                        instructor.createAssignment(courseName, assignmentName);
                        break;

                    case 3:
                        cout << "Enter student name: ";
                        cin.ignore();
                        getline(cin, studentName);
                        cout << "Enter course name: ";
                        getline(cin, courseName);
                        cout << "Enter grade: ";
                        cin >> grade;
                        instructor.gradeSubmission(studentName, courseName, grade);
                        break;

                    case 4:
                        cout << "Enter student name: ";
                        cin.ignore();
                        getline(cin, studentName);
                        cout << "Enter course name: ";
                        getline(cin, courseName);
                        instructor.monitorStudentProgress(studentName, courseName);
                        break;

                    case 5:
                        cout << "Enter student name: ";
                        cin.ignore();
                        getline(cin, studentName);
                        cout << "Enter course name: ";
                        getline(cin, courseName);
                        instructor.issueCertification(studentName, courseName);
                        break;

                    case 6:
                        // Add logic for assigning courses to instructor
                        break;

                    case 7:
                        {
                            string message;
                            cout << "Enter the notification message: ";
                            cin.ignore();
                            getline(cin, message);
                            long notificationId = 1;
                            string dateSent = "2024-12-07";
                            vector<string> recipients = {"dr.smith@gmail.com"};
                            Notification notification(notificationId, message, dateSent, recipients);
                            instructor.sendNotification(message);
                            cout << "Notification sent.\n";
                        }
                        break;

                    case 8:
                        {
                            long notificationId = 1;
                            string message = "This is a notification message.";
                            string dateSent = "2024-12-07";
                            vector<string> recipients = {"dr.smith@gmail.com"};
                            Notification notification(notificationId, message, dateSent, recipients);
                            instructor.receiveNotification(notification);
                            cout << "Notification received.\n";
                        }
                        break;

                    case 9:
                        cout << "Returning to Main Menu...\n";
                        break;

                    default:
                        cout << "\nInvalid Choice. Try Again.\n";
                }
            } while (subchoice != 9);
            break;
        }

        case 3: {
            Admin admin(1, "Admin", "admin@coursera.com", 10001, {"Manage Users", "Create Courses", "Generate Reports"}, "Admin Department");
            string courseName, instructorName, studentName;
            vector<string> recipients;
            int subsubchoice;

            do {
                cout << "\n--- Manage Admin ---\n";
                cout << "1. Display Information of the Admin\n";
                cout << "2. Add Course\n";
                cout << "3. Remove Course\n";
                cout << "4. Assign Instructor\n";
                cout << "5. Generate Reports\n";
                cout << "6. Manage Certificates\n";
                cout << "7. Send System Notification\n";
                cout << "8. Exit to Main Menu\n";

                cout << "Enter Your Choice: ";
                cin >> subsubchoice;

                switch (subsubchoice) {
                    case 1:
                        admin.displayInfo();
                        break;

                    case 2:
                        cout << "Enter course name: ";
                        cin.ignore();
                        getline(cin, courseName);
                        admin.addCourse(courseName);
                        break;

                    case 3:
                        cout << "Enter course name: ";
                        cin.ignore();
                        getline(cin, courseName);
                        admin.removeCourse(courseName);
                        break;

                    case 4:
                        cout << "Enter instructor name: ";
                        cin.ignore();
                        getline(cin, instructorName);
                        cout << "Enter course name: ";
                        getline(cin, courseName);
                        admin.assignInstructor(instructorName, courseName);
                        break;

                    case 5:
                        admin.generateReports();
                        break;

                    case 6:
                        cout << "Enter student name: ";
                        cin.ignore();
                        getline(cin, studentName);
                        cout << "Enter course name: ";
                        getline(cin, courseName);
                        admin.manageCertificates(studentName, courseName);
                        break;

                    case 7:
                        {
                            string message;
                            cout << "Enter the notification message: ";
                            cin.ignore();
                            getline(cin, message);
                            cout << "Enter recipient emails (comma separated): ";
                            string emails;
                            getline(cin, emails);
                            // Assuming recipient emails are separated by commas
                            size_t pos = 0;
                            while ((pos = emails.find(',')) != string::npos) {
                                recipients.push_back(emails.substr(0, pos));
                                emails.erase(0, pos + 1);
                            }
                            recipients.push_back(emails);
                            admin.sendSystemNotification(message, recipients);
                            cout << "System Notification sent.\n";
                        }
                        break;

                    case 8:
                        cout << "Returning to Main Menu...\n";
                        break;

                    default:
                        cout << "\nInvalid Choice. Try Again.\n";
                }
            } while (subsubchoice != 8);
            break;
        }

        case 4: {
            Course course("CS2001", "C++ Programming", "Dr. Smith");
            int groupID;
            string studentName;

            do {
                cout << "\n--- Manage Courses ---\n";
                cout << "1. Display Course Details\n";
                cout << "2. Add Module\n";
                cout << "3. Assign Student to Group\n";
                cout << "4. Exit to Main Menu\n";

                cout << "Enter Your Choice: ";
                cin >> subchoice;

                Student s1(1, "studentName", "email@example.com", 12345, "2024-12-07");
                switch (subchoice) {
                    case 1:
                        course.displayCourseDetails();
                        break;

                    case 2: 
                    {
                        string moduleName;
                        cout << "Enter module name: ";
                        cin.ignore();
                        getline(cin, moduleName);
                        Module module(moduleName, "Module Title", {"Section1", "Section2"});  
                        break;
                    }

                    case 3:
                        course.enrollStudent(&s1);
                        break;

                    case 4:
                        cout << "Returning to Main Menu...\n";
                        break;

                    default:
                        cout << "\nInvalid Choice. Try Again.\n";
                }
            } while (subchoice != 4);
            break;
        }

        case 5: {
            Module module("M1", "Advanced C++", {"Section1", "Section 2"});
            int subsubchoice;

            do {
                cout << "\n--- Manage Modules ---\n";
                cout << "1. Display Module Details\n";
                cout << "2. Assign Module to Course\n";
                cout << "3. Exit to Main Menu\n";

                cout << "Enter Your Choice: ";
                cin >> subsubchoice;

                Course course("CS2001", "C++ Programming", "Dr. Smith");
                switch (subsubchoice) {
                    case 1:
                        module.displayModuleDetails();
                        break;

                    case 2:
                        module.assignModuleToCourse(&course);
                        break;

                    case 3:
                        cout << "Returning to Main Menu...\n";
                        break;

                    default:
                        cout << "\nInvalid Choice. Try Again.\n";
                }
            } while (subsubchoice != 3);
            break;
        }

        case 6: {
            Instructor instructor(1, "Dr. Smith", "dr.smith@gmail.com", 1001, "Computer Science");
            Assignment assignment(1, "Final Project", 100, "2024-12-31", &instructor );
            int score;

            do {
                cout << "\n--- Manage Assignments ---\n";
                cout << "1. Display Assignment Details\n";
                cout << "2. Assign Grade\n";
                cout << "3. Exit to Main Menu\n";

                cout << "Enter Your Choice: ";
                cin >> subchoice;

                switch (subchoice) {
                    case 1:
                        assignment.displayDetails();
                        break;

                    case 2:
                        cout << "Enter grade for assignment: ";
                        cin >> score;
                        assignment.assignGrade(score);
                        break;

                    case 3:
                        cout << "Returning to Main Menu...\n";
                        break;

                    default:
                        cout << "\nInvalid Choice. Try Again.\n";
                }
            } while (subchoice != 3);
            break;
        }

        case 7: {
            Assessment assessment(1, "Final Exam", 100);
            int score;

            do {
                cout << "\n--- Manage Assessments ---\n";
                cout << "1. Display Assessment Details\n";
                cout << "2. Assign Grade\n";
                cout << "3. Exit to Main Menu\n";

                cout << "Enter Your Choice: ";
                cin >> subchoice;

                switch (subchoice) {
                    case 1:
                        assessment.displayDetails();
                        break;

                    case 2:
                        cout << "Enter grade for assessment: ";
                        cin >> score;
                        assessment.assignGrade(score);
                        break;

                    case 3:
                        cout << "Returning to Main Menu...\n";
                        break;

                    default:
                        cout << "\nInvalid Choice. Try Again.\n";
                }
            } while (subchoice != 3);
            break;
        }

        case 8: {
            Certificate certificate("CERT123", "2024-12-07", "C++ Programming", "Haider");
            certificate.displayCertificate();
            break;
        }

        case 9: {
            Notification notification(1, "This is a test notification", "2024-12-07", {"haider@gmail.com"});
            notification.displayNotification();
            break;
        }

        case 10: {
            Group group(1, "Group 1");
            int groupID;
            string studentName;

            do {
                cout << "\n--- Manage Groups ---\n";
                cout << "1. Display Group Members\n";
                cout << "2. Add Member to Group\n";
                cout << "3. Remove Member from Group\n";
                cout << "4. Initiate Group Discussion\n";
                cout << "5. Exit to Main Menu\n";

                cout << "Enter Your Choice: ";
                cin >> subchoice;

                switch (subchoice) {
                    case 1:
                        cout << "Enter group ID: ";
                        cin >> groupID;
                        group.displayGroupMembers(groupID);
                        break;

                    case 2:
                        cout << "Enter student name: ";
                        cin.ignore();
                        getline(cin, studentName);
                        cout << "Enter group ID: ";
                        cin >> groupID;
                        group.addMemberToGroup(groupID, new Student(1, studentName, "", 0, ""));
                        break;

                    case 3:
                        cout << "Enter student name: ";
                        cin.ignore();
                        getline(cin, studentName);
                        cout << "Enter group ID: ";
                        cin >> groupID;
                        group.removeMemberFromGroup(groupID, new Student(1, studentName, "", 0, ""));
                        break;

                    case 4:
                    {
                        cout << "Enter group ID: ";
                        cin >> groupID;
                        cout << "Enter discussion topic: ";
                        cin.ignore();
                        string topic;
                        getline(cin, topic);
                        group.initiateDiscussion(groupID, topic);
                        break;
                    }

                    case 5:
                        cout << "Returning to Main Menu...\n";
                        break;

                    default:
                        cout << "\nInvalid Choice. Try Again.\n";
                }
            } while (subchoice != 5);
            break;
        }

        case 11:
            cout << "Exiting the Program...\n";
            break;

        default:
            cout << "\nInvalid Choice. Try Again.\n";
        }
    } while (choice != 11);

    return 0;
}
