import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
import pandas as pd
from ADRpy import atmospheres as at
from Functions import AtmosPropStd as std
import streamlit as st
import matplotlib.pyplot as plt

# st.set_option('deprecation.showPyplotGlobalUse', False)


with st.container(border=True):
    st.subheader("reynold number calculator")

    atmos= at.Atmosphere()

    alt= st.number_input("Altitude (m)",value= 500.0)
    
    velocity= st.number_input("v infinite (m/s)",value= 20.0)
    col_aa,col_bb= st.columns(2)
    with col_aa:
        chord= st.number_input("Wing chord (cm)",value=25)*0.01
    with col_bb:
        rho= atmos.airdens_kgpm3(alt)
        dyn_vis= std(alt,13)
        reynold_num= (rho*velocity*chord)/(dyn_vis)
        st.write('Reynold number = '+ str(round(reynold_num,2)))

with st.container():
    col_a,col_b= st.columns(2)
    with col_a:
        airfoil1= st.text_input('Aerofoil input',"naca4412",key='aerofoil1')
        airfoil2= st.text_input('Aerofoil input',"naca4415",key='aerofoil2')
    with col_b:
        airfoil3= st.text_input('Aerofoil input',"naca0009",key='aerofoil3')
        airfoil4= st.text_input('Aerofoil input',"e214",key='aerofoil4')

with st.container():
    col1,col2= st.columns(2)
    re_min= st.number_input('Reynold number',value=reynold_num,key='Re min',step=1.0) 
    with col1:
        alpha_min= st.number_input('Alpha min',value=-10,key='alpha min',step=1)
    with col2:
        alpha_max= st.number_input('Alpha max',value=18,key='alpha max',step=1)
        # re_max= st.number_input('Re max',value=int(1e8),key='Re max',step=1)

airfoil_array= [airfoil1,airfoil2,airfoil3,airfoil4]
af_array= [asb.Airfoil(airfoil_array[i]) for i in range(len(airfoil_array))]

with st.container():
    col_1,col_2= st.columns(2)
    with col_1:
        fig, ax = plt.subplots()
        st.pyplot(af_array[0].draw())
        fig, bx = plt.subplots()
        st.pyplot(af_array[1].draw())

    with col_2:
        fig, cx = plt.subplots()
        st.pyplot(af_array[2].draw())
        fig, dx = plt.subplots()
        st.pyplot(af_array[3].draw())

re = [re_min]
alpha= [float(i) for i in range(alpha_min,alpha_max+1,1)]
Alpha, Re = np.meshgrid(alpha, re)

aero_flattened_array=[]
aero_array=[]

for i in range(len(airfoil_array)):
    af=af_array[i]
    aero_flattened = af.get_aero_from_neuralfoil(
        alpha=Alpha.flatten(),
        Re=Re.flatten(),
        mach=0,
        model_size="xxxlarge",
    )
    aero_flattened_array.append(aero_flattened)
    Aero = {
        key: value.reshape(Alpha.shape)
        for key, value in aero_flattened.items()
    }
    aero_array.append(Aero)

with st.container():    
    #Cl-CD
    fig, ax = plt.subplots()
    for i in range(len(aero_array)):
        line, = ax.plot(
                        aero_array[i]["CD"][0, :],
                        aero_array[i]["CL"][0, :],
                        label= f" {af_array[i].name} Airfoil\n"
                    )

    plt.xscale('log')
    plt.legend(loc='lower right')
    # plt.axhline(y = cl_value[2], linestyle = '-', label= "Cl cruise ideal") 
    # plt.axhline(y = cl_value[6], linestyle = '-', label= "Cl max clean") 
    a= p.show_plot(
                    title="$C_L$-$C_D$ Polar for Airfoil at RE = "+str(re_min),
                    ylabel="Drag Coefficient $C_L$",
                    xlabel="Lift Coefficient $C_D$",
            )

    st.pyplot(a)

    # #Cl-AoA
    # st.write(alpha)
    fig, bx = plt.subplots()
    for i in range(len(aero_array)):
        line, = bx.plot(
                            # aero_array[i]["CD"][0, :],
                            np.array(alpha),
                            np.array(aero_array[i]["CL"][0, :]),
                            label= f" {af_array[i].name} Airfoil\n"
                            # color=colors[0], alpha=0.8,
                        )

        # plt.xscale('log')
    plt.legend(loc='lower right')
    # plt.axhline(y = cl_value[2], linestyle = '-', label= "Cl cruise ideal") 
    # plt.axhline(y = cl_value[6], linestyle = '-', label= "Cl max clean") 
    b= p.show_plot(
                        title="$AoA$-$C_L$ Polar for Airfoil at RE = "+str(re_min),
                        xlabel="AoA",
                        ylabel="Lift Coefficient $C_L$",
                )

    st.pyplot(b)

    #Cd- AoA
    fig, cx = plt.subplots()
    for i in range(len(aero_array)):
        line, = cx.plot(
                            # aero_array[i]["CD"][0, :],
                            np.array(alpha),
                            np.array(aero_array[i]["CD"][0, :]),
                            label= f" {af_array[i].name} Airfoil\n"
                            # color=colors[0], alpha=0.8,
                        )

    # plt.xscale('log')
    plt.legend(loc='lower right')

    c= p.show_plot(
                        title="$AoA$-$C_D$ Polar for Airfoil at RE = "+str(re_min),
                        xlabel="AoA",
                        ylabel="Drag Coefficient $C_D$",
                )

    st.pyplot(c)

    #Cl/Cd - AoA
    fig, cx = plt.subplots()
    for i in range(len(aero_array)):
        line, = cx.plot(
                            # aero_array[i]["CD"][0, :],
                            np.array(alpha),
                            np.array(aero_array[i]["CL"][0, :]/aero_array[i]["CD"][0, :]),
                            label= f" {af_array[i].name} Airfoil\n"
                            # color=colors[0], alpha=0.8,
                        )

    # plt.xscale('log')
    plt.legend(loc='lower right')
    c= p.show_plot(
                        title="$AoA$ - $C_L / C_D$ Polar for Airfoil at RE = "+str(re_min),
                        xlabel="AoA",
                        ylabel="$C_L / C_D$",
                )

    st.pyplot(c)
    
    # with st.container(border=True):
    #  st.subheader('Airfoil requirements')
    #  st.dataframe(airfoil_requirements)