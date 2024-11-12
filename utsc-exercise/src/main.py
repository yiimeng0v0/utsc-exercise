import pandas as pd
import streamlit as st
import sqlite3
import sqlalchemy

def get_employee_dataframe():
    db_connection = sqlite3.connect('./db/utsc-exercise.db')
    employee_salary_df = pd.read_sql("""SELECT e.*, s.YearlyCompensation, cm.Country, e.FirstName + ' ' + e.LastName as FullName
                                                FROM EMPLOYEE e 
                                                LEFT JOIN Salary s ON e.EmployeeId = s.EmployeeId
                                                LEFT JOIN OfficeCountryMapping cm ON cm.OfficeId = e.OfficeId
                                            """, db_connection)
    db_connection.close()
    return employee_salary_df

def get_num_employees():
    db_engine = sqlalchemy.create_engine(f"sqlite:///db/utsc-exercise.db")
    db_connection = db_engine.connect()
    # Execute the distinct count query
    result = db_connection.execute(sqlalchemy.text("SELECT COUNT(DISTINCT EMPLOYEEID) FROM EMPLOYEE"))
    distinct_employee_count = result.scalar()
    db_connection.close()
    return distinct_employee_count



def get_avg_salary_by_job_title(employee_salary_df: pd.DataFrame, selected_titles: list):
    """Creates the multi-select filter widget to select job titles, and creates the graph that displays
    average salary by job title.
    """
    # Filter the dataframe based on selected job titles
    filtered_df = employee_salary_df[employee_salary_df['JobTitle'].isin(selected_titles)]

    # Group by JobTitle and calculate the average salary
    avg_salary_by_job_title = filtered_df.groupby('JobTitle')['YearlyCompensation'].mean().reset_index()
    
    #Plot the graph
    st.subheader("Average Salary by Job Title")
    st.bar_chart(avg_salary_by_job_title, x = 'JobTitle', y = 'YearlyCompensation')


#TODO: MAKE THIS USING THE MODEL FUNCTION ABOVE (Copy pasting is your friend here)
# HINT: The country column in the dataframe is 'Country'
def get_avg_salary_by_country(employee_salary_df: pd.DataFrame, selected_countries: list):
    # Filter the dataframe based on selected country
    filtered_df = employee_salary_df[employee_salary_df['Country'].isin(selected_countries)]
 
    # Group by country and calculate the average salary
    avg_salary_by_country = filtered_df.groupby('Country')['YearlyCompensation'].mean().reset_index()
    avg_salary_by_country.columns = ['Country', 'YearlyCompensation']
    #Plot the graph
    st.subheader("Average Salary by Country")
    st.bar_chart(avg_salary_by_country, x = 'Country', y = 'YearlyCompensation')


#TODO: MAKE THIS USING THE MODEL FUNCTION ABOVE (Copy pasting is your friend here)
def get_num_employees_by_country(employee_salary_df: pd.DataFrame, selected_countries: list):
    # Filter the dataframe based on selected job titles
    filtered_df = employee_salary_df[employee_salary_df['Country'].isin(selected_countries)]
    print(filtered_df)
    # Group by country and calculate the num
    num_employees_by_country = filtered_df.groupby('Country')['EmployeeId'].count().reset_index(name='NumEmployees')
    
    #Plot the graph
    st.subheader("Numbers of Employees by Country")
    st.bar_chart(num_employees_by_country, x = 'Country', y = 'NumEmployees')
  

#TODO: MAKE THIS USING THE MODEL FUNCTION ABOVE (Copy pasting is your friend here)
def get_num_employees_by_job_title(employee_salary_df: pd.DataFrame, selected_titles: list):
    filtered_df = employee_salary_df[employee_salary_df['JobTitle'].isin(selected_titles)]
    num_employees_by_job_title = filtered_df.groupby('JobTitle')['EmployeeId'].count().reset_index(name='NumEmployees')
    st.subheader("Number of Employees by Job Title")
    st.bar_chart(num_employees_by_job_title, x = 'JobTitle', y ='NumEmployees')
  

if __name__ == '__main__':
    # Streamlit app title
    st.title('Employee Salary Analysis')

    num_employees = get_num_employees()
    st.write(f"Total number of employees = {num_employees}")

    #Employee DataFrame
    employee_salary_df = get_employee_dataframe()

    # Get unique job titles from the dataframe and make a multiselect filter for them
    job_titles = employee_salary_df['JobTitle'].unique()
    selected_titles = st.multiselect('Select Job Title', job_titles, default=job_titles)
    
    #Avg salary by job title graph
    get_avg_salary_by_job_title(employee_salary_df, selected_titles)
    
    #Number of employees by job title graph
    get_num_employees_by_job_title(employee_salary_df, selected_titles )

    # Get unique contries from the dataframe and make a multiselect filter for them
    countries = employee_salary_df['Country'].unique()
    selected_countries = st.multiselect('Select Countries', countries, default=countries)

    #Avg salary by country graph
    get_avg_salary_by_country(employee_salary_df, selected_countries)

    #Number of employees by country graph
    get_num_employees_by_country(employee_salary_df, selected_countries)
