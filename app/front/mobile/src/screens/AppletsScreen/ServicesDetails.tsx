import React from "react";
import { View, Text, StyleSheet, Image, ScrollView} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import AppletBox from "../../components/AppletsBox/appletBox";
import BackButton from "../../components/BackButton/backButton";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import ProfilLogo from '../../../assets/profilLogo.png';

const ServicesDetails = () => {
    const Navigation = useNavigation();

    const callServices = () => {
        Navigation.navigate('Services')
    }

    const servicesScreen = () => {
        Navigation.navigate("Service screen");
    };

    const create = () => {
        Navigation.navigate('Create');
    };

    return (
        <ScrollView showsVerticalScrollIndicator={false}>
            <View style={styles.backContainer}>
                <Image
                    source={AreaLogo}
                    style={styles.areaLogo}
                />
                <Image
                    source={ProfilLogo}
                    style={styles.profilLogo}
                />
                <BackButton
                text="<"
                onPress={callServices}
                />
                <Text style={styles.homeTitle}>5-Minute Crafts integrations</Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.description}>5-Minute Crafts Youtube channel is a</Text>
            <View style={styles.createStyle}>
                    <CustomerButton
                    text="Create"
                    onPress={create}
                    type="PRIMARY"
                    bgColor={""}
                    fgColor={""}
                    />
                </View>
            </View>
            <Text style={styles.homeTitle}>Popular 5-Minute Crafts workflows & automations</Text>
            <AppletBox
            title="Reveive a weekly email digest of all new videos for the 5-Minute Crafts Youtub channel"
            description={"5-Minute Crafts"}
            bgColor={"green"}
            onPress={servicesScreen}

            />
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    backContainer: {
        marginTop: 30,
        backgroundColor: "green",
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
        maxHeight: 50,
        marginTop: -50,
        marginLeft: 300,
    },
    homeTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
    },
    description: {
        fontSize: 20,
        margin: 30,
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    createStyle: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default ServicesDetails