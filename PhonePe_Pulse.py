import mysql.connector as sql
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from PIL import Image

icon = Image.open("D:\\pythoncode\\Proj\\PhonePe_Project\\images\\logos.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By AJAY K",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by :blue**AJAY**!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})
st.sidebar.header(":wave: :violet[**Hello! *User..* Welcome to the dashboard**]")

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #5F259F;
        font-size: 46px;
        font-family: 'Arial', sans-serif;
        text-shadow: .2px 2px 4px ;
        padding: 20px;
        background-color: #f7f0f0;
        border-radius: 10px;
    }
    </style>
    <div class="title">
        PhonePe-Pulse Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")

mydb = sql.connect(
        host="localhost",
        user="root",
        password="",
        database="phonepe_pulse"
    )
cursor = mydb.cursor()

Agg_Trans = pd.read_csv("Agg_Trans.csv")
Agg_User = pd.read_csv("Agg_User.csv")
Map_Trans = pd.read_csv("map_trans.csv")
Map_User = pd.read_csv("map_user.csv")
Top_Trans = pd.read_csv("top_trans.csv")
Top_User = pd.read_csv("top_user.csv")
Top_User_Dist = pd.read_csv("top_user_district.csv")

#check here
def Aggre_trans_Y(df,year):
    aty= df[df["Year"] == year]
    aty.reset_index(drop= True, inplace= True)

    atyg=aty.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    atyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(atyg, x="State", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=400, height= 450, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(atyg, x="State", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=400, height= 450, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,_,col2 = st.columns([1,1,1], gap="large")
    with col1:
      fig_india_1= px.choropleth(atyg, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                 locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (atyg["Transaction_amount"].min(),atyg["Transaction_amount"].max()),
                                 hover_name= "State",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
      fig_india_1.update_geos(visible =False)
      st.plotly_chart(fig_india_1)
   
    with col2:
      fig_india_2= px.choropleth(atyg, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                 locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (atyg["Transaction_count"].min(),atyg["Transaction_count"].max()),
                                 hover_name= "State",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
      fig_india_2.update_geos(visible =False)
        
      st.plotly_chart(fig_india_2)

    return aty

def Aggre_trans_Y_Q(df,quarter):
    atyq= df[df["Quarter"] == quarter]
    atyq.reset_index(drop= True, inplace= True)

    atyqg=atyq.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    atyqg.reset_index(inplace= True)
    
    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(atyqg, x= "State", y= "Transaction_amount", 
                            title= f"{atyq['Year'].min()} AND {quarter} TRANSACTION AMOUNT",width=400, height= 450,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(atyqg, x= "State", y= "Transaction_count", 
                            title= f"{atyq['Year'].min()} AND {quarter} TRANSACTION COUNT",width=400, height= 450,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,_,col2 = st.columns([1,2,1], gap="large")
    with col1:
        fig_india_1= px.choropleth(atyqg, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                 locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (atyqg["Transaction_amount"].min(),atyqg["Transaction_amount"].max()),
                                 hover_name= "State",title = f"{quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2= px.choropleth(atyqg, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                 locations= "State", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (atyqg["Transaction_count"].min(),atyqg["Transaction_count"].max()),
                                 hover_name= "State",title = f"{quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    return atyq

def Aggre_Transaction_type(df,state):
    # df_state = df[df["State"]==state]
    # df_state.reset_index(drop= True, inplace= True)

    # agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    # agttg.reset_index(inplace= True)
    col1,_,col2= st.columns([1,1,1],gap="Large")
    with col1:

        fig_hbar_1= px.bar(df, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(df, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)

def Aggre_user_plot_1(df,year):
    aguy= df[df["Year"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("User_brand")["User_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="User_brand",y= "User_count", title=f"{year} BRANDS AND USER COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    aguq= df[df["Quater"] == quarter]
    aguq.reset_index(drop= True, inplace= True)
    fig_pie_1= px.pie(data_frame=aguq, names= "User_brand", values="User_count", hover_data= "User_percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.3, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return aguq

def Aggre_user_plot_3(df,state):
    agus= df[df["State"]==state]
    agus.reset_index(drop= True, inplace= True)
    
    agusg= pd.DataFrame(agus.groupby("User_brand")["User_count"].sum())
    agusg.reset_index(inplace= True)

    fig_scatter_1 = px.line(agusg,x="User_brand",y="User_count",markers=True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_trans_plot_1(df,state):
    mtys= df[df["State"] == state]
    mtysg= mtys.groupby("district")[["Transaction_count","Transaction_amount"]].sum()
    mtysg.reset_index(inplace= True)
    col1,col2= st.columns([2,1])
    with col1:
        fig_map_bar_1= px.bar(mtysg, x= "district", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(mtysg, x= "district", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.qualitative.Alphabet)
        
        st.plotly_chart(fig_map_bar_1)

def map_trans_plot_2(df,state):
    mtys= df[df["State"] == state]
    mtysg= mtys.groupby("district")[["Transaction_count","Transaction_amount"]].sum()
    mtysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(mtysg, names= "district", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(mtysg, names= "district", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_trans_plot_2p(df,state):
    mtys= df[df["State"] == state]
    mtysg= mtys.groupby("District_pincode")[["Transaction_count","Transaction_amount"]].sum()
    mtysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(mtysg, names= "District_pincode", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(mtysg, names= "District_pincode", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)
    
def map_user_plot_1(df, year):
    muy= df[df["Year"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("State")[["registeredUsers", "appOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "State", y= ["registeredUsers","appOpens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("State")[["registeredUsers", "appOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "State", y= ["registeredUsers","appOpens"], markers= True,
                                title= f"{df['Year'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["State"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("district")[["registeredUsers", "appOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "registeredUsers",y= "district",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "appOpens", y= "district",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tuy= df[df["Year"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["State","Quarter"])["registeredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "State", y= "registeredUsers", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["State"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["registeredUsers"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "registeredUsers",barmode= "group",
                           width=1000, height= 800,color= "registeredUsers",hover_data="district_pincode",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

def ques1():
    query = """
        SELECT User_brand, SUM(User_count) AS Total_Transaction_Count,round(Sum(User_percentage),2) AS Total_Transaction_Percentage
        FROM agg_user
        GROUP BY User_brand
        ORDER BY Total_Transaction_Count DESC;
        """
    brand2 = pd.read_sql(query, mydb)
    # area_trace = go.Scatter(
    #                             x=brand2["User_brand"],
    #                             y=brand2["Total_Transaction_Count"],
    #                             fill="tozeroy",
    #                             mode="lines+markers",
    #                             name="Area Trace with default `zorder` of 0",
    #                             line=dict(color="lightsteelblue"),
    #                         )

    # bar_trace = go.Bar(
    #     x=brand2["User_brand"],
    #     y=brand2["Total_Transaction_Percentage"],
    #     name="Bar Trace with `zorder` of 1",
    #     zorder=1,
    #     marker=dict(color="lightslategray"),
    # )

    # fig = go.Figure(data=[area_trace, bar_trace])
    # st.plotly_chart(fig)

    fig_brands = px.pie(brand2, values="Total_Transaction_Count", names="User_brand",
                    color_discrete_sequence=px.colors.sequential.dense_r,
                    title="Top Mobile Brands of Transaction_count")
    fig_brands2 = px.bar(
                            brand2,
                            x="User_brand",
                            y="Total_Transaction_Count",
                            color="User_brand",
                            color_discrete_sequence=px.colors.sequential.dense_r,
                            title="Top Mobile Brands by Transaction Count"
                        )
    st.plotly_chart(fig_brands2)
    st.plotly_chart(fig_brands)

def ques2():
    query = """
            SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount
        FROM agg_trans
        GROUP BY State
        ORDER BY Total_Transaction_Amount ASC
        LIMIT 10;"""
    top_states = pd.read_sql(query, mydb)
    fig_states = px.bar(top_states, x="State", y="Total_Transaction_Amount",
                         color="State",
                         color_discrete_sequence=px.colors.sequential.Plasma,
                         title="Lowest Transaction Amount by States")
    st.plotly_chart(fig_states)

def ques3():
    query = """
            SELECT District, SUM(Map_amount) AS Total_Transaction_Amount
            FROM map_trans
            GROUP BY District
            ORDER BY Total_Transaction_Amount DESC
            LIMIT 10;
        """
    top_dist = pd.read_sql(query, mydb)
    fig_dist = px.bar(top_dist, x="District", y="Total_Transaction_Amount",
                         color="District",
                         color_discrete_sequence=px.colors.sequential.Plasma,
                         title="Top 10 Districts by Transaction Amount")
    st.plotly_chart(fig_dist)

def ques4():
    query = """
            SELECT District, SUM(Map_amount) AS Total_Transaction_Amount
            FROM map_trans
            GROUP BY District
            ORDER BY Total_Transaction_Amount 
            LIMIT 10;
        """
    top_dist = pd.read_sql(query, mydb)
    fig_dist = px.bar(top_dist, x="District", y="Total_Transaction_Amount",
                         color="District",
                         color_discrete_sequence=px.colors.sequential.Plasma,
                         title="Top 10 Districts by Lowest Transaction Amount")
    st.plotly_chart(fig_dist)

def ques5():
    query ="""
    SELECT Quarter, AVG(Transaction_amount) AS Avg_Transaction_Amount,Year
    FROM agg_trans
    GROUP BY Quarter,year
    ORDER BY Year, Quarter;
    """
    quarter_performance = pd.read_sql(query, mydb)
    fig = px.bar(quarter_performance, x="Quarter",
    y="Avg_Transaction_Amount",
    color="Year",
    title="Average Transaction Amount by Quarter and Year" )
    st.plotly_chart(fig)

def ques6(year):
    query = f"""WITH RankedStates AS (
            SELECT 
                mu.State,
                mu.App_open,
                at.Transaction_count,
                ROW_NUMBER() OVER (PARTITION BY mu.State ORDER BY mu.App_open DESC) AS rn
            FROM 
                map_user mu
            JOIN 
                agg_trans at ON mu.State = at.State AND at.Year = {year} 
        )
        SELECT 
            State,
            App_open,
            Transaction_count
        FROM 
            RankedStates
        WHERE 
            rn = 1
        ORDER BY 
            App_open DESC
        LIMIT 10;
            """
    df = pd.read_sql(query, mydb)
    fig = px.bar(
            df,
            x="State",
            y="App_open",
            title=f"Top 10 States by App Opens in {year}",
            color="Transaction_count",
            labels={"App_open": "App Opens", "State": "State", "Transaction_count": "Transaction Count"},
            color_continuous_scale=px.colors.sequential.Viridis
        )
    st.plotly_chart(fig)
def ques7():
    query = """
    SELECT State,SUM(Transaction_count) AS Total_Transaction_Count
    FROM
        agg_trans
    GROUP BY
        State
    ORDER BY
        Total_Transaction_Count ASC
    LIMIT 10;
    """
    df = pd.read_sql(query, mydb)
    fig = px.pie(df, values="Total_Transaction_Count", names="State",
                 color_discrete_sequence=px.colors.sequential.Plasma,
                 title="Top States by Transaction Count")
    st.plotly_chart(fig)

def ques8():
    query = """
    SELECT State,SUM(Transaction_count) AS Total_Transaction_Count
    FROM
        agg_trans
    GROUP BY
        State
    ORDER BY
        Total_Transaction_Count DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, mydb)
    fig = px.pie(df, values="Total_Transaction_Count", names="State",
                 color_discrete_sequence=px.colors.sequential.Plasma,
                 title="Bottom States by Transaction Count")
    st.plotly_chart(fig)

def ques9():
    query = """
    SELECT State,SUM(Transaction_amount) AS Total_Transaction_Amount
    FROM
        agg_trans
    GROUP BY
        State
    ORDER BY
        Total_Transaction_Amount DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, mydb)
    fig = px.bar(df, x="State", y="Total_Transaction_Amount",
                 color="State",
                 color_discrete_sequence=px.colors.sequential.Plasma,
                 title="Top States by Total Transaction Amount")
    st.plotly_chart(fig)

def ques10():
    query = """
    SELECT District,SUM(Map_amount) AS Total_Transaction_Amount
    FROM
        map_trans
    GROUP BY
        District
    ORDER BY
        Total_Transaction_Amount ASC
    LIMIT 50;
    """
    df = pd.read_sql(query, mydb)
    fig = px.bar(df, x="District", y="Total_Transaction_Amount",
                 color="District",
                 color_discrete_sequence=px.colors.sequential.Plasma,
                 title="Top 50 Districts by Total Transaction Amount")
    st.plotly_chart(fig)



with st.sidebar:
   st.markdown("<br>",unsafe_allow_html=True)
   selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "6px", "--hover-color": "#8267E5"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
         
if selected == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian ***digital payments and financial technology*** company")
        st.subheader("****FEATURES****",divider='violet')
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.write("****EASY TRANSACTIONS****")
        st.write()
        
    with col2:
       st.markdown("<br>",unsafe_allow_html=True)
       st.markdown("<br>",unsafe_allow_html=True)
       st.image("D:\\pythoncode\\Proj\\PhonePe_Project\\images\\mockup.jpg")
       phonepe_playstore_url = "https://play.google.com/store/apps/details?id=com.phonepe.app"
       st.markdown(f'''<a href="{phonepe_playstore_url}" download>
        <button style="background-color: #5F259F; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 34px 52px; cursor: pointer;">DOWNLOAD THE APP NOW</button>
        </a>''', unsafe_allow_html=True)
        
    col3,col4= st.columns(2)
      
    with col3:
      st.markdown("<br>",unsafe_allow_html=True)
      st.markdown("<br>",unsafe_allow_html=True)
      st.video("images//phonepe-ad.mp4")

    col4.markdown('''
    <style>
    .left-padding {
        padding-left: 20px;
    }
    </style>
    <div class="left-padding">
        <p><b>Easy Transactions</p>
        <p><b>ne App For All Your Payments</p>
        <p><b>Your Bank Account Is All You Need</p>
        <p><b>Multiple Payment Modes</p>
        <p><b>PhonePe Merchants</p>
        <p><b>Multiple Ways To Pay</p>
        <pre><b><i>   1. Direct Transfer & More</pre>
        <pre><b><i>  2. QR Code</pre>
        <p><b>Earn Great Rewards</p>
    </div>
    ''', unsafe_allow_html=True)

    col5,col6 = st.columns(2)
    
    with col5:
      st.markdown(" ")
      st.markdown(" ")
      st.markdown(" ")
      st.markdown(" ")
      st.markdown(" ")
      st.markdown(" ")
      st.markdown(" ")
      st.markdown(" ")
      st.write("****No Wallet Top-Up Required****")
      st.write("****Pay Directly From Any Bank To Any Bank A/C****")
      st.write("****Instantly & Free****")
    
    with col6:
      st.video("D:\\pythoncode\\Proj\\PhonePe_Project\\images\\vid2.mp4")
      st.balloons()


if selected == "Explore Data":
   tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
   with tab1:
      method = st.radio("**Select the Analysis Method**",["**Transaction Analysis**", "**User Analysis**"])
      
      if method == "**Transaction Analysis**":
         col1,col2= st.columns(2)
         with col1:
            years_at= st.slider("**Select the Year**", Agg_Trans["Year"].min(), Agg_Trans["Year"].max(),Agg_Trans["Year"].min())
         df_agg_tran_Y= Aggre_trans_Y(Agg_Trans,years_at)
            
         col1,col2= st.columns(2)
         with col1:
            quarters_at= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

         df_agg_tran_Y_Q= Aggre_trans_Y_Q(df_agg_tran_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
         state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y_Q["State"].unique())

         Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)

      elif method == "**User Analysis**":
            year_au= st.selectbox("Select the Year_AU",Agg_User["Year"].unique())
            agg_user_Y= Aggre_user_plot_1(Agg_User,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quater"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["State"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)
   with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.slider("**Select the Year_mt**", Map_Trans["Year"].min(), Map_Trans["Year"].max(),Map_Trans["Year"].min())

            df_map_trans_Y= Aggre_trans_Y(Map_Trans,years_m1)
            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mt", df_map_trans_Y["State"].unique())

            map_trans_plot_1(df_map_trans_Y,state_m1)

            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.slider("**Select the Quarter_mt**", df_map_trans_Y["Quarter"].min(), df_map_trans_Y["Quarter"].max(),df_map_trans_Y["Quarter"].min())

            df_map_tran_Y_Q = Aggre_trans_Y_Q(df_map_trans_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["State"].unique())            
            
            map_trans_plot_2(df_map_tran_Y_Q, state_m4)

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",Map_User["Year"].unique())
            map_user_Y= map_user_plot_1(Map_User, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["State"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)
   with tab3:
    method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Transaction Analysis", "Top User Analysis"])
    if method_top == "Top Transaction Analysis":
        col1,col2= st.columns(2)
        with col1:
            years_t2= st.slider("**Select the Year_tt**", Top_Trans["Year"].min(), Top_Trans["Year"].max(),Top_Trans["Year"].min())

        df_top_tran_Y= Aggre_trans_Y(Top_Trans,years_t2)

        
        col1,col2= st.columns(2)
        with col1:
            quarters_t2= st.slider("**Select the Quarter_tt**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(),df_top_tran_Y["Quarter"].min())

        df_top_tran_Y_Q= Aggre_trans_Y_Q(df_top_tran_Y, quarters_t2)

        col1,col2= st.columns(2)
        with col1:
            state_m4= st.selectbox("**Select the State_miy**", df_top_tran_Y_Q["State"].unique())            
        map_trans_plot_2p(df_top_tran_Y_Q, state_m4)

    elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", Top_User["Year"].unique())

            df_top_user_Y= top_user_plot_1(Top_User,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["State"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)
if selected == "Top Charts":

    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Average Transaction Amount by Quarter and Year','Find the top 10 states by the number of app opens and their corresponding transaction counts for the current year',
                                  'States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    if ques == "Top Brands Of Mobiles Used":
        ques1()
    elif ques == "States With Lowest Trasaction Amount":
        ques2()
    elif ques == "Districts With Highest Transaction Amount":
        ques3()
    elif ques == "Top 10 Districts With Lowest Transaction Amount":
        ques4()
    elif ques == "Average Transaction Amount by Quarter and Year":
        ques5()
    elif ques == "Find the top 10 states by the number of app opens and their corresponding transaction counts for the current year":
        col1,col2= st.columns(2)
        with col1:
            years_at= st.slider("**Select the Year**", Map_User["Year"].min(), Map_User["Year"].max(),Map_User["Year"].min())
            ques6(years_at)

    elif ques == "States With Lowest Trasaction Count":
        ques7()
    elif ques == "States With Highest Trasaction Count":
        ques8()
    elif ques == "States With Highest Trasaction Amount":
        ques9()
    elif ques == "Top 50 Districts With Lowest Transaction Amount":
        ques10()
    

if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/AjayKarthekeyan/PhonePe_Pulse/")

    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("D:\\pythoncode\\Proj\\PhonePe_Project\\images\\col2.png")
        st.image("D:\\pythoncode\\Proj\\PhonePe_Project\\images\\col21.png")
        st.image("D:\\pythoncode\\Proj\\PhonePe_Project\\images\\col22.png")
        st.image("D:\\pythoncode\\Proj\\PhonePe_Project\\images\\col.png")