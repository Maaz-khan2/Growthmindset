import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title='Data Sweeper', layout='wide')

# custom css
st.markdown(
    '''
    <style>
    .stApp{
        background-color: black;
        color: white;
          }
        </style>
        ''',
        unsafe_allow_html=True
)

#title or discription
st.title('streamer integrator by Maaz khan')
st.write('streamer integrator and most beneficial')

#file uploader
uploaded_files = st.file_uploader('upload your files(accept csv or Excel):', type=['cvs','xlsx'], accept_multiple_files=(True))

if uploaded_files:
   for file in uploaded_files:
       file_ext = os.path.splitext(file.name)[-1].lower()

       if file_ext=='.cvs':
           df=pd.read_csv(file)
       elif file_ext== '.xlsx':
           df=pd.read_excel(file)
       else:
           st.error(f"unsupported file type:{file_ext}") 
           continue
   
       #file_details
       st.write('preview the head of dataframe')
       st.dataframe(df.head())

       # data cleaning option
       st.subheader('Data Cleaning Options')
       if st.checkbox(f'Clean data for {file.name}'):
         col1, col2 = st.columns(2)  # Fixed the assignment of columns
    
         with col1:
            if st.button(f"Remove duplicates from the file: {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write('Duplicates removed')  # Fixed spelling
    
         with col2:
            if st.button(f"Fill missing values for: {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write('Missing values filled')

       st.subheader('select column to keep')
       columns = st.multiselect(f'choose columns for{file.name}', df.columns , default=df.columns)
       df=df[columns]

            
       #data visualization
       st.subheader('Data Visualization')
       if st.checkbox(f"Show visualization: {file.name}"):
           st.bar_chart(df.select_dtypes(include=['number']))


       #Conversion Options
       st.subheader('Conversion Options')
       conversion_type = st.radio(f'convert{file.name} to:', ['cvs' , 'Excel'] , key=file.name)
       if st.button(f'convert{file.name}'):
           Buffer = BytesIO()
           if conversion_type == 'csv':    
               df.to.cvs(Buffer , index=False)
               file_name = file.name.replace(file_ext,'.csv')       
               mime_type = 'text/csv' 
         
           elif conversion_type == 'Excel':    
               df.to.to_excel(Buffer , index=False)
               file_name = file.name.replace(file_ext,'.xlsx')    
               mime_type = 'application/vnd.openxmlformates-officedocument'
           Buffer.seek(0) 
           
           st.download_button(
               label=f'Download {file.name} , {conversion_type}',             
               data=Buffer,
               file_name=file_name,
               mime=mime_type
           )

st.success(f'all files proccessed successfully')




           





   

     




