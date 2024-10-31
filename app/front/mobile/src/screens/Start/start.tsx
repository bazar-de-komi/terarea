import React from "react";
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import MenuIcon from '../../../assets/menuIcon.png';
import SignIn from "../Authentication/SignIn";

const Start = () => {
    const Navigation = useNavigation();

    const signIn = () => {
        Navigation.navigate('Sign In');
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.headerContainer}>
                <Image
                    source={AreaLogo}
                    style={styles.areaLogo}
                />
                <Image
                    source={MenuIcon}
                    style={styles.profilLogo}
                />
                <Text style={styles.homeTitle}>Automation for business and home</Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.title}>Save time and get more done</Text>
                <View style={styles.back}>
                    <CustomerButton
                        text="Start Today"
                        onPress={signIn}
                        type="PRIMARY"
                        bgColor={""}
                        fgColor={""}
                    />
                </View>
            </View>
            <Text style={styles.homeTitle}>Get started with any Applet</Text>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    headerContainer: {
        marginTop: 30,
        backgroundColor: '#e0d8d7',
        borderRadius: 10,
        alignItems: 'center',
        padding: 5,
        height: 500,
    },
    areaLogo: {
        maxHeight: 50,
        marginTop: 10,
        marginLeft: -250,
    },
    profilLogo: {
        maxWidth: 30,
        maxHeight: 30,
        marginBottom: 60,
        marginTop: -40,
        marginLeft: 300,
    },
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
    },
    title: {
        fontSize: 28,
        margin: 30,
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    back: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default Start
