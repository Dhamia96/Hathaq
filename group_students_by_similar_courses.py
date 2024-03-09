import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os 

class group_students_by_similar_courses:
  def __init__(self,studentID) -> None:
    # Read student information from the CSV file
    relative_path = r"datasets"
    students_info_path = os.path.join(relative_path, "students_info.csv")
    # Read data files
    self.students_info = pd.read_csv(students_info_path, encoding='utf-8')
    self.studentID= studentID


  def data_processing(self):
    # Create a list of all unique expected_skills
    unique_skills = list(set().union(*self.students_info['expected_skills']))
    # Create CountVectorizer and fit it on the unique_skills
    vectorizer = CountVectorizer(vocabulary=unique_skills)
    # Vectorize the skills for each student
    student_skills = []
    for skills in self.students_info['expected_skills']:
        skills_text = ', '.join(skills)
        student_skills.append(skills_text)
    vectorized_skills = vectorizer.transform(student_skills)
    # Create a pivot table
    pivot_table = pd.DataFrame(vectorized_skills.toarray(), index=self.students_info['student_id'], columns=unique_skills)
    # Calculate cosine similarity matrix
    cosine_sim = cosine_similarity(pivot_table)
    return pivot_table, cosine_sim

  def find_similar_students(self, top_n):
      pivot_table, cosine_sim= self.data_processing()

      if self.studentID not in pivot_table.index: #REMOVE THIS AFTER CREATING LOGIN PAGE AND SEND USER ID DYNAMICALLY 
        raise ValueError("Invalid student ID. Please provide a valid student ID.") #REMOVE THIS AFTER CREATING LOGIN PAGE AND SEND USER ID DYNAMICALLY 
      # Get the index position of the student_id
      student_index = pivot_table.index.get_loc(self.studentID)

      # Get the similarity scores for the student
      similarity_scores = list(enumerate(cosine_sim[student_index]))

      # Sort the similarity scores in descending order
      similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

      # Get the top similar students (excluding the student itself)
      similar_students_index = [similarity_scores[i][0] for i in range(1, top_n+1)]
      similar_students= []
      for similr_student in similar_students_index:
        similar_students.append(pivot_table.index[similr_student])

      return similar_students

#EXAMPLE USAGE
student_id= 396
max_students=4

# Initialize an instance of the 'group_students_by_similar_courses' class
connector= group_students_by_similar_courses(student_id)
# Find similar students for the given student ID
recommended_students_group = connector.find_similar_students(max_students )
print(f"your ID: {student_id}.\n I suggest you to create a group with the following students: {recommended_students_group} to discuss your current course and sharing your questions and ideas")