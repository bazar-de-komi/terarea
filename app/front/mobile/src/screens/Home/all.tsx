import React from "react";
import { View, Text, StyleSheet, Image, ScrollView} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput/CustomerInput";
import Header from "../../components/Header/header";
import AppletBox from "../../components/AppletsBox/appletBox";

const All = () => {
    const Navigation = useNavigation();
    const loginPressed = () => {
        Navigation.navigate("Sign In");
    }
    const allScreens = () => {
        Navigation.navigate("All");
    }
    const appletsScreens = () => {
        Navigation.navigate("Applets");
    }

    const servicesScreens = () => {
        Navigation.navigate("Services");
    }

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header/>
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
                onPress={servicesScreens}
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
                title="How we automate tiktok"
                description="Learn how to use TEST"
                bgColor="#f54242"
                />
            <CustomerButton
            text="Back to Sign in"
            onPress={loginPressed}
            type="TERTIARY"
            bgColor={""}
            fgColor={""}
            />
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
    },
    areaLogo: {
        maxHeight: 50,
        marginTop: 10,
        marginLeft: -250,
    },
    profilLogo: {
        maxHeight: 50,
        marginTop: -50,
        marginLeft: 300,
    },
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
        marginLeft: 150,
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
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

export default All