import React from "react";
import { View, Text, StyleSheet, ScrollView} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import CustomerInput from "../../components/CustomersInput/CustomerInput";
import Header from '../../components/Header/header.tsx';
import AppletBox from "../../components/AppletsBox/appletBox";

const Services = () => {
    const Navigation = useNavigation();
    const allScreens = () => {
        Navigation.navigate("All");
    };

    const applets = () => {
        Navigation.navigate("Applets");
    }

    const ServicesDetails = () => {
        Navigation.navigate('Service details')
    }

    const services = () => {
        Navigation.navigate("Services");
    };

    const servicesData = [
        {
            title: "5-Minute Crafts",
            description: "",
            bgColor: "orange",
        },
        {
            title: "The Verge on Youtube",
            description: "",
            bgColor: "red",
        },
        {
            title: "2Smart Cloud",
            description: "",
            bgColor: "grey",
        },
    ];

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
            <View style={styles.searchServices}>
                <CustomerInput
                placeholder="All services"
            />
            </View>
            {servicesData.map((services, index) => (
                <AppletBox
                key={index}
                title={services.title}
                description={services.description}
                bgColor={services.bgColor}
                onPress={ServicesDetails}
                />
            ))}
        </ScrollView>
    );
};

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
        marginBottom: 10,
        width: '130%',
        alignSelf: 'center',
    },
    searchServices: {
        alignItems: 'center',
        marginBottom: 40,
        width: '100%',
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
});

export default Services;