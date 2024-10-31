import React from "react";
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput/CustomerInput";
import Header from '../../components/Header/header.tsx';
import AppletAndServiceBox from "../../components/AppletAndServiceBox/appletAndServiceBox";

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

    const handleAppletButton = () => {
        Navigation.navigate("Applet screen");
    };

    const appletsData = [
        {
            title: "Get the weather forecast every dat at 7:00 AM",
            description: "Weather Underground",
            bgColor: "orange",
        },
        {
            title: "Quickly create events in Google Calendar",
            description: "Google",
            bgColor: "blue",
        },
        {
            title: "Track your fitness goals daily",
            description: "Fitbit",
            bgColor: "green",
        },
    ];

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <Header />
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
                    fgColor={"blue"}
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
                    placeholder="Search applets"
                />
            </View>
            {appletsData.map((applet, index) => (
                <AppletAndServiceBox
                    key={index}
                    title={applet.title}
                    description={applet.description}
                    bgColor={applet.bgColor}
                    onPress={handleAppletButton}
                />
            ))}
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
})

export default Applets
