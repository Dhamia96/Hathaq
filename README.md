# Academic Platform with AI Technology (حذِق)

This project aims to develop an academic platform that leverages AI technology to enhance the learning experience and facilitate career development for students. The platform consists of three Python files, each serving a specific purpose.

## Connecting_student_with_jobs.py

The `Connecting_student_with_jobs.py` file utilizes natural language processing (NLP) techniques and cosine similarity to suggest customized job opportunities based on the user's current course. The primary goal of this file is to motivate students to complete their courses by showing them job recommendations that align with the skills acquired through their ongoing studies. By encouraging course completion, the platform helps students visualize the potential career paths that their courses can lead to.

## group_students_by_similar_courses.py

The `group_students_by_similar_courses.py` file employs cosine similarity to group students who are interested in acquiring specific skills. For instance, if student 'A' is taking a Data Analysis course and student 'B' is taking Statistics, they can be grouped together because both courses require shareable skills. The platform suggests forming study groups with students who are learning similar skills, fostering collaboration and knowledge exchange. Additionally, students with similar skill sets can participate in quizzes to compete and further enhance their understanding of the subject matter.

## prediction_script.py

The `prediction_script.py` file utilizes neural networks to predict a student's likelihood of successfully completing a particular course. The predictor tool has been trained to achieve an accuracy of over 75% in predicting course outcomes. If the predictor determines that a student has the potential to pass the course, the system sends the student recommended job opportunities as a means of motivation after course completion. Conversely, if the predictor predicts that a student may struggle to complete the course, it alerts the course creator or teacher. The teacher can then engage with the student to identify and address any obstacles to their success. Based on the student's current skills and abilities, the teacher can recommend suitable course that align with their capabilities.
