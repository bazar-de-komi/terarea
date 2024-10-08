import React from "react";
import { View, Text, StyleSheet, Image, ScrollView} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput/CustomerInput";
import AppletBox from "../../components/AppletsBox/appletBox";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import ProfilLogo from '../../../assets/profilLogo.png';

const Home = () => {
    const Navigation = useNavigation();
    const loginPressed = () => {
        Navigation.navigate("Sign In");
    }
    const allScreens = () => {
        Navigation.navigate("Sign In");
    }
    const appletsScreens = () => {
        Navigation.navigate("Sign In");
    }

    const servicesSreens = () => {
        Navigation.navigate("Sign In");
    }
    return (
        <ScrollView showsVerticalScrollIndicator={false}>
        {/* <View style={styles.bgNewForgotPass}> */}
            <View style={styles.headerContainer}>
                <Image
                    source={AreaLogo}
                    style={styles.areaLogo}
                />
                <Image
                    source={ProfilLogo}
                    style={styles.profilLogo}
                />
                </View>
                    <Text style={styles.homeTitle}>Explore</Text>
                    <View style={styles.homeNavigation}>
                        <CustomerButton
                        text="All"
                        onPress={allScreens}
                        type="TERTIARY"
                        bgColor={""}
                        fgColor={""}
                        />
                        <CustomerButton
                        text="Applets"
                        onPress={appletsScreens}
                        type="TERTIARY"
                        bgColor={""}
                        fgColor={""}
                        />
                        <CustomerButton
                        text="Services"
                        onPress={servicesSreens}
                        type="TERTIARY"
                        bgColor={""}
                        fgColor={""}
                        />
                    </View>
                    <View style={styles.searchBar}>
                        <CustomerInput
                        placeholder="Search Applets or Services"
                        />
                    </View>
                        <AppletBox
                        title="How we auotmate tiktok"
                        description="Learn how to use"
                        bgColor="#f54242"
                        />
                    {/* <CustomerInput
                    placeholder="Enter your new password"
                    value={newPassword}
                    setValue={setNewPassword}
                    secureTextEntry={false}
                    /> */}
                    {/* <View style={styles.appletBox}>
                        <CustomerButton
                        text="Back to Sign in"
                        onPress={loginPressed}
                        type="PRIMARY"
                        bgColor={""}
                        fgColor={""}
                        />
                    </View> */}
                    <CustomerButton
                    text="Back to Sign in"
                    onPress={loginPressed}
                    type="TERTIARY"
                    bgColor={""}
                    fgColor={""}
                    />
        
                {/* </View> */}
    </ScrollView>
    )
}

const styles = StyleSheet.create({
    // bgNewForgotPass: {
    //     top: 10,
    //     // marginTop: 20,
    //     justifyContent: 'center',
    //     alignItems: 'center',
    //     padding: 20,
    //     backgroundColor: '#F5F5F5',
    // },
    headerContainer: {
        marginTop: 30,
        backgroundColor: '#e0d8d7',
        borderRadius: 10,
        alignItems: 'center',
        padding: 5,
    },
    areaLogo: {
        // maxWidth: 110,
        maxHeight: 50,
        marginTop: 10,
        marginLeft: -250,
    },
    profilLogo: {
        // maxWidth: 100,
        maxHeight: 50,
        marginTop: -50,
        marginLeft: 300,
    },
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
        marginLeft: 150,
        // alignItems: 'center',
    },
    homeNavigation: {
        flexDirection: 'row', // Arrange buttons in a row
        justifyContent: 'space-around', // Distribute buttons evenly
        alignItems: 'center', // Align items vertically centered
        marginBottom: 20,
    },
    searchBar: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
    appletBox: {
        width: '100%',
        maxWidth: 400,
        backgroundColor: '#e0d8d7',
        borderRadius: 15,
        alignItems: 'center',
        padding: 5,
    },
})

export default Home