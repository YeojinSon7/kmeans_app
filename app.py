import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler # preprocessing 데이터 전처리
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
def main():
    st.title('K-Means 클러스터링 앱')

    # csv 파일 업록드
    csv_file = st.file_uploader('csv 파일 업로드', type = ['csv']) # type이 csv니까 csv아닌건 안올라간다

    if csv_file is not None:
        df = pd.read_csv(csv_file)
        st.dataframe(df)
        st.subheader('Nan 데이터 확인')
        st.dataframe(df.isna().sum())
        st.subheader('결측값 처리한 결과')
        df = df.dropna() 
        df.reset_index(inplace = True, drop= True)
        st.dataframe(df)
        st.subheader('클러스터링에 사용할 컬럼 선택')
        selected_columns = st.multiselect('x로 사용할 컬럼을 선택하세요.',df.columns)
        if len(selected_columns) != 0:
            X = df[selected_columns]
            st.dataframe(X) # y는 없다
            # 숫자로된 새로운 데이터프레임 만든다.
            X_new = pd.DataFrame()
            for name in X.columns :
                print(name)
                # 데이터가 문자열이면, 데이터의 종류가 몇개인지 확인한다.
                if X[ name ].dtype == object : # pandas 에서 문자열은 object로 나온다
                    if X[name].nunique() >= 3:
                    # 원핫 인코딩한다.
                        ct = ColumnTransformer([('encoder',OneHotEncoder(), [0])], remainder='passthrough')
                        col_names = sorted(X[name].unique())
                        X_new[col_names] = ct.fit_transform(X[name].to_frame())
                    else:
                    # 레이블 인코딩 한다.
                        label_encoder = LabelEncoder()
                        X_new[name]= label_encoder.fit_transform(X[name])
                # 숫자 데이터일때의 처리는 여기서
                else:
                    X_new[name] = X[name]
            st.subheader('문자열은 숫자로 바꿔줍니다.') 
            st.dataframe(X_new)
            st.subheader('피처 스케일링 합니다.')
            scaler = MinMaxScaler()
            X_new = scaler.fit_transform(X_new)
            st.dataframe(X_new)

            # 유저가 입력한 파일의 데이터 갯수를 세어서 해당 데이터의 갯수가 10보다 작으면, 데이터의 갯수가지만 wcss를 구하고 10보다 크면, 10개로 한다.

            if X_new.shape[0] < 10:# 결과는 튜플로 나온다 # 데이터의 갯수 구하기
                max_count = X_new.shape[0]
            else:
                max_count = 10
            wcss = []
            for k in range(1,max_count+1):
                kmeans = KMeans(n_clusters= k,random_state =5,n_init='auto') # n_init='auto' warning 안뜨게 하는거
                kmeans.fit(X_new)
                wcss.append(kmeans.inertia_)
            x = np.arange(1, max_count+1)
            fig = plt.figure()
            plt.plot(x,wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of Clusters')
            plt.ylabel('WCSS')
            st.pyplot(fig)

            st.subheader('클러스터링 갯수 선택')
            k = st.number_input('k를 선택',1,max_count,value=3) # value는 디폴트 값

            kmeans = KMeans(n_clusters=k, random_state=5, n_init='auto')
            y_pred = kmeans.fit_predict(X_new)
            df['Group'] = y_pred

            st.subheader('그루핑 정보 표시')
            st.dataframe(df)

            st.subheader('보고싶은 그룹을 선택!')
            group_number = st.number_input('그룹번호 선택',0,k-1)
            st.dataframe(df.loc[df['Group'] == group_number,])

            df.to_csv('result.csv',index=False) # 메모리에있는 df를 파일로 저장
if __name__ == '__main__' :
    main()