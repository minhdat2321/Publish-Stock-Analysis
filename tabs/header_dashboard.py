import streamlit as st
import numpy as np
import pandas as pd
import fmpsdk

def header_chart(df_final, company_dt, tick = "AAPL"):
    # Specify the path to the Markdown file




    t1,t2,t6,t3,t4,t5 = st.columns([0.5,1,1,1,1,1])
    t1.image(str(company_dt['image'].values[0]), width = 120)
    t2.subheader(str(company_dt['companyName'].values[0]))
    t2.metric(label=f":blue[{company_dt['exchangeShortName'].values[0]}]",value=f"$ {company_dt['price'].values[0]}",delta= company_dt['changes'].values[0], delta_color='normal',)

    mkc1,mkc2 = t3.columns([1,1])
    mkc1.markdown("**Market Cap**")
    mkc1.markdown("**Volume Average**")

    mkc1.markdown("**Beta**")
    mkc1.markdown("**P/E**")
    mkc1.markdown("**P/B**")

    mkc2.markdown(f"{round(company_dt['mktCap'].values[0]/1000_000_000,ndigits=4)}B")
    mkc2.markdown(f"{round(company_dt['volAvg'].values[0]/1000_000,ndigits=4)}M")
    mkc2.markdown(company_dt['beta'].values[0])
    mkc2.markdown(f"{round(df_final['priceEarningsRatio'].values[0],ndigits=4)}")
    mkc2.markdown(f"{round(df_final['priceToBookRatio'].values[0],ndigits=4)}")


    ttm1,ttm2 = t4.columns([0.5,0.7])
    ttm1.markdown("**Dividend Yield**")
    ttm1.markdown("**PEG**")
    ttm1.markdown("**P/E(TTM)**")
    ttm1.markdown("**P/B(TTM)**")

    ttm2.markdown(f"{round(df_final['dividendYield'].values[0]*100,ndigits=4)}%")
    ttm2.markdown(f"{round(df_final['priceEarningsToGrowthRatio'].values[0],ndigits=4)}")
    ttm2.markdown(f"{round(df_final['peRatioTTM'].values[-1],ndigits=4)}")
    ttm2.markdown(f"{round(df_final['priceToBookRatioTTM'].values[-1],ndigits=4)}")


    in1,in2 = t5.columns([0.5,1])

    in1.markdown("**Sector**")
    in1.markdown("**Website**")

    
    in2.markdown(company_dt['sector'].values[0])
    in2.markdown(company_dt['website'].values[0])



    aa1, aa2 = t6.columns([1, 1])
    with aa1:
    
        for name in ['Business', 'Product','Competitors']:
            file_path = f"E:/Economic Vault/Economic/Micro/Company/{tick}/{name}.md"
            
            try:
                # Read the Markdown file
                with open(file_path, 'r', encoding='utf-8') as file:
                    md_content = file.read()
                st.button(name, use_container_width=True, help=md_content)
            except (FileNotFoundError, UnboundLocalError):
                pass

    with aa2:
    
        for name in [ 'Input', 'Output', 'Risk factors']:
            file_path = f"E:/Economic Vault/Economic/Micro/Company/{tick}/{name}.md"
            
            try:
                # Read the Markdown file
                with open(file_path, 'r', encoding='utf-8') as file:
                    md_content = file.read()
                
                
                st.button(name, use_container_width=True, help=md_content)
                no_data = False
            except (FileNotFoundError, UnboundLocalError):
                no_data = True
                pass
    if no_data is True:
    
        with t6:
            st.button("Overview",help=str(company_dt['description'].values[0]).replace(". ",'. \n - '), use_container_width=True)
            no_data = None