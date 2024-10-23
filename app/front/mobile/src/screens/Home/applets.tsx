import React from "react";
import { View, Text, StyleSheet, Image, ScrollView} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput/CustomerInput";
import Header from '../../components/Header/header.tsx';
import AppletBox from "../../components/AppletsBox/appletBox";

const Applets = () => {
    const Navigation = useNavigation();
    const allScreens = () => {
        Navigation.navigate("All");
    }
    const applets = () => {
        Navigation.navigate("Applets");
    }

    const services = () => {
        Navigation.navigate("Services");
    }

    const appletsBox = () => {
        Navigation.navigate("Applet screen");
    };

    const goHome = () => {
        Navigation.navigate('Home');
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
                onPress={applets}
                type="TERTIARY"
                bgColor={""}
                fgColor={""}
                />
                <CustomerButton
                text="Services"
                onPress={services}
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
            title="Get the weather forecast every dat at 7:00 AM"
            description="Weather Underground"
            bgColor="orange"
            onPress={appletsBox}
            />
    </ScrollView>
    )
}

const styles = StyleSheet.create({
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
    back: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default Applets