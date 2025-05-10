# Calendar Application 

A comprehensive calendar application designed to help users manage various types of events, such as meetings, appointments, and birthdays. This project demonstrates key Object-Oriented Programming (OOP) concepts including:

- **Classes and Objects**
- **Constructor Chaining**
- **Deep Copy Constructors**
- **Encapsulation**
- **Inheritance**
- **Abstract Classes**
- **Interfaces**
- **Method Overriding**
- **Polymorphism**

  The application allows users to create, share, and receive notifications for events, making it a robust tool for personal and collaborative scheduling.

## Key Concepts Demonstrated

![UML](https://github.com/SuzyAdel/CalenderAPP/assets/128175020/c1e8b476-da5b-4ddc-b903-218b58977866)

### Inheritance
- **Event** is an abstract class extended by **Meeting**, **Appointment**, and **Birthday**.

### Polymorphism
- The `addReminder` method in **Event** is overridden by the subclasses.

### Encapsulation
- Attributes are private or protected, accessed via public getter and setter methods.

### Deep Copy Constructors
- Ensures independent copies of objects for **User**, **Calendar**, **Event**, **Meeting**, **Appointment**, **Birthday**, and **Reminder**.

### Interfaces
- The **Notifiable** interface is implemented by **User**.

## Class Overview

### 1. CalendarMain
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/8b0e4892-6cd6-479c-b54a-1c649e796ac7" alt="CalenderMain" width="200">

- **Purpose**: Entry point of the application.
- **Description**: Initializes the application by creating users, calendars, events, and reminders. Demonstrates polymorphism by processing different types of events.

### 2. User
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/f13a47b3-8b37-4511-93f5-fa2be65567b7" alt="User" width="200">

- **Purpose**: Represents a user of the calendar application.
- **Description**: Contains user details and a list of calendars owned by the user. Implements the **Notifiable** interface to receive notifications. Supports deep copying.
- **Attributes**: `userId`, `name`, `calendars`
- **Methods**: `addCalendar`, `sendNotification`, deep copy constructor, and standard getters and setters.

### 3. Calendar
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/baed482d-c993-4341-beb6-463d3abeceda" alt="Calender" width="200">

- **Purpose**: Represents a calendar that can hold various events and be shared with other users.
- **Description**: Contains calendar details, a list of events, and a list of users with whom the calendar is shared. Supports deep copying.
- **Attributes**: `calendarId`, `name`, `owner`, `events`, `sharedWith`
- **Methods**: `addEvent`, `shareWith`, deep copy constructor, and standard getters and setters.

### 4. Event
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/074638d1-4466-4b4c-bc3f-430be1e90c22" alt="Event" width="200">

- **Purpose**: Abstract base class for different types of events.
- **Description**: Defines common properties and methods for events, such as ID, title, description, date, time, location, and reminders. Includes an abstract method `addReminder` and a deep copy constructor.
- **Attributes**: `eventId`, `title`, `description`, `date`, `time`, `location`, `reminders`
- **Methods**: Abstract method `addReminder`, deep copy constructor, and standard getters and setters.

### 5. Meeting
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/48c00e5d-cd18-4218-82b1-84bee17c77b2" alt="Meeting" width="200">

- **Purpose**: Represents a meeting event.
- **Description**: Extends **Event** and includes a list of participants. Implements the `addReminder` method and provides functionality to add participants. Supports deep copying.
- **Attributes**: `participants` (list of User)
- **Methods**: `addParticipant`, `addReminder`, deep copy constructor, and standard getters and setters.

### 6. Appointment
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/b0323d4e-c42e-4154-87a9-3d35e35b0087" alt="Appointment" width="200">

- **Purpose**: Represents an appointment event.
- **Description**: Extends **Event** and includes details about the doctor. Implements the `addReminder` method and supports deep copying.
- **Attributes**: `doctor`
- **Methods**: `addReminder`, deep copy constructor, and standard getters and setters.

### 7. Birthday
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/2ae35e35-322d-4d67-83b1-702a3a7691ce" alt="Birthday" width="200">

- **Purpose**: Represents a birthday event.
- **Description**: Extends **Event** and includes the name of the person whose birthday is being celebrated. Implements the `addReminder` method and supports deep copying.
- **Attributes**: `personName`
- **Methods**: `addReminder`, deep copy constructor, and standard getters and setters.

### 8. Reminder
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/fb0b839a-b1b5-4158-9718-10fcae5e5c48" alt="Reminder" width="200">

- **Purpose**: Represents a reminder for an event.
- **Description**: Contains reminder details such as ID, time, and message. Supports deep copying.

### 9. CalendarApp
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/e08b66f2-ba19-4ff4-bb65-ea1d0654d91f" alt="CalenderApp UML" width="200">

- **Purpose**: Represents the calendar application with a user.
- **Description**: Provides a structure to hold the user of the application, facilitating access to user-related operations.
- **Attributes**: `user`
- **Methods**: `getUser`, `setUser`

### 10. Notifiable
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/a787a78b-4c25-491c-a67d-efa2e922a019" alt="Notifiable" width="200">

- **Purpose**: Interface to provide notification functionality.
- **Description**: Defines a method `sendNotification` for sending notifications, which is implemented by the **User** class to receive event reminders.
- **Methods**: `sendNotification`

## Calendar Application GUI

### Overview
The Calendar Application GUI provides a user-friendly interface to manage and add different types of events such as appointments, meetings, and birthdays.

![CalenderApp GUI](https://github.com/SuzyAdel/CalenderAPP/assets/128175020/231609aa-f677-44d2-9a93-95693d43d1ab)

### Features

#### 1. Year and Month Selection
![dd momth](https://github.com/SuzyAdel/CalenderAPP/assets/128175020/7f8936ba-6440-4b88-95ce-77388202061a)

- **Dropdown Menu**: Users can select the desired year and month using dropdown menus at the top of the calendar interface.
- **Navigation**: Allows for easy navigation to view and manage events across different months and years.

#### 2. Event Addition
![addev dd](https://github.com/SuzyAdel/CalenderAPP/assets/128175020/38cfdb22-acd9-463b-9880-611f14ec4c7f)

- **Event Type Dropdown**: Users can choose the type of event (Appointment, Meeting, Birthday) from a dropdown list.
- **Input Fields**: Based on the selected event type, the interface provides specific input fields:
  - **Title**: A text box to enter the event title.
  - **Description**: A text box to enter a description of the event.
  - **Time**: A text box to specify the time of the event.
  - **Location**: A text box to specify the location of the event.
  - **Participants**: (Only for Meetings) A text box or list to add participants.
  - **Doctor**: (Only for Appointments) A field to specify the doctor's name.
  - **Person Name**: (Only for Birthdays) A field to specify the name of the person whose birthday it is.
- **Add Button**: After filling in the required details, users can click the "Add" button to save the event.

#### 3. Event Visualization
<img src="https://github.com/SuzyAdel/CalenderAPP/assets/128175020/64ea84bc-80d6-4b45-b170-091751755529" alt="Event Visualization" width="550">

- **Color Coding**: Each type of event is color-coded for easy differentiation on the calendar:
  - **Yellow**: For Birthdays
  - **Green**: For Appointments
  - **Blue**: For Meetings
- **Shading**: The days on the calendar are shaded with the corresponding color when an event is added, providing a quick visual representation of scheduled events.

## Example Usage in CalendarMain

The `CalendarMain` class demonstrates how to use the calendar application:

- **Create Users and Calendars**: A user named Alice is created with a work calendar.
- **Add Events**: Different types of events (meeting, appointment, birthday) are added to the calendar.
- **Add Reminders**: Reminders are added to events to notify users.
- **Share Calendars**: The calendar is shared with another user, Bob.
- **Process Events**: Events are processed to demonstrate polymorphism by checking the event type and displaying specific information about the event.

This example highlights the creation and management of events, the use of deep copying to ensure data integrity, and the implementation of polymorphic behavior to handle different event types dynamically.

Creators: Suzy , Menna , Ziad 
