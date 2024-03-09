import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
class ConnectingStudentsWithPostedJobs:

    def __init__(self, studentID):
        relative_path = r"datasets"
        students_info_path = os.path.join(relative_path, "students_info.csv")
        jobs_info_path = os.path.join(relative_path, "jobs_info.csv")
        # Read data files
        self.jobs_info = pd.read_csv(jobs_info_path, encoding='utf-8')
        self.students_info = pd.read_csv(students_info_path, encoding='utf-8')
    
        self.studentID = studentID

    def processing_data_pipeline(self):
        '''
        This function processes a list of texts and performs several data cleaning and tokenization steps.
        '''
        ar_stop_words_path= os.path.join(r"nlp", 'arabic-stop-words.txt')
        file = open(ar_stop_words_path, encoding='utf-8') #reads arabic stop words file
        ar_stop_words = file.read()
        file.close()
        texts = self.jobs_info['required_skills']
        # Initialize a list to store tokens for all rows
        all_tokens=[]

        for text in texts:
          #remove tashkeel
          text=re.sub(u'[\u064e\u064f\u0650\u0651\u0652\u064c\u064b\u064d\u0640\ufc62]','',text)

          # Remove stop words in Arabic
          cleaned_text = ' '.join(word for word in text.split() if word not in ar_stop_words)

          # Remove stop words in English
          en_stop_words = "and the"
          cleaned_text = ' '.join(word for word in cleaned_text.split() if word not in en_stop_words)

          # Convert English letters to lowercase
          converted_text = re.sub(r'\b\w+\b', lambda match: match.group().lower(), cleaned_text)

          standardized_text = re.sub(r'(\w+)\s+(\d+)', r'\1\2', converted_text)

          # Remove punctuation marks
          rm_punctuation = re.sub(r'[^\w\s\d]', '', standardized_text)

          # Remove non-Arabic and non-English letters
          rm_non_ar_en = re.sub(r'[^\u0600-\u06FF\u0750-\u077Fa-zA-Z\s\d]', '', rm_punctuation)

          # Split arabic phrase into individual words
          words = rm_non_ar_en.split()

          # Initialize the list of tokens for the current row
          tokens = []

          # Iterate through the words
          i = 0
          while i < len(words):
              current_word = words[i]

          # Check if the current word is a noun
              if not current_word.startswith('ال') and i < len(words) - 1:
                    next_word = words[i + 1]

                    if next_word.startswith('ال'):
                    
                        # Combine the current word and the following word
                        combined_token = current_word + ' ' + next_word
                        tokens.append(combined_token)
                        i += 2
                        continue

              # Add the current word as a separate token
              tokens.append(current_word)
              i += 1
          all_tokens.append(tokens)
          #pattern = r'\b\w+\b'
          #all_tokens = re.findall(pattern, rm_non_ar_en)

        self.jobs_info['required_skills_tokens']= all_tokens
        #return all_tokens

    def recommend_students_for_jobs(self, num_recommended_job):

        self.processing_data_pipeline()

        if self.studentID not in self.students_info['student_id']: #REMOVE THIS AFTER CREATING LOGIN PAGE AND SEND USER ID DYNAMICALLY 
            raise ValueError("Invalid student ID. Please provide a valid student ID.") #REMOVE THIS AFTER CREATING LOGIN PAGE AND SEND USER ID DYNAMICALLY 

        vectorizer = CountVectorizer()
        
        job_skills = vectorizer.fit_transform(self.jobs_info['required_skills_tokens'].astype(str))

        #concatenate the current student's skills (skills) with the student expected skills (expected_skills)
        self.students_info['combined_skills'] = self.students_info['skills'].astype(str) + ' ' + self.students_info['expected_skills'].astype(str)
        student_skills = vectorizer.transform(self.students_info['combined_skills'].astype(str))

        similarity_matrix = cosine_similarity(job_skills, student_skills)*100
        
        self.students_info.drop('combined_skills', axis=1, inplace=True)

        similarity_scores = pd.DataFrame(similarity_matrix, columns=self.students_info['student_id'])
        similarity_scores.index = self.jobs_info['job_id']
        #return similarity_scores
        recommended_jobs=[]
        top_similarities = similarity_scores[self.studentID].nlargest(num_recommended_job)
        for job_id, similarity in top_similarities.items():
            job_record = self.jobs_info.loc[self.jobs_info['job_id'] == job_id]
            if similarity > 0:
                recommended_jobs.append((job_record, similarity))

        # Display recommended_jobs or error message
        if len(recommended_jobs) == 0:
            print("Sorry! We couldn't find a job for you.")
            print("Try to take more courses and gain new skills to find suitable job offers.")
        else:
        # Display recommended_jobs
            print("Recommended Jobs:")
            for job_record, similarity in recommended_jobs:
                print("Student ID:", self.studentID)
                print("Job ID:", job_record['job_id'].values[0])
                print("Job Title:", job_record['job_title'].values[0])
                print("Company Name:", job_record['company_name'].values[0])
                print(f"Jobs Similarity Score To Your Skills:{similarity :.2f}%")
                print("-" * 30)
        #return recommended_jobs
                
#USAGE EXAMPLE
studentID= 396  #THIS VALUE COMES FROM USER INPUT(PASSED DYNAMICALLY) 
num_recommended_job=2
connector = ConnectingStudentsWithPostedJobs(studentID)
recommended_jobs = connector.recommend_students_for_jobs(num_recommended_job)
print(recommended_jobs)