Requirements:
(Staff) Log hours for student
(Student) Request confirmation of hours (by staff)
View Student Leaderboard
(Student) View accolades (10/25/50 hours milestones)

My interpretation:
To me the system seemed like one where students would request their confirmation of hours by submitting the form to the staff and the staff would log the hours by confirming or rejecting the request. If confirmed, it would update the leaderboard and allow students to view the leaderboard and access their total hours there. Staff would also just be able to give an award using the command. Most of my commands use {student_id} as a parameter as the assignment did not specify any need to implement current user logic since the entire thing is just cli and not the web interface. For that reason i also just used the base user model and had staff and student inherit it.

Student Commands:
flask student create {name} {email} {password} {programme} - creates a student account with the information detailed
flask student add_record {student_id} {hours} - creates a student record for the student specified depicting how many hours were volunteered
flask student leaderboard {n} - shows student leaderboard for the top n students detailing the total hours volunteered by each student, n can be left out for a default of 3 students.
flask student my_position {student_id} - allows a student to search the leaderboard for their listing to find total hours and position held.
flask student my_accolades {student_id} - shows accolades for student specified.

Staff Commands:
flask staff create {name} {email} {password} {department} - creates a staff account with the information detailed.
flask staff list_pending - shows a list of all pending records for confirmation/rejection.
flask staff list_all - shows a list of all records.
flask staff confirm_record {record_id} - confirms the record of specified ID and updates the leaderboard accordingly.
flask staff reject_record {record_id} - rejects the record of specified ID.
flask staff give_award {student_id} {accolade_tier} - bestows an award to a student of tier 1, 2 or 3. Eligibility is determined by hours volunteered and is caluclated by the system.
