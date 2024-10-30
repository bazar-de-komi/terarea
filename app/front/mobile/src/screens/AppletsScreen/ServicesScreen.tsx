import React from "react";
import { View, Text, StyleSheet, Image, ScrollView} from 'react-native'
import { useNavigation } from "@react-navigation/native";

import CustomerButton from "../../components/CustomerButton";
import BackButton from "../../components/BackButton/backButton";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';
import ProfilLogo from '../../../assets/profilLogo.png';

const ServicesScreen = () => {
    const Navigation = useNavigation();

    const signUp = () => {
        Navigation.navigate('All');
    }

    const serviceDetails = () => {
        Navigation.navigate('Service details')
    }

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
                onPress={serviceDetails}
                />
                <Text style={styles.homeTitle}>Receive a weekly email digest of all new videos for the "5-Minyes Crafts" Youtube channel</Text>
                <View style={styles.homeNavigation}>
                </View>
                <Text style={styles.description}>5-Minute Crafts</Text>
            </View>
            <View style={styles.connectStyle}>
                    <CustomerButton
                    text="Connect"
                    onPress={signUp}
                    type="PRIMARY"
                    bgColor={""}
                    fgColor={""}
                    />
                </View>
            <Text style={styles.descriptionSericesAfterConnectButton}>Receive a weekly email digest of all new videos for the "5-Minyes Crafts" Youtube channel</Text>
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
        color: 'white',
        // fontFamily: 'arial',
    },
    descriptionSericesAfterConnectButton: {
        fontSize: 28,
        fontWeight: 'bold',
        margin: 30,
    },
    description: {
        fontSize: 20,
        margin: 30,
        color: 'white',
        // fontFamily: 'font',
    },
    homeNavigation: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        marginBottom: 20,
    },
    connectStyle: {
        alignItems: 'center',
        marginBottom: 40,
        width: '130%',
        alignSelf: 'center',
    },
})

export default ServicesScreen